# AgentOS - AI-First Operating System

**An AI-first Operating System where the agent controls everything.**

AgentOS is a research project to build a Linux-based OS designed from the ground up for AI agents. Unlike traditional OSs where AI is an app, in AgentOS, the AI has deep system integration, capable of seeing the screen, controlling inputs, managing files, and controlling the entire system.

## 🚀 Quick Start

**Just run one Python file - no setup needed!**

```bash
python main.py
```

That's it! The agent will start in interactive mode, ready to help you.

### Command Line Options

```bash
# Interactive mode (default)
python main.py

# Run a single command
python main.py -c "list all files in my home directory"

# Specify a model
python main.py -m /path/to/model.gguf
```

## 🎯 Features

### Core Capabilities

- **File Management**: Read, write, list, move, and delete files
- **System Control**: Execute commands, manage processes, get system info
- **Screen Interaction**: Capture screen, click, type, extract text via OCR
- **Memory Management**: Short-term and long-term memory with semantic search
- **Task Planning**: Break down complex goals into executable steps
- **Tool Calling**: AI can use tools to interact with the system

### Architecture

- **Modular Design**: Clean separation between agent, tools, memory, and planning
- **Extensible**: Easy to add new tools and capabilities
- **Testable**: Comprehensive test suite for all components
- **Production-Ready**: Error handling, safety checks, and proper logging

## 📁 Project Structure

```
AgentOS/
├── main.py                 # Main entry point - just run this!
├── src/agent/              # Core agent code
│   ├── agent_core_enhanced.py  # Enhanced agent with tool calling
│   ├── llm_interface.py    # LLM backend interface
│   ├── llama_cpp_backend.py    # Local LLM backend
│   ├── file_tools.py       # File operations
│   ├── system_tools.py     # System control
│   ├── automation_tools.py # UI automation
│   ├── screen_tools_enhanced.py  # Screen capture & OCR
│   ├── memory/             # Memory management
│   ├── planning/           # Task planning
│   └── tools/              # Tool registry
├── tests/                  # Comprehensive test suite
│   ├── test_agent_enhanced.py
│   ├── test_system_tools.py
│   └── ...
└── requirements.txt        # Python dependencies
```

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- Linux (for system tools and screen capture)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### System Dependencies (for full functionality)

```bash
# Ubuntu/Debian
sudo apt install xdotool tesseract-ocr

# For screen capture (if PIL not available)
sudo apt install x11-apps imagemagick
```

### Optional: Local LLM Model

Download a quantized model (e.g., Mistral 7B):

```bash
mkdir -p models
wget -O models/mistral-7b-instruct-v0.2.Q4_K_M.gguf \
  https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
pytest tests/
```

Run specific test files:

```bash
pytest tests/test_agent_enhanced.py
pytest tests/test_system_tools.py
```

## 📖 Usage Examples

### Basic Interaction

```python
from agent.agent_core_enhanced import AgentEnhanced, AgentConfig
from agent.llm_interface import EchoBackend

# Create agent
backend = EchoBackend()  # Or LlamaCppBackend for real LLM
agent = AgentEnhanced(backend=backend)

# Run agent
result = agent.run("List all Python files in my home directory")
print(result.final_answer)
```

### Using Tools Directly

```python
from agent.system_tools import SystemTools

tools = SystemTools()
info = tools.get_system_info()
print(info)
```

## 🔧 Configuration

Configuration is managed in `src/agent/config.py`:

```python
from agent.config import settings

# Set model path
settings.model_path = "/path/to/model.gguf"

# Set workspace
settings.workspace_root = "/home/ai/workspace"
```

## 🏗️ Architecture

### Agent Core

The `AgentEnhanced` class orchestrates:
- **LLM Backend**: Generates responses and tool calls
- **Tool Registry**: Manages available tools
- **Memory Manager**: Maintains conversation and long-term memory
- **Planner**: Breaks down tasks into steps

### Tool System

Tools are registered and can be called by the AI:
- **File Tools**: File operations with safety checks
- **System Tools**: System information and command execution
- **Automation Tools**: Mouse and keyboard control
- **Screen Tools**: Screen capture and OCR

### Memory System

- **Short-term**: Recent conversation context
- **Long-term**: Vector database for semantic search (planned)

## 🚧 Roadmap

- [x] Core agent architecture
- [x] File management tools
- [x] System control tools
- [x] Screen capture and OCR
- [x] Memory management
- [x] Tool calling framework
- [ ] Vision model integration
- [ ] Vector database for long-term memory
- [ ] Advanced planning with LLM
- [ ] OS integration (systemd service)
- [ ] GUI overlay

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

[Add your license here]

## 🙏 Acknowledgments

Built with research from:
- LangGraph/LangChain patterns
- OpenAI function calling
- llama.cpp for local inference
- Modern AI agent architectures

