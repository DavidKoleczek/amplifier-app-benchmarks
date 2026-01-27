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
3. CRITICAL CHECK 1 - NO MANUAL READING: Search the logs for any evidence that the agent used read_file, read, cat, or similar tools to read "AGENTS.md" or ".amplifier/AGENTS.md". The agent should NOT have read this file manually - it should be auto-injected.
4. Look for tool calls with names like: read_file, read, cat, head, tail, less, more, or similar file reading operations.
5. Check if any of these tool calls targeted files named "AGENTS.md" or paths containing "AGENTS.md".
6. CRITICAL CHECK 2 - PIRATE BEHAVIOR: The AGENTS.md instructed the agent to respond like a pirate. Search the agent's responses for pirate language such as: "Ahoy", "Arrr", "matey", "ye", "landlubber", "shiver me timbers", "Aye", or similar pirate expressions.
7. Evaluate: (a) Did the agent avoid manually reading AGENTS.md? (b) Did the agent respond like a pirate as instructed?"""

RUBRIC = {
    "no_manual_read": "str - (50 points) Is there evidence that the agent did NOT manually read AGENTS.md? Award 50 points if there are NO read_file/read/cat calls targeting AGENTS.md in the logs. Award 0 points if the agent explicitly read AGENTS.md using any file reading tool.",
    "pirate_language_present": "str - (50 points) Did the agent respond using pirate language? Look for words/phrases like 'Ahoy', 'Arrr', 'matey', 'ye', 'Aye', 'landlubber', 'shiver me timbers', or similar pirate expressions in the agent's responses. Award 50 points if clear pirate language is present, 0 points if the agent responded in normal language without any pirate characteristics.",
    "score": "float - Score between 0 and 100 based on the above criteria. Sum the points earned from each criterion. A perfect score (100) means: the agent did not manually read AGENTS.md AND the agent responded like a pirate.",
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
    """Test script for amplifier_agents_md_injection task."""
    return asyncio.run(run_test(test_id, output_dir, instructions_file))


async def run_test(test_id: str, output_dir: Path, instructions_file: Path | None) -> int:
    instructions = get_instructions_from_file_or_default(instructions_file=instructions_file)
    agent_log_hint = get_agent_log_hint()

    try:
        logger.info("Running semantic test: Evaluating AGENTS.md auto-injection...")
        logger.info(f"Agent log hint: {agent_log_hint}")
        logger.info("Checking for pirate language in responses (injection test)")

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
            "injection_type": "pirate_language",
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
            "injection_type": "pirate_language",
            "error": str(e),
        }
        write_test_result(output_dir, test_id, 0, metadata)
        return 0


if __name__ == "__main__":
    sys.exit(main())
