# Copyright (c) Microsoft. All rights reserved.

"""Core Harbor benchmark runner logic."""

import asyncio
import sys
from pathlib import Path

from harbor.job import Job
from harbor.models.job.config import JobConfig
from harbor.models.job.config import OrchestratorConfig
from harbor.models.job.config import RegistryDatasetConfig
from harbor.models.registry import Registry
from harbor.models.registry import RemoteRegistryInfo
from harbor.models.trial.config import AgentConfig
from harbor.models.trial.config import EnvironmentConfig
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_REGISTRY_URL = "https://raw.githubusercontent.com/laude-institute/harbor/main/registry.json"
DEFAULT_DATASET = "terminal-bench"
DEFAULT_VERSION = "2.0"
DEFAULT_MODEL: str | None = None
DEFAULT_N_CONCURRENT = 1
DEFAULT_N_ATTEMPTS = 1
DEFAULT_TIMEOUT_MULTIPLIER = 1.0
DEFAULT_JOBS_DIR = "./harbor_jobs"
DEFAULT_DEBUG = False
DEFAULT_QUIET = False
DEFAULT_AGENT_IMPORT_PATH = "amplifier_app_benchmarks.harbor.amplifier_agent:AmplifierAgent"


def get_registry() -> Registry:
    """Get the Harbor registry."""
    return Registry.from_url(DEFAULT_REGISTRY_URL)


def list_datasets() -> None:
    """List available datasets from the Harbor registry."""
    registry = get_registry()
    table = Table(title="Available Datasets")
    table.add_column("Name", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Description")
    table.add_column("Tasks", style="magenta")

    for dataset in registry.datasets:
        table.add_row(dataset.name, dataset.version, dataset.description, str(len(dataset.tasks)))

    console.print(table)


def list_tasks(dataset_name: str, version: str) -> None:
    """List tasks in a specific dataset.

    Args:
        dataset_name: Name of the dataset
        version: Version of the dataset
    """
    registry = get_registry()

    dataset = None
    for d in registry.datasets:
        if d.name == dataset_name and d.version == version:
            dataset = d
            break

    if dataset is None:
        for d in registry.datasets:
            if d.name == dataset_name:
                dataset = d
                console.print(f"[yellow]Using version {d.version} (requested: {version})[/yellow]")
                break

    if dataset is None:
        console.print(f"[red]Dataset '{dataset_name}' not found[/red]")
        sys.exit(1)

    table = Table(title=f"Tasks in {dataset.name}@{dataset.version}")
    table.add_column("#", style="dim")
    table.add_column("Task Name", style="cyan")

    for i, task in enumerate(dataset.tasks, 1):
        table.add_row(str(i), task.name)

    console.print(table)
    console.print(f"\nTotal: {len(dataset.tasks)} task(s)")


def run_job(
    dataset: str = DEFAULT_DATASET,
    version: str = DEFAULT_VERSION,
    task: str | None = None,
    model: str | None = DEFAULT_MODEL,
    n_concurrent: int = DEFAULT_N_CONCURRENT,
    n_attempts: int = DEFAULT_N_ATTEMPTS,
    timeout_multiplier: float = DEFAULT_TIMEOUT_MULTIPLIER,
    jobs_dir: str = DEFAULT_JOBS_DIR,
    job_name: str | None = None,
    debug: bool = DEFAULT_DEBUG,
    quiet: bool = DEFAULT_QUIET,
) -> None:
    """Run a Harbor benchmark job.

    Args:
        dataset: Name of the benchmark dataset
        version: Version of the dataset
        task: Specific task to run (None for all tasks)
        model: LLM model name for the agent
        n_concurrent: Number of concurrent trials
        n_attempts: Number of attempts per task
        timeout_multiplier: Multiplier for task timeouts
        jobs_dir: Output directory for job results
        job_name: Custom job name (auto-generated if None)
        debug: Enable debug logging
        quiet: Suppress verbose output
    """
    config_kwargs: dict = {
        "jobs_dir": Path(jobs_dir),
        "n_attempts": n_attempts,
        "timeout_multiplier": timeout_multiplier,
        "debug": debug,
        "orchestrator": OrchestratorConfig(
            n_concurrent_trials=n_concurrent,
            quiet=quiet,
        ),
        "environment": EnvironmentConfig(),
        "agents": [
            AgentConfig(
                import_path=DEFAULT_AGENT_IMPORT_PATH,
                model_name=model,
            )
        ],
        "datasets": [
            RegistryDatasetConfig(
                registry=RemoteRegistryInfo(url=DEFAULT_REGISTRY_URL),
                name=dataset,
                version=version,
                task_names=[task] if task else None,
            )
        ],
    }
    if job_name:
        config_kwargs["job_name"] = job_name

    config = JobConfig(**config_kwargs)

    console.print(f"[bold]Running job:[/bold] {config.job_name}")
    console.print(f"  Dataset: {dataset}@{version}")
    console.print(f"  Task filter: {task or 'all'}")
    console.print(f"  Agent: amplifier (model: {model or 'default'})")
    console.print(f"  Output: {jobs_dir}\n")

    job = Job(config)
    asyncio.run(job.run())
