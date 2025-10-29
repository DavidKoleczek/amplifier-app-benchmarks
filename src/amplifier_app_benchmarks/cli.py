"""CLI for running Amplifier benchmarks."""

import asyncio
import os
import shutil
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

import click
from dotenv import load_dotenv
from eval_recipes.benchmarking.harness import Harness
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()


def download_github_file(url: str, dest_path: Path) -> None:
    """Download a file from GitHub to local path.

    Args:
        url: GitHub raw URL
        dest_path: Local destination path
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response:
        dest_path.write_bytes(response.read())


def fetch_eval_recipes_data(mode: str) -> tuple[Path, Path]:
    """Fetch agent and task data from eval-recipes GitHub repo to temp directory.

    Args:
        mode: Benchmark mode (currently only "quick" is supported)

    Returns:
        Tuple of (agents_dir, tasks_dir) paths in temp directory
    """
    if mode != "quick":
        raise ValueError(f"Unsupported mode: {mode}. Currently only 'quick' is supported.")

    # Create temp directory
    temp_dir = Path(tempfile.mkdtemp(prefix="amplifier_benchmarks_"))
    console.print(f"[cyan]Created temporary directory: {temp_dir}[/cyan]")

    # GitHub raw URLs for eval-recipes data
    github_base = "https://raw.githubusercontent.com/microsoft/eval-recipes/main/data"

    # For quick mode: fetch amplifier_v2 agent and arxiv_conclusion_extraction task
    agent_name = "amplifier_v2"
    task_name = "arxiv_conclusion_extraction"

    # Create directories
    agents_dir = temp_dir / "agents" / agent_name
    tasks_dir = temp_dir / "tasks" / task_name
    agents_dir.mkdir(parents=True, exist_ok=True)
    tasks_dir.mkdir(parents=True, exist_ok=True)

    console.print("[cyan]Fetching agent and task data from GitHub...[/cyan]")

    try:
        # Download agent files
        agent_files = ["agent.yaml", "command_template.txt", "install.dockerfile"]
        for file in agent_files:
            url = f"{github_base}/agents/{agent_name}/{file}"
            dest = agents_dir / file
            download_github_file(url, dest)
        console.print(f"[green]✓[/green] Downloaded agent: {agent_name}")

        # Download task files
        task_files = ["task.yaml", "instructions.txt", "setup.dockerfile", "test.py"]
        for file in task_files:
            url = f"{github_base}/tasks/{task_name}/{file}"
            dest = tasks_dir / file
            download_github_file(url, dest)
        console.print(f"[green]✓[/green] Downloaded task: {task_name}")

    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to download data from GitHub: {e}")
    except Exception as e:
        raise RuntimeError(f"Error fetching eval-recipes data: {e}")

    return temp_dir / "agents", temp_dir / "tasks"


@click.command()
@click.option(
    "--mode",
    type=click.Choice(["quick"], case_sensitive=False),
    required=True,
    help="Benchmark mode. 'quick' runs amplifier_v2 on arxiv_conclusion_extraction task.",
)
@click.option(
    "--runs-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=lambda: Path.cwd() / ".benchmark_results",
    help="Directory to store benchmark run results (default: .benchmark_results in current directory)",
)
@click.option(
    "--num-trials",
    type=int,
    default=1,
    help="Number of times to run each task (default: 1)",
)
def main(
    mode: str,
    runs_dir: Path,
    num_trials: int,
) -> None:
    """Run benchmarks for Amplifier using eval-recipes.

    Examples:

        # Quick benchmark (1 trial)
        run_benchmarks --mode quick

        # Multiple trials with custom output directory
        run_benchmarks --mode quick --num-trials 3 --runs-dir ./my_results
    """
    # Show banner
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Amplifier Benchmarks[/bold cyan]\nPowered by eval-recipes",
            border_style="cyan",
        )
    )
    console.print()

    # Verify required environment variables
    required_vars = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        console.print(f"[red]Error: Missing required environment variables: {', '.join(missing_vars)}[/red]")
        console.print("\nPlease set these environment variables:")
        for var in missing_vars:
            console.print(f"  export {var}=your-key-here")
        raise click.Abort()

    # Fetch agent and task data based on mode
    try:
        agents_dir, tasks_dir = fetch_eval_recipes_data(mode)
    except Exception as e:
        console.print(f"[red]Error preparing benchmark data: {e}[/red]")
        raise click.Abort()

    # Show configuration
    console.print("[cyan]Configuration:[/cyan]")
    console.print(f"  Mode: {mode}")
    console.print("  Agent: amplifier_v2")
    console.print("  Task: arxiv_conclusion_extraction")
    console.print(f"  Trials: {num_trials}")
    console.print(f"  Results directory: {runs_dir}")
    console.print()

    # Set up agent and task filters for quick mode
    agent_filters = ["name=amplifier_v2"]
    task_filters = ["name=arxiv_conclusion_extraction"]

    try:
        # Create harness
        harness = Harness(
            agents_dir=agents_dir,
            tasks_dir=tasks_dir,
            runs_dir=runs_dir,
            environment={
                "ANTHROPIC_API_KEY": os.environ["ANTHROPIC_API_KEY"],
                "OPENAI_API_KEY": os.environ["OPENAI_API_KEY"],
            },
            agent_filters=agent_filters,
            task_filters=task_filters,
            max_parallel_tasks=1,  # Run sequentially for clarity
            num_trials=num_trials,
        )

        # Run benchmarks
        console.print("[bold cyan]Running benchmarks...[/bold cyan]")
        console.print()
        asyncio.run(harness.run(generate_reports=True))

        # Show completion message
        console.print()
        console.print("[bold green]✓ Benchmarks complete![/bold green]")
        console.print(f"Results saved to: {runs_dir}")
        console.print()

        # Security warning
        console.print(
            Panel(
                "Any of the files generated in the benchmarking run may contain secrets that were used during "
                "the evaluation run. [bold red]NEVER[/bold red] commit these files to source control without "
                "first checking for exposed secrets.",
                title="[yellow]⚠ Security Warning[/yellow]",
                border_style="yellow",
            )
        )

    except KeyboardInterrupt:
        console.print("\n[yellow]Benchmark interrupted by user[/yellow]")
        raise click.Abort()
    except Exception as e:
        console.print(f"\n[red]Error running benchmarks: {e}[/red]")
        raise click.Abort()
    finally:
        # Cleanup temp directory
        if agents_dir and agents_dir.parent.exists():
            try:
                shutil.rmtree(agents_dir.parent)
                console.print("[dim]Cleaned up temporary directory[/dim]")
            except Exception:
                pass  # Best effort cleanup


if __name__ == "__main__":
    main()
