from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional


Role = Literal["user", "system", "assistant"]


@dataclass
class Message:
    role: Role
    content: str


@dataclass
class ToolCall:
    name: str
    arguments: Dict[str, Any]


@dataclass
class AgentStep:
    """One reasoning + action step."""

    input_messages: List[Message]
    tool_calls: List[ToolCall]
    output_message: Optional[Message] = None


@dataclass
class AgentResult:
    """Final result returned to the user."""

    messages: List[Message]
    steps: List[AgentStep]


