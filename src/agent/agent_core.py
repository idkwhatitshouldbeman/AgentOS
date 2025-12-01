"""
Core agent loop (high-level).

Right now this is a minimal skeleton that:
- takes a user message
- calls the LLM backend once
- returns the response wrapped in AgentResult

Later this will:
- plan tool calls (file ops, screen actions, system APIs)
- run multi-step reasoning
- integrate vision inputs
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .llm_interface import LLMBackend
from .types import AgentResult, AgentStep, Message


@dataclass
class AgentConfig:
    max_response_tokens: int = 256


class Agent:
    def __init__(self, backend: LLMBackend, config: AgentConfig | None = None) -> None:
        self._backend = backend
        self._config = config or AgentConfig()

    def run(self, messages: List[Message]) -> AgentResult:
        """
        Single-step agent run.

        Deterministic and easy to unit test when the backend is mocked.
        """
        output = self._backend.generate(
            messages, max_tokens=self._config.max_response_tokens
        )
        step = AgentStep(input_messages=messages, tool_calls=[], output_message=output)
        return AgentResult(messages=[output], steps=[step])


