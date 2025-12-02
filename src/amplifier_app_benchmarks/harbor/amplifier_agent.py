# Copyright (c) Microsoft. All rights reserved.

"""Amplifier agent definition for Harbor benchmarks."""

import os
from pathlib import Path

from harbor.agents.installed.base import BaseInstalledAgent, ExecInput
from harbor.models.agent.context import AgentContext


class AmplifierAgent(BaseInstalledAgent):
    """Harbor agent that runs Amplifier with the toolkit profile."""

    @staticmethod
    def name() -> str:
        return "amplifier"

    @property
    def _install_agent_template_path(self) -> Path:
        return Path(__file__).parent / "amplifier_install.sh"

    def create_run_agent_commands(self, instruction: str) -> list[ExecInput]:
        model = self.model_name or "claude-sonnet-4-5-20250929"
        return [
            ExecInput(
                command=f'amplifier run --profile toolkit:toolkit-dev --model {model} --verbose "{instruction}"',
                env={"ANTHROPIC_API_KEY": os.environ["ANTHROPIC_API_KEY"]},
            )
        ]

    def populate_context_post_run(self, context: AgentContext) -> None:
        pass
