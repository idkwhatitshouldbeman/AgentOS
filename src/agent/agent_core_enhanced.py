"""
Enhanced Agent Core with proper tool calling and state management.
Based on research from LangGraph/LangChain patterns.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .llm_interface import LLMBackend
from .types import AgentResult, AgentStep, Message, ToolCall, ToolResult
from .memory.manager import MemoryManager
from .planning.planner import Planner
from .tools.registry import ToolRegistry, Tool
from .config import settings


@dataclass
class AgentConfig:
    """Configuration for the AI agent."""
    max_response_tokens: int = 1024
    max_iterations: int = 10
    system_prompt: str = """You are an AI agent running inside AgentOS, an AI-first operating system.
You have full control over the system and can:
- Read and write files
- Execute system commands
- Control the screen (click, type, capture)
- Manage processes
- Access system information

Always think step by step. Use tools when needed. Be helpful, efficient, and safe."""
    temperature: float = 0.7
    enable_tool_calling: bool = True


class AgentEnhanced:
    """
    Enhanced AI agent with proper tool calling and state management.
    
    Features:
    - Multi-step reasoning with tool calls
    - Memory management
    - Task planning
    - Safe tool execution
    """
    
    def __init__(self, backend: LLMBackend, config: AgentConfig | None = None):
        self._backend = backend
        self._config = config or AgentConfig()
        
        # Initialize subsystems
        self.memory = MemoryManager()
        self.planner = Planner()
        self.tools = ToolRegistry()
        
        # Register all available tools
        self._register_tools()
        
        # State tracking
        self.conversation_history: List[Message] = []
        self.current_iteration = 0

    def _register_tools(self):
        """Register all available tools."""
        from .file_tools import FileTools
        from .automation_tools import AutomationTools
        from .system_tools import SystemTools
        from .screen_tools_enhanced import ScreenToolsEnhanced
        
        # Initialize tool instances
        file_tools = FileTools()
        automation_tools = AutomationTools()
        system_tools = SystemTools()
        screen_tools = ScreenToolsEnhanced()
        
        # Register file tools
        def read_file_tool(path: str):
            return file_tools.read_file(path)
        self.tools.register(Tool("read_file", read_file_tool, "Read the contents of a file"))
        
        def write_file_tool(path: str, content: str):
            return file_tools.write_file(path, content)
        self.tools.register(Tool("write_file", write_file_tool, "Write content to a file"))
        
        def list_directory_tool(path: str):
            return file_tools.list_directory(path)
        self.tools.register(Tool("list_directory", list_directory_tool, "List files in a directory"))
        
        def move_file_tool(src: str, dst: str):
            return file_tools.move_file(src, dst)
        self.tools.register(Tool("move_file", move_file_tool, "Move or rename a file"))
        
        def delete_file_tool(path: str):
            return file_tools.delete_file(path)
        self.tools.register(Tool("delete_file", delete_file_tool, "Delete a file or directory"))
        
        # Register automation tools
        def click_tool(x: int, y: int, button: int = 1):
            return automation_tools.click(x, y, button)
        self.tools.register(Tool("click", click_tool, "Click at screen coordinates"))
        
        def type_text_tool(text: str):
            return automation_tools.type_text(text)
        self.tools.register(Tool("type_text", type_text_tool, "Type text at current focus"))
        
        def press_key_tool(key: str):
            return automation_tools.press_key(key)
        self.tools.register(Tool("press_key", press_key_tool, "Press a key or key combination"))
        
        # Register system tools
        def get_system_info_tool():
            return system_tools.get_system_info()
        self.tools.register(Tool("get_system_info", get_system_info_tool, "Get system information"))
        
        def list_processes_tool(limit: int = 20):
            return system_tools.list_processes(limit)
        self.tools.register(Tool("list_processes", list_processes_tool, "List running processes"))
        
        def run_command_tool(command: str, timeout: int = 30):
            return system_tools.run_command(command, timeout)
        self.tools.register(Tool("run_command", run_command_tool, "Run a system command"))
        
        # Register screen tools
        def capture_screen_tool(format: str = "png"):
            return screen_tools.capture_screen(format)
        self.tools.register(Tool("capture_screen", capture_screen_tool, "Capture the entire screen"))
        
        def extract_text_tool(x: int = None, y: int = None, width: int = None, height: int = None):
            return screen_tools.extract_text_from_screen(x, y, width, height)
        self.tools.register(Tool("extract_text_from_screen", extract_text_tool, "Extract text from screen using OCR"))

    def run(self, user_input: str | List[Message]) -> AgentResult:
        """
        Run the agent with user input.
        
        Args:
            user_input: User message string or list of messages
            
        Returns:
            AgentResult with conversation and steps
        """
        # Convert string input to message
        if isinstance(user_input, str):
            messages = [Message(role="user", content=user_input)]
        else:
            messages = user_input
        
        # Add system prompt
        system_msg = Message(role="system", content=self._config.system_prompt)
        self.conversation_history = [system_msg]
        self.conversation_history.extend(messages)
        
        # Add to memory
        for msg in messages:
            if msg.role == "user":
                self.memory.add(f"User: {msg.content}")
        
        # Main agent loop
        steps: List[AgentStep] = []
        self.current_iteration = 0
        
        while self.current_iteration < self._config.max_iterations:
            self.current_iteration += 1
            
            # Get context from memory
            context = self.memory.get_context_window(max_tokens=2000)
            
            # Prepare messages for LLM (with tool definitions if enabled)
            llm_messages = self._prepare_messages_for_llm()
            
            # Generate response
            response = self._backend.generate(
                llm_messages,
                max_tokens=self._config.max_response_tokens,
            )
            
            # Parse tool calls from response (simplified - real implementation would parse JSON)
            tool_calls = self._parse_tool_calls(response)
            tool_results: List[ToolResult] = []
            
            # Execute tools if any
            if tool_calls:
                for tool_call in tool_calls:
                    result = self._execute_tool(tool_call)
                    tool_results.append(result)
                    
                    # Add tool result to conversation
                    tool_result_msg = Message(
                        role="tool",
                        content=json.dumps(result.output) if isinstance(result.output, dict) else str(result.output),
                        name=tool_call.name,
                    )
                    self.conversation_history.append(tool_result_msg)
            
            # Create step
            step = AgentStep(
                input_messages=llm_messages,
                tool_calls=tool_calls,
                tool_results=tool_results,
                output_message=response,
            )
            steps.append(step)
            
            # Add response to conversation
            self.conversation_history.append(response)
            self.memory.add(f"Assistant: {response.content}")
            
            # If no tool calls, we're done
            if not tool_calls:
                break
        
        # Extract final answer
        final_answer = steps[-1].output_message.content if steps else "No response generated"
        
        return AgentResult(
            messages=self.conversation_history,
            steps=steps,
            final_answer=final_answer,
        )

    def _prepare_messages_for_llm(self) -> List[Message]:
        """Prepare messages for LLM with tool definitions."""
        messages = self.conversation_history.copy()
        
        # Add tool definitions if enabled (simplified - real implementation would format properly)
        if self._config.enable_tool_calling:
            tool_defs = self.tools.get_definitions()
            if tool_defs:
                tools_json = json.dumps([{
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                } for t in tool_defs], indent=2)
                
                # Add tools to system message or as separate message
                tools_msg = Message(
                    role="system",
                    content=f"Available tools:\n{tools_json}\n\nYou can call these tools by including tool calls in your response.",
                )
                messages.insert(1, tools_msg)  # Insert after system prompt
        
        return messages

    def _parse_tool_calls(self, message: Message) -> List[ToolCall]:
        """
        Parse tool calls from LLM response.
        
        This is a simplified parser. In production, you'd want:
        - JSON parsing for structured tool calls
        - Natural language understanding
        - Proper error handling
        """
        # For now, return empty list - real implementation would parse JSON tool calls
        # This would be handled by the LLM backend if it supports function calling
        return []

    def _execute_tool(self, tool_call: ToolCall) -> ToolResult:
        """Execute a tool call."""
        tool = self.tools.get_tool(tool_call.name)
        
        if not tool:
            return ToolResult(
                call_id=tool_call.id,
                output="",
                error=f"Tool '{tool_call.name}' not found",
            )
        
        try:
            # Execute tool
            result = tool(**tool_call.arguments)
            
            # Format result
            if isinstance(result, dict):
                if "error" in result:
                    return ToolResult(
                        call_id=tool_call.id,
                        output="",
                        error=result["error"],
                    )
                else:
                    return ToolResult(
                        call_id=tool_call.id,
                        output=json.dumps(result),
                    )
            else:
                return ToolResult(
                    call_id=tool_call.id,
                    output=str(result),
                )
        except Exception as e:
            return ToolResult(
                call_id=tool_call.id,
                output="",
                error=f"Error executing tool: {e}",
            )

