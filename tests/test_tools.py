"""
Tests for tool system.
"""

from agent.tools import (
    AVAILABLE_TOOLS,
    FileToolExecutor,
    ScreenToolExecutor,
    SystemToolExecutor,
    Tool,
)


def test_tool_registry():
    """Test that tool registry has expected tools."""
    tool_names = [tool.name for tool in AVAILABLE_TOOLS]
    assert "read_file" in tool_names
    assert "write_file" in tool_names
    assert "list_directory" in tool_names
    assert "click" in tool_names
    assert "type_text" in tool_names
    assert "get_system_info" in tool_names


def test_file_tool_executor():
    """Test FileToolExecutor interface."""
    executor = FileToolExecutor()
    result = executor.execute("read_file", {"path": "/test"})
    assert "error" in result  # Stub returns error for now


def test_screen_tool_executor():
    """Test ScreenToolExecutor interface."""
    executor = ScreenToolExecutor()
    result = executor.execute("click", {"x": 100, "y": 200})
    assert "error" in result  # Stub returns error for now


def test_system_tool_executor():
    """Test SystemToolExecutor interface."""
    executor = SystemToolExecutor()
    result = executor.execute("get_system_info", {})
    assert "error" in result  # Stub returns error for now


def test_tool_schema():
    """Test that tools have valid schemas."""
    for tool in AVAILABLE_TOOLS:
        assert tool.name
        assert tool.description
        assert isinstance(tool.parameters, dict)
        assert "type" in tool.parameters
        assert tool.parameters["type"] == "object"

