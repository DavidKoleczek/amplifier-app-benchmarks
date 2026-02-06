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
3. CRITICAL CHECK 1 - NO MANUAL READING: Search the logs for any evidence that the agent used read_file, read, cat, or similar tools to read context files like "direct-context.md", "behavior-context.md", or any file in the "context/" directory. The agent should NOT have read these files manually - they should be auto-injected via bundle context.include.
4. Look for tool calls with names like: read_file, read, cat, head, tail, less, more, or similar file reading operations.
5. Check if any of these tool calls targeted files named "direct-context.md", "behavior-context.md", or paths containing "context/".
6. CRITICAL CHECK 2 - DIRECT CONTEXT TOKEN: Look for the exact token 'BUNDLE_DIRECT_CONTEXT_ALPHA' in the agent's responses. This token proves that context.include in the bundle's frontmatter resolved correctly.
7. CRITICAL CHECK 3 - TRANSITIVE CONTEXT TOKEN: Look for the exact token 'BEHAVIOR_TRANSITIVE_CONTEXT_BETA' in the agent's responses. This token proves that context contributed by included behaviors resolved correctly.
8. Evaluate: (a) Did the agent avoid manually reading context files? (b) Did the agent find and report the direct context token? (c) Did the agent find and report the transitive context token?"""

RUBRIC = {
    "no_manual_read": "str - (34 points) Is there evidence that the agent did NOT manually read context files? Award 34 points if there are NO read_file/read/cat calls targeting 'direct-context.md', 'behavior-context.md', or any file in a 'context/' directory in the logs. Award 0 points if the agent explicitly read any context file using any file reading tool. The context should be auto-injected via bundle composition, not manually read.",
    "direct_context_token_found": "str - (33 points) Did the agent report finding 'BUNDLE_DIRECT_CONTEXT_ALPHA'? Award 33 points if this exact token appears in the agent's response. Award 0 points if the agent could not find this token or reported it as missing.",
    "transitive_context_token_found": "str - (33 points) Did the agent report finding 'BEHAVIOR_TRANSITIVE_CONTEXT_BETA'? Award 33 points if this exact token appears in the agent's response. Award 0 points if the agent could not find this token or reported it as missing.",
    "score": "float - Score between 0 and 100 based on the above criteria. Sum the points earned from each criterion. A perfect score (100) means: the agent did not manually read context files AND both tokens were found, proving bundle context resolution works correctly via auto-injection.",
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
    """Test script for amplifier_bundle_context task."""
    return asyncio.run(run_test(test_id, output_dir, instructions_file))


async def run_test(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    instructions = get_instructions_from_file_or_default(instructions_file=instructions_file)
    agent_log_hint = get_agent_log_hint()

    try:
        logger.info("Running semantic test: Evaluating bundle context resolution...")
        logger.info(f"Agent log hint: {agent_log_hint}")
        logger.info("Checking for context tokens: BUNDLE_DIRECT_CONTEXT_ALPHA and BEHAVIOR_TRANSITIVE_CONTEXT_BETA")

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
            "test_type": "bundle_context_resolution",
            "expected_tokens": {
                "direct": "BUNDLE_DIRECT_CONTEXT_ALPHA",
                "transitive": "BEHAVIOR_TRANSITIVE_CONTEXT_BETA",
            },
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
            "test_type": "bundle_context_resolution",
            "error": str(e),
        }
        write_test_result(output_dir, test_id, 0, metadata)
        return 0


if __name__ == "__main__":
    sys.exit(main())
