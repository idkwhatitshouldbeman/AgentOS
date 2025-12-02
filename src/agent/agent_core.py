from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .llm_interface import LLMBackend
from .types import AgentResult, AgentStep, Message
from .memory.manager import MemoryManager
from .planning.planner import Planner
from .tools.registry import ToolRegistry
from .config import settings


@dataclass
class AgentConfig:
    max_response_tokens: int = 256
    system_prompt: str = "You are an AI agent running inside AgentOS. You have control over the system."


class Agent:
    def __init__(self, backend: LLMBackend, config: AgentConfig | None = None) -> None:
        self._backend = backend
        self._config = config or AgentConfig()
        
        # Initialize Subsystems
        self.memory = MemoryManager()
        self.planner = Planner()
        self.tools = ToolRegistry()
        
        # Register basic tools (placeholder)
        # self.tools.register_function("read_file", read_file_tool)

    def run(self, messages: List[Message]) -> AgentResult:
        """
        Single-step agent run.
        """
        # 1. Add user message to memory
        if messages:
            last_msg = messages[-1]
            if last_msg.role == "user":
                self.memory.add(f"User: {last_msg.content}")

        # 2. Get context from memory
        # context = self.memory.get_context_window()
        
        # 3. Generate response
        # Note: We would inject system prompt and context here
        output = self._backend.generate(
            messages, max_tokens=self._config.max_response_tokens
        )
        
        # 4. Save response to memory
        self.memory.add(f"Assistant: {output.content}")
        
        step = AgentStep(input_messages=messages, tool_calls=[], output_message=output)
        return AgentResult(messages=[output], steps=[step], final_answer=output.content)


