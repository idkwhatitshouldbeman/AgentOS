# AI-OS Agent Developer Guide

Welcome to the AI-OS agent development guide! This document covers everything you need to know to develop, test, and contribute to the AI agent.

## Quick Start

### 1. Clone and Setup

```bash
cd /home/aaroh/Downloads/AgentOS
./scripts/dev-setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Set up development tools
- Run tests to verify everything works

### 2. Activate Virtual Environment

```bash
source .venv/bin/activate
```

### 3. Install LLM Backend (Optional)

```bash
# Install llama.cpp with hardware acceleration
./scripts/setup-llama-cpp.sh

# Download a quantized model
./scripts/download-models.sh
```

## Project Structure

```
AgentOS/
├── src/agent/              # Core agent code
│   ├── types.py            # Data structures
│   ├── llm_interface.py    # LLM abstract interface
│   ├── llama_cpp_backend.py # llama.cpp implementation
│   ├── model_config.py     # Model registry and config
│   ├── agent_core.py       # Core agent loop
│   ├── tools.py            # Tool system framework
│   ├── file_tools.py       # File operations
│   ├── screen_tools.py     # Screen capture
│   ├── automation_tools.py # UI automation
│   ├── vision_interface.py # Vision model interface
│   └── logging_config.py   # Logging system
├── tests/                  # Test suite
├── scripts/                # Utility scripts
└── docs/                   # Documentation
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agent_core.py -v

# Run with coverage
pytest tests/ --cov=src/agent --cov-report=html

# Run only unit tests (fast)
pytest tests/ -v -m "not slow"
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

### Adding a New Tool

1. Define tool in `src/agent/tools.py`:

```python
Tool(
    name="my_tool",
    description="Description of what it does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"},
        },
        "required": ["param1"],
    },
)
```

2. Implement tool executor:

```python
class MyToolExecutor(ToolExecutor):
    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        # Implement tool logic
        return {"success": True, "result": "..."}
```

3. Write tests:

```python
def test_my_tool():
    executor = MyToolExecutor()
    result = executor.execute("my_tool", {"param1": "value"})
    assert result["success"] is True
```

### Working with the Agent

```python
from agent.agent_core import Agent, AgentConfig
from agent.llm_interface import EchoBackend
from agent.types import Message

# Create agent with test backend
backend = EchoBackend()
agent = Agent(backend=backend)

# Run inference
messages = [Message(role="user", content="Hello!")]
result = agent.run(messages)

print(result.messages[0].content)
```

### Using Real LLM

```python
from agent.llama_cpp_backend import LlamaCppBackend
from agent.model_config import get_model_config

# Get model configuration
config = get_model_config("llama-3.2-3b")

# Create backend
backend = LlamaCppBackend(
    model_path=config.path,
    n_ctx=config.n_ctx,
    temperature=config.temperature,
)

# Use with agent
agent = Agent(backend=backend)
```

## Logging

### Basic Logging

```python
from agent.logging_config import setup_logging, get_logger

# Setup logging
setup_logging(log_level="INFO", log_file="agent.log")

# Get logger
logger = get_logger("my_module")

# Log messages
logger.info("Agent started")
logger.debug("Processing message", extra={"agent_step": 1})
```

### JSON Logging

```python
setup_logging(log_level="DEBUG", log_file="agent.json", json_format=True)
```

## Screen Automation

### Capture Screenshots

```python
from agent.screen_tools import ScreenTools

screen = ScreenTools()

# Full screenshot
result = screen.capture_screenshot("/tmp/screenshot.png")

# Region capture
result = screen.capture_screenshot("/tmp/region.png", region=(100, 100, 800, 600))

# Get screen info
info = screen.get_screen_info()
print(f"Screen size: {info['width']}x{info['height']}")
```

### UI Automation

```python
from agent.automation_tools import AutomationTools

auto = AutomationTools()

# Click at coordinates
auto.click(500, 300)

# Type text
auto.type_text("Hello, world!")

# Press keys
auto.press_key("Return")
auto.press_key("ctrl+c")

# Get mouse position
pos = auto.get_mouse_location()
print(f"Mouse at: {pos['x']}, {pos['y']}")
```

## File Operations

```python
from agent.file_tools import FileTools

file_tools = FileTools(allowed_paths=["/home/user/workspace"])

# Read file
result = file_tools.read_file("README.md")
print(result["content"])

# Write file
file_tools.write_file("output.txt", "Hello!")

# List directory
result = file_tools.list_directory("/home/user")
for entry in result["entries"]:
    print(f"{entry['type']}: {entry['name']}")
```

## Testing Best Practices

### 1. Use Fixtures

```python
import pytest

@pytest.fixture
def temp_workspace(tmp_path):
    """Create temporary workspace."""
    return tmp_path

def test_with_workspace(temp_workspace):
    # Use temp_workspace
    pass
```

### 2. Mock External Dependencies

```python
from unittest.mock import Mock, patch

@patch("agent.llama_cpp_backend.Llama")
def test_with_mock(mock_llama):
    mock_llama.return_value = Mock()
    # Test code
```

### 3. Test Error Handling

```python
def test_error_case():
    tools = FileTools()
    result = tools.read_file("/nonexistent/file.txt")
    assert "error" in result
```

## Debugging Tips

### 1. Enable Debug Logging

```python
setup_logging(log_level="DEBUG")
```

### 2. Print Agent Steps

```python
result = agent.run(messages)
for step in result.steps:
    print(f"Step: {step.input_messages}")
    print(f"Tools: {step.tool_calls}")
    print(f"Output: {step.output_message}")
```

### 3. Use pytest Debugging

```bash
# Drop into pdb on failures
pytest tests/ --pdb

# Show print statements
pytest tests/ -s
```

## Contributing

1. Create a feature branch
2. Write tests for your changes
3. Ensure all tests pass
4. Format code with black/isort
5. Submit PR

## Common Issues

### llama-cpp-python Installation Fails

Try installing with specific backend:

```bash
# CPU-only
pip install llama-cpp-python

# With CUDA
CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python

# With Metal (macOS)
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
```

### X11 Tools Not Found

```bash
sudo apt install x11-utils xdotool imagemagick
```

### Import Errors

Make sure you're in the virtual environment:

```bash
source .venv/bin/activate
```

And the package is installed in editable mode:

```bash
pip install -e .
```

## Next Steps

- Read [Architecture Documentation](architecture.md)
- Review [API Reference](api-reference.md)
- Check out [Deployment Guide](deployment-guide.md)
- See [PROJECT_STATUS.md](../PROJECT_STATUS.md) for roadmap
