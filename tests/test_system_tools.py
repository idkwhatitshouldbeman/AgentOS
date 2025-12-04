"""
Tests for system tools.
"""

import pytest
from agent.system_tools import SystemTools


def test_system_tools_get_system_info():
    """Test getting system information."""
    tools = SystemTools()
    result = tools.get_system_info()
    
    assert "error" not in result
    assert "system" in result or "success" in result


def test_system_tools_list_processes():
    """Test listing processes."""
    tools = SystemTools()
    result = tools.list_processes(limit=5)
    
    assert "error" not in result
    assert "processes" in result or "success" in result


def test_system_tools_run_command():
    """Test running a command."""
    tools = SystemTools()
    result = tools.run_command("echo 'test'", timeout=5)
    
    assert "error" not in result
    assert "stdout" in result or "success" in result


def test_system_tools_get_network_info():
    """Test getting network information."""
    tools = SystemTools()
    result = tools.get_network_info()
    
    assert "error" not in result
    assert "interfaces" in result or "success" in result


def test_system_tools_get_environment():
    """Test getting environment variables."""
    tools = SystemTools()
    result = tools.get_environment_vars()
    
    assert "error" not in result
    assert "environment" in result or "success" in result


def test_system_tools_dangerous_command_blocked():
    """Test that dangerous commands are blocked when privileged access is disabled."""
    tools = SystemTools(allow_privileged=False)
    result = tools.run_command("rm -rf /", timeout=1)
    
    # Should be blocked
    assert "error" in result or "Dangerous" in str(result)

