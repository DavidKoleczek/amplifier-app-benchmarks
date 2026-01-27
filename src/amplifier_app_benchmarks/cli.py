"""CLI for running Amplifier benchmarks."""

import asyncio
from datetime import UTC, datetime
import os
from pathlib import Path
from typing import Literal, cast

import click
from eval_recipes.benchmarking.harness import Harness
from eval_recipes.benchmarking.schemas import ScoreRunSpec
from loguru import logger
import yaml


def get_default_data_dir() -> Path:
    """Get the default data directory relative to this package."""
    return Path(__file__).parents[2] / "data"


@click.group()
def cli() -> None:
    """Amplifier App Benchmarks CLI."""


@cli.command()
@click.argument(
    "run_config",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--agents-dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Directory containing agent configurations. Defaults to data/agents.",
)
@click.option(
    "--tasks-dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Directory containing task definitions. Defaults to data/tasks.",
)
@click.option(
    "--runs-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Output directory for results. Creates timestamped dir if not provided.",
)
@click.option(
    "--max-parallel",
    type=int,
    default=15,
    help="Maximum number of trials to run in parallel.",
)
@click.option(
    "--continuation-provider",
    type=click.Choice(["openai", "azure_openai", "none"], case_sensitive=False),
    default="none",
    help="LLM provider for agent continuation.",
)
def run(
    run_config: Path,
    agents_dir: Path | None,
    tasks_dir: Path | None,
    runs_dir: Path | None,
    max_parallel: int,
    continuation_provider: str,
) -> None:
    """Run a score-based benchmark from a run config YAML file.

    RUN_CONFIG is the path to a YAML file defining which agents and tasks to run.
    """
    data_dir = get_default_data_dir()

    if agents_dir is None:
        agents_dir = data_dir / "agents"
    if tasks_dir is None:
        tasks_dir = data_dir / "tasks"

    # Load run definition from config file
    with run_config.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)

    run_definition = ScoreRunSpec.model_validate(config)
    logger.info(f"Loaded run config from {run_config}")

    # Create or use runs directory
    if runs_dir is None:
        base_dir = Path.cwd() / ".benchmark_results"
        timestamp = datetime.now(UTC).strftime("%Y-%m-%d_%H-%M-%S")
        runs_dir = base_dir / timestamp
        logger.info(f"Starting new run: {runs_dir}")
    else:
        if runs_dir.exists() and (runs_dir / "jobs.db").exists():
            logger.info(f"Resuming existing run: {runs_dir}")
        else:
            logger.info(f"Starting new run: {runs_dir}")

    runs_dir.mkdir(parents=True, exist_ok=True)

    # Set up logging
    log_file = runs_dir / "benchmark.log"
    logger.add(log_file, format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}")
    logger.info(f"Logging to {log_file}")

    harness = Harness(
        agents_dir=agents_dir,
        tasks_dir=tasks_dir,
        run_definition=run_definition,
        runs_dir=runs_dir,
        environment={
            "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
            "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
            "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
        },
        max_parallel_trials=max_parallel,
        continuation_provider=cast(Literal["openai", "azure_openai", "none"], continuation_provider),
    )

    asyncio.run(harness.run())
    logger.info("Benchmark complete")


if __name__ == "__main__":
    cli()
