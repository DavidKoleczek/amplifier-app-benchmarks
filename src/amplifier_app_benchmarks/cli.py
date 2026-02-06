"""CLI for running Amplifier benchmarks."""

import asyncio
from datetime import datetime
import os
from pathlib import Path
import sys

import click
from dotenv import load_dotenv
from loguru import logger

from eval_recipes.benchmarking.loaders import load_agents, load_benchmark, load_tasks
from eval_recipes.benchmarking.pipelines.comparison_pipeline import ComparisonPipeline
from eval_recipes.benchmarking.pipelines.score_pipeline import ScorePipeline

load_dotenv()


def get_default_data_dir() -> Path:
    """Get the default data directory relative to this package."""
    return Path(__file__).parents[2] / "data"


@click.group()
def cli() -> None:
    """Amplifier App Benchmarks CLI."""


@cli.command()
@click.option(
    "--benchmark",
    "benchmark_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    required=True,
    help="Path to benchmark definition YAML file",
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
    "--output-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Directory to store benchmark results. Creates timestamped dir if not provided.",
)
@click.option(
    "--max-parallel",
    type=int,
    default=15,
    help="Maximum number of parallel jobs.",
)
def run(
    benchmark_path: Path,
    agents_dir: Path | None,
    tasks_dir: Path | None,
    output_dir: Path | None,
    max_parallel: int,
) -> None:
    """Run a benchmark from a benchmark definition YAML file."""
    data_dir = get_default_data_dir()

    if agents_dir is None:
        agents_dir = data_dir / "agents"
    if tasks_dir is None:
        tasks_dir = data_dir / "tasks"
    if output_dir is None:
        output_dir = Path.cwd() / ".benchmark_results" / datetime.now().strftime("%Y%m%d_%H%M%S")

    # Ensure output directory exists before setting up file logging
    output_dir.mkdir(parents=True, exist_ok=True)

    # Configure logging to both stderr and file
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(output_dir / "benchmark.log", level="INFO", encoding="utf-8")

    agents = load_agents(agents_dir)
    tasks = load_tasks(tasks_dir)
    benchmark = load_benchmark(benchmark_path)

    logger.info(f"Agents: {list(agents.keys())}")
    logger.info(f"Tasks: {list(tasks.keys())}")

    environment = {
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
        "GITHUB_TOKEN": os.environ.get("GITHUB_TOKEN", ""),
    }

    if benchmark.score_benchmark and benchmark.score_benchmark.score_benchmarks:
        logger.info("Running score pipeline...")
        pipeline = ScorePipeline(
            benchmark=benchmark.score_benchmark,
            agents=agents,
            tasks=tasks,
            output_dir=output_dir,
            max_parallel=max_parallel,
            environment=environment,
        )
        results = asyncio.run(pipeline.run())
        logger.info(f"Completed {len(results)} score job(s)")

    if benchmark.comparison_benchmark and benchmark.comparison_benchmark.comparison_benchmarks:
        logger.info("Running comparison pipeline...")
        comparison_pipeline = ComparisonPipeline(
            benchmark=benchmark.comparison_benchmark,
            agents=agents,
            tasks=tasks,
            output_dir=output_dir,
            max_parallel=max_parallel,
            environment=environment,
        )
        comparison_results = asyncio.run(comparison_pipeline.run())
        logger.info(f"Completed {len(comparison_results)} comparison job(s)")

    logger.info("Benchmark complete")


if __name__ == "__main__":
    cli()
