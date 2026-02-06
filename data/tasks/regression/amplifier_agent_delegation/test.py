# Copyright (c) Microsoft. All rights reserved.

import asyncio
import sys
from pathlib import Path

import click
from eval_recipes.benchmarking.evaluation.semantic_test import semantic_test
from eval_recipes.benchmarking.evaluation.test_utils import (
    get_agent_log_hint,
    get_instructions_from_file_or_default,
    get_test_id_from_env_or_default,
    write_test_result,
)
from loguru import logger

STEPS = """1. Navigate to the agent log directory provided in AGENT LOG LOCATION.
2. Look for session log files corresponding to this test (there should only be one).
3. Search the logs for evidence that a task-like tool was called to delegate to the foundation:explorer agent.
4. Look for indicators such as: task tool invocations, agent spawn events, sub-session creation, or references to "foundation:explorer".
5. Verify that the sub-agent was successfully invoked and returned a response.
6. Evaluate whether the agent successfully delegated to the Explorer sub-agent based on the log evidence."""

RUBRIC = {
    "task_tool_called": "str - (40 points) Is there evidence in the logs that a task-like (task, delegate, or similar) tool was called?",
    "explorer_agent_invoked": "str - (40 points) Is there evidence that an agent like the foundation:explorer sub-agent was invoked?",
    "delegation_successful": "str - (20 points) Does the log evidence indicate the delegation completed successfully with a response?",
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
    """Test script for amplifier_agent_delegation task."""
    return asyncio.run(run_test(test_id, output_dir, instructions_file))


async def run_test(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    instructions = get_instructions_from_file_or_default(instructions_file=instructions_file)
    agent_log_hint = get_agent_log_hint()

    try:
        logger.info("Running semantic test: Evaluating agent delegation via logs...")
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
