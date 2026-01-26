# Copyright (c) Microsoft. All rights reserved.

"""
Test script for amplifier_provider_responds task.

This is a regression test that verifies Amplifier can successfully communicate
with the LLM provider and receive a coherent response.
"""

import asyncio
import sys
from pathlib import Path

import click
from eval_recipes.benchmarking.semantic_test import semantic_test
from eval_recipes.benchmarking.test_utils import (
    get_instructions_from_file_or_default,
    get_test_id_from_env_or_default,
    write_test_result,
)
from loguru import logger

STEPS = """1. Check if a file named "result.txt" exists in the /project directory.
2. If it exists, read the contents of result.txt.
3. Check if the file contains the exact text "REGRESSION_PROVIDER_OK".
4. Evaluate whether the agent successfully created the file with the correct content."""

RUBRIC = {
    "file_exists": "str - (40 points) Does the file 'result.txt' exist in /project?",
    "correct_content": "str - (60 points) Does result.txt contain 'REGRESSION_PROVIDER_OK'?",
    "score": "float - Score between 0 and 100 based on the above criteria. Sum the points earned from each criterion.",
}


@click.command()
@click.option(
    "--test-id",
    default=lambda: get_test_id_from_env_or_default("dev"),
    help="Test ID for result file naming (defaults to EVAL_RECIPES_TEST_ID env var)",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=lambda: Path(__file__).parents[0],
    help="Directory to write result file",
)
@click.option(
    "--instructions-file",
    type=click.Path(path_type=Path),
    default=None,
    help="Path to instructions file (defaults to ./instructions.txt in working directory)",
)
def main(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    """Test script for amplifier_provider_responds task."""
    return asyncio.run(run_test(test_id, output_dir, instructions_file))


async def run_test(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    """
    Semantic test: Use an auditor agent to evaluate if the agent created
    result.txt with the expected content.
    """
    instructions = get_instructions_from_file_or_default(instructions_file=instructions_file)

    try:
        logger.info("Running semantic test: Evaluating provider response...")
        result = await semantic_test(
            steps=STEPS,
            rubric=RUBRIC,
            context=instructions,
            working_dir=Path("/project"),
        )

        metadata = {
            "instructions": instructions,
            "semantic_test_result": {
                "score": result.score,
                "details": result.metadata,
            },
        }

        write_test_result(output_dir, test_id, result.score, metadata)
        logger.info(f"Test completed with score: {result.score:.1f}/100")
        return 0

    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
        metadata = {
            "instructions": instructions,
            "error": str(e),
        }
        write_test_result(output_dir, test_id, 0, metadata)
        return 0


if __name__ == "__main__":
    sys.exit(main())
