# Copyright (c) Microsoft. All rights reserved.

import asyncio
import sys
from pathlib import Path

import click
from eval_recipes.benchmarking.semantic_test import semantic_test
from eval_recipes.benchmarking.test_utils import get_instructions_from_file_or_default
from eval_recipes.benchmarking.test_utils import get_test_id_from_env_or_default
from eval_recipes.benchmarking.test_utils import write_test_result
from loguru import logger

STEPS_VALIDATE_UTILITY = """1. Look for Python files in the current directory to find the utility created by the agent.
2. Examine the code to understand how to run it.
3. Run the utility (it should be a simple Python script that can be executed directly).
4. Capture and examine the output:
   - Does it print to stdout?
   - Is the output in the correct format with two lines?
   - First line format: "CPU Cores: <number>"
   - Second line format: "RAM: <number> GB"
5. Validate the output structure:
   - Are both lines present?
   - Can you parse numeric values from both lines?
   - Is "CPU Cores:" followed by a number?
   - Is "RAM:" followed by a number and "GB"?
6. Check that the numbers are reasonable:
   - CPU cores should be a positive integer (typically 1-128)
   - RAM should be a positive number in GB (typically 1-1024)"""

RUBRIC_VALIDATE_UTILITY = {
    "utility_created": "str - (20 points) Did the agent create a Python utility?",
    "utility_runs": "str - (20 points) Does the utility run without errors?",
    "correct_format": "str - (30 points) Is the output in the correct format (two lines: 'CPU Cores: X' and 'RAM: Y GB')?",
    "cpu_value_valid": "str - (15 points) Is the CPU cores value a valid positive integer?",
    "ram_value_valid": "str - (15 points) Is the RAM value a valid positive number?",
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
    """Test script for system_info_utility task."""
    return asyncio.run(run_test(test_id, output_dir, instructions_file))


async def run_test(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    instructions = get_instructions_from_file_or_default(instructions_file=instructions_file)

    try:
        logger.info("Running semantic test: Validating utility output...")
        result = await semantic_test(
            steps=STEPS_VALIDATE_UTILITY,
            rubric=RUBRIC_VALIDATE_UTILITY,
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
