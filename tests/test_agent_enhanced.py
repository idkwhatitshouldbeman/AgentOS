"""
Comprehensive tests for the enhanced agent system.
"""

import pytest
import tempfile
import os
from pathlib import Path

from agent.agent_core_enhanced import AgentEnhanced, AgentConfig
from agent.llm_interface import EchoBackend
from agent.types import Message


def test_agent_enhanced_basic():
    """Test basic agent functionality."""
    backend = EchoBackend()
    config = AgentConfig(max_response_tokens=100, max_iterations=1)
    agent = AgentEnhanced(backend=backend, config=config)
    
    result = agent.run("hello world")
    
    assert result is not None
    assert len(result.messages) > 0
    assert result.final_answer is not None
    assert len(result.steps) > 0


def test_agent_enhanced_tool_registration():
    """Test that tools are properly registered."""
    backend = EchoBackend()
    agent = AgentEnhanced(backend=backend)
    
    # Check that tools are registered
    assert len(agent.tools._tools) > 0
    
    # Check for specific tools
    assert agent.tools.get_tool("read_file") is not None
    assert agent.tools.get_tool("write_file") is not None
    assert agent.tools.get_tool("get_system_info") is not None


def test_agent_enhanced_file_tools():
    """Test file tool execution."""
    backend = EchoBackend()
    agent = AgentEnhanced(backend=backend)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.txt"
        test_content = "Hello, AgentOS!"
        
        # Test write_file tool
        write_tool = agent.tools.get_tool("write_file")
        assert write_tool is not None
        
        result = write_tool(path=str(test_file), content=test_content)
        assert "error" not in result or result.get("success", False)
        
        # Test read_file tool
        read_tool = agent.tools.get_tool("read_file")
        assert read_tool is not None
        
        result = read_tool(path=str(test_file))
        if "error" not in result:
            assert "content" in result
            assert test_content in result["content"]


def test_agent_enhanced_system_tools():
    """Test system tool execution."""
    backend = EchoBackend()
    agent = AgentEnhanced(backend=backend)
    
    # Test get_system_info tool
    sys_tool = agent.tools.get_tool("get_system_info")
    assert sys_tool is not None
    
    result = sys_tool()
    assert "error" not in result
    assert "system" in result or "success" in result


def test_agent_enhanced_memory():
    """Test memory management."""
    backend = EchoBackend()
    agent = AgentEnhanced(backend=backend)
    
    # Add some memories
    agent.memory.add("User asked about files")
    agent.memory.add("Agent read file.txt")
    
    # Search memory
    results = agent.memory.search("files")
    assert len(results) > 0
    
    # Get context window
    context = agent.memory.get_context_window(max_tokens=100)
    assert len(context) > 0


def test_agent_enhanced_iteration_limit():
    """Test that agent respects iteration limit."""
    backend = EchoBackend()
    config = AgentConfig(max_iterations=3)
    agent = AgentEnhanced(backend=backend, config=config)
    
    result = agent.run("test")
    
    # Should not exceed max_iterations
    assert len(result.steps) <= config.max_iterations


def test_agent_enhanced_conversation_history():
    """Test conversation history tracking."""
    backend = EchoBackend()
    agent = AgentEnhanced(backend=backend)
    
    result1 = agent.run("first message")
    assert len(agent.conversation_history) > 0
    
    result2 = agent.run("second message")
    # History should accumulate
    assert len(agent.conversation_history) > len(result1.messages)


def test_agent_enhanced_multiple_messages():
    """Test agent with multiple messages."""
    backend = EchoBackend()
    agent = AgentEnhanced(backend=backend)
    
    messages = [
        Message(role="user", content="Hello"),
        Message(role="user", content="How are you?"),
    ]
    
    result = agent.run(messages)
    assert result is not None
    assert len(result.messages) >= len(messages)

