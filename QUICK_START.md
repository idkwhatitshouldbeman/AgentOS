# AgentOS - Quick Start Guide

## 🚀 Super Simple - Just Run This!

```bash
python main.py
```

That's it! The AI agent will start and you can talk to it.

## What It Does

AgentOS is an AI-first operating system where the AI agent has full control:

- **File Management**: Read, write, list, move, delete files
- **System Control**: Run commands, manage processes, get system info  
- **Screen Control**: Capture screen, click, type, extract text
- **Memory**: Remembers conversations and can search past interactions
- **Planning**: Breaks down complex tasks into steps

## First Time Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install system tools (optional, for full functionality):**
   ```bash
   sudo apt install xdotool tesseract-ocr
   ```

3. **Run it:**
   ```bash
   python main.py
   ```

## Example Commands

Once running, try:
- "List all files in my home directory"
- "Get system information"
- "Read the file README.md"
- "What processes are running?"

## Using a Real AI Model

By default, AgentOS uses a simple echo backend for testing. To use a real AI model:

1. Download a quantized model (e.g., Mistral 7B):
   ```bash
   mkdir -p models
   wget -O models/mistral-7b-instruct-v0.2.Q4_K_M.gguf \
     https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf
   ```

2. Run with the model:
   ```bash
   python main.py -m models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
   ```

## That's It!

No complex setup, no clicking, no configuration files. Just run `python main.py` and start using your AI-first OS!

