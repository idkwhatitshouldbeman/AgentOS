"""
Tool system for the AI agent.

Tools are functions the AI can call to interact with the system:
- File operations
- Screen actions
- System control
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Tool:
    """Represents a tool the AI can use."""

    name: str
    description: str
    parameters: Dict[str, Any]  # JSON schema for parameters


class ToolExecutor(ABC):
    """Abstract base for executing tools."""

    @abstractmethod
    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool with given arguments.

        Returns:
            Dict with 'result' (success) or 'error' (failure)
        """
        raise NotImplementedError


class FileToolExecutor(ToolExecutor):
    """Executor for file operation tools."""

    def __init__(self, file_tools=None):
        """
        Initialize file tool executor.

        Args:
            file_tools: FileTools instance (creates new one if None)
        """
        from .file_tools import FileTools

        self.file_tools = file_tools or FileTools()

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file operation."""
        if tool_name == "read_file":
            return self.file_tools.read_file(arguments.get("path", ""))
        elif tool_name == "write_file":
            return self.file_tools.write_file(
                arguments.get("path", ""), arguments.get("content", "")
            )
        elif tool_name == "list_directory":
            return self.file_tools.list_directory(arguments.get("path", ""))
        elif tool_name == "move_file":
            return self.file_tools.move_file(
                arguments.get("src", ""), arguments.get("dst", "")
            )
        elif tool_name == "delete_file":
            return self.file_tools.delete_file(arguments.get("path", ""))
        else:
            return {"error": f"Unknown file tool: {tool_name}"}


class ScreenToolExecutor(ToolExecutor):
    """Executor for screen interaction tools."""

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute screen action (stub for now)."""
        # TODO: Implement screen actions
        # - click(x, y)
        # - type_text(text)
        # - capture_screen()
        # - find_element(description)
        return {"error": f"Screen tool '{tool_name}' not yet implemented"}


class SystemToolExecutor(ToolExecutor):
    """Executor for system control tools."""

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system action (stub for now)."""
        # TODO: Implement system operations
        # - list_processes()
        # - get_system_info()
        # - (future) overclock settings
        return {"error": f"System tool '{tool_name}' not yet implemented"}


# Registry of available tools
AVAILABLE_TOOLS: List[Tool] = [
    # File tools
    Tool(
        name="read_file",
        description="Read the contents of a file",
        parameters={
            "type": "object",
            "properties": {"path": {"type": "string", "description": "File path"}},
            "required": ["path"],
        },
    ),
    Tool(
        name="write_file",
        description="Write content to a file",
        parameters={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "File content"},
            },
            "required": ["path", "content"],
        },
    ),
    Tool(
        name="list_directory",
        description="List files in a directory",
        parameters={
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Directory path"}},
            "required": ["path"],
        },
    ),
    # Screen tools (stubs for now)
    Tool(
        name="click",
        description="Click at screen coordinates",
        parameters={
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "X coordinate"},
                "y": {"type": "integer", "description": "Y coordinate"},
            },
            "required": ["x", "y"],
        },
    ),
    Tool(
        name="type_text",
        description="Type text at current focus",
        parameters={
            "type": "object",
            "properties": {"text": {"type": "string", "description": "Text to type"}},
            "required": ["text"],
        },
    ),
    # System tools (stubs for now)
    Tool(
        name="get_system_info",
        description="Get system information",
        parameters={"type": "object", "properties": {}},
    ),
]

