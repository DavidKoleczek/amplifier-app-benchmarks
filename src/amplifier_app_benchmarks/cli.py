# Copyright (c) Microsoft. All rights reserved.

"""CLI for running Amplifier benchmarks."""

import asyncio
import os
import shutil
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

import click
import yaml
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


def fetch_eval_recipes_tasks(mode: str, temp_dir: Path) -> Path:
    """Fetch task data from eval-recipes GitHub repo to temp directory.

    Args:
        mode: Benchmark mode (sanity_check, quick, or full)
        temp_dir: Temporary directory to store task data

    Returns:
        Path to tasks directory containing downloaded tasks
    """
    # GitHub raw URLs for eval-recipes data
    github_base = "https://raw.githubusercontent.com/microsoft/eval-recipes/main/data"

    # Define task sets for each mode
    if mode == "sanity_check":
        task_names = ["arxiv_conclusion_extraction", "cpsc_recall_monitor"]
    elif mode == "quick":
        task_names = [
            "cpsc_recall_monitor",
            "email_drafting",
            "product_review_finder",
            "style_blender",
            "news_research_tool",
        ]
    elif mode == "full":
        # Full mode: all available tasks (excluding sec_10q_extractor)
        task_names = [
            "arxiv_conclusion_extraction",
            "arxiv_paper_summarizer",
            "cpsc_recall_monitor",
            "cross_repo_improvement_tool",
            "email_drafting",
            "gdpval_extraction",
            "github_docs_extractor",
            "image_tagging",
            "linkedin_drafting",
            "markdown_deck_converter",
            "news_research_tool",
            "product_review_finder",
            "repo_embedding_server",
            "style_blender",
        ]
    else:
        raise ValueError(f"Unsupported mode: {mode}. Must be one of: sanity_check, quick, full")

    tasks_dir = temp_dir / "tasks"
    console.print("[cyan]Fetching task data from GitHub...[/cyan]")

    try:
        for task_name in task_names:
            task_dir = tasks_dir / task_name
            task_dir.mkdir(parents=True, exist_ok=True)

            # Download task files
            task_files = ["task.yaml", "instructions.txt", "test.py"]
            for file in task_files:
                url = f"{github_base}/tasks/{task_name}/{file}"
                dest = task_dir / file
                try:
                    download_github_file(url, dest)
                except urllib.error.HTTPError as e:
                    if e.code == 404 and file == "setup.dockerfile":
                        # setup.dockerfile is optional
                        continue
                    raise

            # Try to download optional setup.dockerfile
            try:
                url = f"{github_base}/tasks/{task_name}/setup.dockerfile"
                dest = task_dir / "setup.dockerfile"
                download_github_file(url, dest)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    pass  # setup.dockerfile is optional
                else:
                    raise

            console.print(f"[green]✓[/green] Downloaded task: {task_name}")

    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to download data from GitHub: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error fetching eval-recipes data: {e}") from e

    return tasks_dir


def parse_mode_parameter(mode: str) -> tuple[str | None, Path | None]:
    """Parse mode parameter into base mode and custom tasks path.

    Args:
        mode: Mode string which can be:
            - "sanity_check", "quick", or "full" (predefined modes)
            - "quick+/path/to/tasks" (combine mode with custom tasks)
            - "/path/to/tasks" (custom tasks only)

    Returns:
        Tuple of (base_mode, custom_tasks_path):
            - ("quick", None) for predefined mode
            - ("quick", Path("/path")) for combined mode
            - (None, Path("/path")) for custom only
    """
    # Check if mode contains '+' (combined mode)
    if "+" in mode:
        base_mode, tasks_path = mode.split("+", 1)
        if base_mode not in ["sanity_check", "quick", "full"]:
            raise ValueError(f"Invalid base mode: {base_mode}. Must be sanity_check, quick, or full")
        return base_mode, Path(tasks_path)

    # Check if mode is a predefined mode
    if mode in ["sanity_check", "quick", "full"]:
        return mode, None

    # Otherwise, treat as custom tasks path
    return None, Path(mode)


def get_mode_defaults(mode: str | None) -> tuple[int, int]:
    """Get default num_trials and max_parallel_tasks for a given mode.

    Args:
        mode: Benchmark mode (sanity_check, quick, full, or None for custom)

    Returns:
        Tuple of (num_trials, max_parallel_tasks)
    """
    if mode == "sanity_check":
        return 1, 2
    if mode == "quick":
        return 2, 10
    if mode == "full":
        return 5, 20
    if mode is None:  # Custom tasks only
        return 1, 5
    raise ValueError(f"Unknown mode: {mode}")


def prepare_tasks_configuration(
    base_mode: str | None,
    custom_tasks_path: Path | None,
    temp_dir: Path,
) -> tuple[Path, int]:
    """Prepare tasks configuration by fetching and/or copying task definitions.

    Args:
        base_mode: Base mode (sanity_check, quick, full) or None for custom only
        custom_tasks_path: Path to custom tasks directory, or None for mode-only
        temp_dir: Temporary directory to store tasks

    Returns:
        Tuple of (tasks_dir, num_tasks)
    """
    tasks_dir = temp_dir / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)

    num_tasks = 0

    # Fetch eval-recipes tasks if base mode specified
    if base_mode:
        console.print(f"[cyan]Fetching {base_mode} tasks from eval-recipes...[/cyan]")
        eval_tasks_dir = fetch_eval_recipes_tasks(mode=base_mode, temp_dir=temp_dir)
        num_tasks = len(list(eval_tasks_dir.iterdir()))
        console.print(f"[green]✓[/green] Fetched {num_tasks} eval-recipes tasks")

    # Copy custom tasks if path specified
    if custom_tasks_path:
        if not custom_tasks_path.exists():
            raise ValueError(f"Custom tasks path does not exist: {custom_tasks_path}")
        if not custom_tasks_path.is_dir():
            raise ValueError(f"Custom tasks path is not a directory: {custom_tasks_path}")

        console.print(f"[cyan]Copying custom tasks from {custom_tasks_path}...[/cyan]")

        # Copy each task directory
        custom_count = 0
        for task_dir in custom_tasks_path.iterdir():
            if not task_dir.is_dir():
                continue

            # Validate required files
            required_files = ["task.yaml", "instructions.txt", "test.py"]
            missing_files = [f for f in required_files if not (task_dir / f).exists()]
            if missing_files:
                console.print(f"[yellow]⚠[/yellow] Skipping {task_dir.name}: missing {', '.join(missing_files)}")
                continue

            # Copy task directory to tasks_dir
            dest_task_dir = tasks_dir / task_dir.name
            if dest_task_dir.exists():
                console.print(f"[yellow]⚠[/yellow] Skipping {task_dir.name}: already exists (from eval-recipes)")
                continue

            shutil.copytree(task_dir, dest_task_dir)
            custom_count += 1

        console.print(f"[green]✓[/green] Copied {custom_count} custom tasks")
        num_tasks += custom_count

    if num_tasks == 0:
        raise ValueError("No tasks found. Check your mode or custom tasks path.")

    return tasks_dir, num_tasks


def prepare_agent_configuration(
    local_source_path: Path,
    override_agent_path: Path | None,
    temp_dir: Path,
) -> tuple[Path, str]:
    """Prepare agent configuration with local source path.

    Args:
        local_source_path: Path to local amplifier-dev source
        override_agent_path: Optional path to custom agent definition
        temp_dir: Temporary directory to store agent configuration

    Returns:
        Tuple of (agents_dir, agent_name)
    """
    # Determine source agent directory
    if override_agent_path:
        source_agent_dir = override_agent_path
        agent_name = override_agent_path.name
        console.print(f"[cyan]Using custom agent from: {override_agent_path}[/cyan]")
    else:
        # Use bundled default agent
        package_dir = Path(__file__).parent.parent.parent
        source_agent_dir = package_dir / "agents" / "amplifier_next_default"
        agent_name = "amplifier_next_default"
        console.print("[cyan]Using default agent: amplifier_next_default[/cyan]")

    # Validate source agent directory
    required_files = ["agent.yaml", "install.dockerfile", "command_template.txt"]
    for file in required_files:
        if not (source_agent_dir / file).exists():
            raise ValueError(f"Agent directory missing required file: {file}")

    # Copy agent directory to temp location
    agents_dir = temp_dir / "agents"
    dest_agent_dir = agents_dir / agent_name
    dest_agent_dir.mkdir(parents=True, exist_ok=True)

    for file in required_files:
        shutil.copy2(source_agent_dir / file, dest_agent_dir / file)

    # Copy data directory if it exists
    source_data_dir = source_agent_dir / "data"
    if source_data_dir.exists() and source_data_dir.is_dir():
        dest_data_dir = dest_agent_dir / "data"
        shutil.copytree(source_data_dir, dest_data_dir)
        console.print("[green]✓[/green] Copied data directory from agent definition")

    # Update agent.yaml with actual local_source_path
    agent_yaml_path = dest_agent_dir / "agent.yaml"
    with agent_yaml_path.open() as f:
        agent_config = yaml.safe_load(f) or {}

    agent_config["local_source_path"] = str(local_source_path.resolve())

    with agent_yaml_path.open("w") as f:
        yaml.dump(agent_config, f, default_flow_style=False, sort_keys=False)

    console.print(f"[green]✓[/green] Configured agent with local source: {local_source_path}")

    return agents_dir, agent_name


@click.command()
@click.option(
    "--local_source_path",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    required=True,
    help="Path to local amplifier-dev repository to be evaluated",
)
@click.option(
    "--override_agent_path",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Optional path to custom agent definition (default: uses bundled amplifier_next_default)",
)
@click.option(
    "--mode",
    type=str,
    default="quick",
    help=(
        "Task selection mode:\n\n"
        "Predefined modes:\n"
        "  sanity_check: 2 tasks (1 trial, 2 parallel)\n"
        "  quick: 5 tasks (2 trials, 10 parallel, ~1 hour) [default]\n"
        "  full: 14 tasks (5 trials, 20 parallel, many hours)\n\n"
        "Custom tasks:\n"
        "  quick+/path/to/tasks: Add custom tasks to quick mode\n"
        "  /path/to/tasks: Custom tasks only (1 trial, 5 parallel default)"
    ),
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
    default=None,
    help="Number of times to run each task",
)
@click.option(
    "--max-parallel-tasks",
    type=int,
    default=None,
    help="Maximum number of tasks to run in parallel",
)
@click.option(
    "--enable-agent-continuation/--disable-agent-continuation",
    default=True,
    help="Enable or disable agent continuation checks",
)
@click.option(
    "--report-score-threshold",
    type=float,
    default=85.0,
    help="Minimum score threshold to skip report generation (reports generated for scores below this)",
)
def main(
    local_source_path: Path,
    override_agent_path: Path | None,
    mode: str,
    runs_dir: Path,
    num_trials: int | None,
    max_parallel_tasks: int | None,
    enable_agent_continuation: bool,
    report_score_threshold: float,
) -> None:
    """Run benchmarks for Amplifier using eval-recipes."""
    # Show banner
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]Amplifier Benchmarks[/bold cyan]\nPowered by eval-recipes",
            border_style="cyan",
        )
    )
    console.print()

    # Validate local_source_path
    if not local_source_path.exists():
        console.print(f"[red]Error: Local source path does not exist: {local_source_path}[/red]")
        raise click.Abort()

    if not local_source_path.is_dir():
        console.print(f"[red]Error: Local source path is not a directory: {local_source_path}[/red]")
        raise click.Abort()

    # Validate override_agent_path if provided
    if override_agent_path:
        if not override_agent_path.exists():
            console.print(f"[red]Error: Override agent path does not exist: {override_agent_path}[/red]")
            raise click.Abort()

        if not override_agent_path.is_dir():
            console.print(f"[red]Error: Override agent path is not a directory: {override_agent_path}[/red]")
            raise click.Abort()

    # Verify required environment variables
    required_vars = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        console.print(f"[red]Error: Missing required environment variables: {', '.join(missing_vars)}[/red]")
        console.print("\nPlease set these environment variables:")
        for var in missing_vars:
            console.print(f"  export {var}=your-key-here")
        raise click.Abort()

    # Create temp directory for agent and task data
    temp_dir = Path(tempfile.mkdtemp(prefix="amplifier_benchmarks_"))
    console.print(f"[cyan]Created temporary directory: {temp_dir}[/cyan]")

    try:
        # Prepare agent configuration
        agents_dir, agent_name = prepare_agent_configuration(
            local_source_path=local_source_path,
            override_agent_path=override_agent_path,
            temp_dir=temp_dir,
        )

        # Parse mode parameter
        base_mode, custom_tasks_path = parse_mode_parameter(mode)

        # Prepare tasks configuration
        tasks_dir, num_tasks = prepare_tasks_configuration(
            base_mode=base_mode,
            custom_tasks_path=custom_tasks_path,
            temp_dir=temp_dir,
        )

        # Get mode defaults and apply overrides
        default_num_trials, default_max_parallel = get_mode_defaults(base_mode)
        final_num_trials = num_trials if num_trials is not None else default_num_trials
        final_max_parallel = max_parallel_tasks if max_parallel_tasks is not None else default_max_parallel

        # Build task display string
        task_parts = []
        if base_mode == "sanity_check":
            task_parts.append("2 eval-recipes tasks")
        elif base_mode == "quick":
            task_parts.append("5 eval-recipes tasks")
        elif base_mode == "full":
            task_parts.append("14 eval-recipes tasks")

        if custom_tasks_path:
            # Calculate number of custom tasks
            eval_count = 0
            if base_mode == "sanity_check":
                eval_count = 2
            elif base_mode == "quick":
                eval_count = 5
            elif base_mode == "full":
                eval_count = 14

            custom_count = num_tasks - eval_count
            if base_mode:
                task_parts.append(f"{custom_count} custom tasks")
            else:
                task_parts = [f"{num_tasks} custom tasks"]

        task_display = " + ".join(task_parts) if task_parts else f"{num_tasks} tasks"

        # Determine mode display name
        if base_mode and custom_tasks_path:
            mode_display = f"{base_mode} + custom"
        elif base_mode:
            mode_display = base_mode
        else:
            mode_display = "custom"

        # Show configuration
        console.print()
        console.print("[cyan]Configuration:[/cyan]")
        console.print(f"  Mode: {mode_display}")
        console.print(f"  Agent: {agent_name}")
        console.print(f"  Local source: {local_source_path}")
        console.print(f"  Tasks: {task_display} ({num_tasks} total)")
        console.print(f"  Trials per task: {final_num_trials}{' (default)' if num_trials is None else ' (override)'}")
        console.print(
            f"  Max parallel tasks: {final_max_parallel}{' (default)' if max_parallel_tasks is None else ' (override)'}"
        )
        console.print(f"  Results directory: {runs_dir}")
        console.print()

        # Set up agent filter (run all fetched tasks)
        agent_filters = [f"name={agent_name}"]

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
            task_filters=None,  # Run all fetched tasks
            max_parallel_tasks=final_max_parallel,
            num_trials=final_num_trials,
            enable_agent_continuation=enable_agent_continuation,
            report_score_threshold=report_score_threshold,
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
        raise
    finally:
        # Cleanup temp directory
        if temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
                console.print("[dim]Cleaned up temporary directory[/dim]")
            except Exception:
                pass


if __name__ == "__main__":
    main()
