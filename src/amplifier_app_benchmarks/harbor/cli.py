# Copyright (c) Microsoft. All rights reserved.

"""CLI entry point for Harbor benchmark runner."""

import sys

import click
from dotenv import load_dotenv
from rich.console import Console

from .runner import DEFAULT_DATASET
from .runner import DEFAULT_DEBUG
from .runner import DEFAULT_JOBS_DIR
from .runner import DEFAULT_MODEL
from .runner import DEFAULT_N_ATTEMPTS
from .runner import DEFAULT_N_CONCURRENT
from .runner import DEFAULT_QUIET
from .runner import DEFAULT_TIMEOUT_MULTIPLIER
from .runner import DEFAULT_VERSION
from .runner import list_datasets
from .runner import list_tasks
from .runner import run_job

load_dotenv()
console = Console()


@click.command()
@click.option("--dataset", "-d", default=DEFAULT_DATASET, help="Benchmark dataset name")
@click.option("--version", "-v", default=DEFAULT_VERSION, help="Dataset version")
@click.option("--task", "-t", default=None, help="Specific task to run (omit for all tasks)")
@click.option("--model", "-m", default=DEFAULT_MODEL, help="LLM model name for the agent")
@click.option("--n-concurrent", "-n", default=DEFAULT_N_CONCURRENT, help="Number of concurrent trials")
@click.option("--n-attempts", "-k", default=DEFAULT_N_ATTEMPTS, help="Number of attempts per task")
@click.option("--timeout-multiplier", default=DEFAULT_TIMEOUT_MULTIPLIER, help="Timeout multiplier for tasks")
@click.option("--jobs-dir", "-o", default=DEFAULT_JOBS_DIR, help="Output directory for job results")
@click.option("--job-name", default=None, help="Custom job name")
@click.option("--debug", is_flag=True, default=DEFAULT_DEBUG, help="Enable debug logging")
@click.option("--quiet", "-q", is_flag=True, default=DEFAULT_QUIET, help="Suppress verbose output")
@click.option("--list-datasets", "show_datasets", is_flag=True, help="List available datasets")
@click.option("--list-tasks", "show_tasks", is_flag=True, help="List tasks in the dataset")
def main(
    dataset: str,
    version: str,
    task: str | None,
    model: str | None,
    n_concurrent: int,
    n_attempts: int,
    timeout_multiplier: float,
    jobs_dir: str,
    job_name: str | None,
    debug: bool,
    quiet: bool,
    show_datasets: bool,
    show_tasks: bool,
) -> None:
    """Run Harbor benchmarks against Amplifier.

    By default, runs terminal-bench@2.0 with a predetermined Amplifier version.
    """
    if show_datasets:
        list_datasets()
        return

    if show_tasks:
        list_tasks(dataset, version)
        return

    try:
        run_job(
            dataset=dataset,
            version=version,
            task=task,
            model=model,
            n_concurrent=n_concurrent,
            n_attempts=n_attempts,
            timeout_multiplier=timeout_multiplier,
            jobs_dir=jobs_dir,
            job_name=job_name,
            debug=debug,
            quiet=quiet,
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(130)


if __name__ == "__main__":
    main()
