# Copyright (c) Microsoft. All rights reserved.

import asyncio
import sys
from pathlib import Path

import click
from loguru import logger

from eval_recipes.benchmarking.evaluation.semantic_test import semantic_test
from eval_recipes.benchmarking.evaluation.test_utils import (
    get_instructions_from_file_or_default,
    get_test_id_from_env_or_default,
    write_test_result,
)

# The exact target text that should be extracted from the PDF
TARGET_CODE = "BENCHMARK_SECRET_CODE_7X9K2M4P"

STEPS = f"""1. Check if a file named "extracted_code.txt" exists in the /project directory.
2. If it exists, read the contents of extracted_code.txt.
3. Check if the file contains the exact code "{TARGET_CODE}".
4. Evaluate whether the agent successfully read the PDF and extracted the correct verification code."""

RUBRIC = {
    "file_exists": "str - (30 points) Does the file 'extracted_code.txt' exist in /project?",
    "correct_code": f"str - (70 points) Does extracted_code.txt contain the exact code '{TARGET_CODE}'?",
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
    """Test script for amplifier_pdf_extraction task."""
    return asyncio.run(run_test(test_id, output_dir, instructions_file))


async def run_test(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    instructions = get_instructions_from_file_or_default(instructions_file=instructions_file)

    try:
        logger.info("Running semantic test: Evaluating PDF extraction...")
        logger.info(f"Expected target code: {TARGET_CODE}")

        result = await semantic_test(
            steps=STEPS,
            rubric=RUBRIC,
            context=instructions,
            working_dir=Path("/project"),
        )

        metadata = {
            "instructions": instructions,
            "expected_target_code": TARGET_CODE,
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
            "expected_target_code": TARGET_CODE,
            "error": str(e),
        }
        write_test_result(output_dir, test_id, 0, metadata)
        return 0


if __name__ == "__main__":
    sys.exit(main())
