from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional
from datetime import datetime
import uuid

Role = Literal["user", "system", "assistant", "tool"]


@dataclass
class Message:
    role: Role
    content: str
    name: Optional[str] = None  # For tool outputs


@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class ToolResult:
    call_id: str
    output: str
    error: Optional[str] = None


@dataclass
class MemoryEntry:
    id: str
    content: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None


@dataclass
class Task:
    id: str
    description: str
    status: Literal["pending", "running", "completed", "failed"] = "pending"
    dependencies: List[str] = field(default_factory=list)
    result: Optional[str] = None


@dataclass
class Plan:
    id: str
    goal: str
    tasks: List[Task]
    created_at: float


@dataclass
class AgentStep:
    """One reasoning + action step."""

    input_messages: List[Message]
    tool_calls: List[ToolCall] = field(default_factory=list)
    tool_results: List[ToolResult] = field(default_factory=list)
    thought: Optional[str] = None
    output_message: Optional[Message] = None


@dataclass
class AgentResult:
    """Final result returned to the user."""

    messages: List[Message]
    steps: List[AgentStep]
    final_answer: str



