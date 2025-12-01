"""
Deterministic wrapper around the underlying language model.

The concrete backend (llama.cpp, etc.) will be plugged in later.
For now we expose a simple, easily-mockable interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from .types import Message


class LLMBackend(ABC):
    """Abstract interface that any LLM backend must implement."""

    @abstractmethod
    def generate(self, messages: List[Message], max_tokens: int = 256) -> Message:
        """
        Generate a single assistant message from the conversation.

        Implementations should be pure from the caller's perspective:
        - no hidden global state
        - deterministic where possible, or at least configurable via seed.
        """
        raise NotImplementedError


class EchoBackend(LLMBackend):
    """
    Simple echo backend used for early unit tests.

    It just reflects the last user message content.
    """

    def generate(self, messages: List[Message], max_tokens: int = 256) -> Message:
        last_user = next((m for m in reversed(messages) if m.role == "user"), None)
        content = "" if last_user is None else f"echo: {last_user.content[:max_tokens]}"
        return Message(role="assistant", content=content)


