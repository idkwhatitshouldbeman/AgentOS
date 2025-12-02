"""
Global Configuration for AgentOS.
"""

from dataclasses import dataclass
import os

@dataclass
class Config:
    # LLM Settings
    model_path: str = os.getenv("AGENT_MODEL_PATH", "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")
    context_window: int = 4096
    max_tokens: int = 1024
    temperature: float = 0.7
    
    # System Settings
    workspace_root: str = os.getenv("AGENT_WORKSPACE", "/home/ai/workspace")
    memory_path: str = os.path.join(workspace_root, "memory")
    
    # Feature Flags
    enable_vision: bool = False
    enable_voice: bool = False
    
    # Debug
    debug_mode: bool = True

# Global instance
settings = Config()
