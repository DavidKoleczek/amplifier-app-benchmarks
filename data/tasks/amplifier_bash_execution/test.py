# Copyright (c) Microsoft. All rights reserved.

import asyncio
import sys
from pathlib import Path

import click
from eval_recipes.benchmarking.semantic_test import semantic_test
from eval_recipes.benchmarking.test_utils import (
    get_agent_log_hint,
    get_instructions_from_file_or_default,
    get_test_id_from_env_or_default,
    write_test_result,
)
from loguru import logger

STEPS = """1. Navigate to the agent log directory provided in AGENT LOG LOCATION.
2. Look for session log files corresponding to this test (there should only be one).
3. Search the logs for evidence that the bash tool was called.
4. Verify that the bash tool execution was successful (look for tool call events, exit codes, or output).
5. Evaluate whether the agent successfully invoked the bash tool based on the log evidence."""

RUBRIC = {
    "bash_tool_called": "str - (60 points) Is there evidence in the logs that the bash tool was called?",
    "execution_successful": "str - (40 points) Does the log evidence indicate the bash command executed successfully?",
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
    """Test script for amplifier_bash_execution task."""
    return asyncio.run(run_test(test_id, output_dir, instructions_file))


async def run_test(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    instructions = get_instructions_from_file_or_default(instructions_file=instructions_file)
    agent_log_hint = get_agent_log_hint()

    try:
        logger.info("Running semantic test: Evaluating bash tool execution via logs...")
        logger.info(f"Agent log hint: {agent_log_hint}")

        result = await semantic_test(
            steps=STEPS,
            rubric=RUBRIC,
            context=instructions,
            working_dir=Path("/project"),
            agent_log_hint=agent_log_hint,
        )

        metadata = {
            "instructions": instructions,
            "agent_log_hint": agent_log_hint,
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
            "agent_log_hint": agent_log_hint,
            "error": str(e),
        }
        write_test_result(output_dir, test_id, 0, metadata)
        return 0


if __name__ == "__main__":
    sys.exit(main())
