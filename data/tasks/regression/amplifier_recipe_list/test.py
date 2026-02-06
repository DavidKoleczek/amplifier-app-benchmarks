# Copyright (c) Microsoft. All rights reserved.

import asyncio
import sys
from pathlib import Path

import click
from loguru import logger

from eval_recipes.benchmarking.evaluation.semantic_test import semantic_test
from eval_recipes.benchmarking.evaluation.test_utils import (
    get_agent_log_hint,
    get_instructions_from_file_or_default,
    get_test_id_from_env_or_default,
    write_test_result,
)

STEPS = """1. Navigate to the agent log directory provided in AGENT LOG LOCATION.
2. Look for session log files corresponding to this test (there should only be one).
3. Search the logs for evidence that tools were called to discover available recipes.
4. Look for tool calls such as: recipes tool with 'list' operation, glob/read_file for recipe files, load_skill for recipe information, or similar discovery mechanisms.
5. Count how many separate tool invocations were needed to find/list the recipes. Ideally, the agent should discover recipes efficiently (1-2 tool calls).
6. Verify that the agent successfully discovered and listed recipe names."""

RUBRIC = {
    "tools_used_for_discovery": "str - (40 points) Is there evidence in the logs that the agent used internal tools (such as recipes list, glob, read_file, or similar) to discover available recipes? Award full points if tools were clearly used for discovery.",
    "discovery_efficiency": "str - (30 points) How efficiently did the agent discover recipes? Award 30 points if recipes were found in 1-2 tool calls, 20 points for 3 tool calls, 10 points for 4 tool calls, 0 points for 5+ tool calls or if no tools were used. Count only tool calls directly related to finding recipes.",
    "recipes_discovered": "str - (30 points) Did the agent successfully discover and list actual recipe names? Award full points if the logs show recipe names were found and listed.",
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
    """Test script for amplifier_recipe_list task."""
    return asyncio.run(run_test(test_id, output_dir, instructions_file))


async def run_test(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    instructions = get_instructions_from_file_or_default(instructions_file=instructions_file)
    agent_log_hint = get_agent_log_hint()

    try:
        logger.info("Running semantic test: Evaluating recipe discovery via logs...")
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
