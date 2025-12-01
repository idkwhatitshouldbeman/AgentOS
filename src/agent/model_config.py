"""
Model configuration for the AI agent.

Manages model registry, paths, and presets for different LLM backends.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


@dataclass
class ModelConfig:
    """Configuration for a specific model."""

    name: str
    path: str
    n_ctx: int = 2048  # Context window size
    n_threads: int = 4  # CPU threads for inference
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    max_tokens: int = 512
    stop_sequences: list[str] | None = None


# Default model storage directory
DEFAULT_MODELS_DIR = Path.home() / ".cache" / "ai-os-models"


# Model registry with presets
MODEL_REGISTRY: Dict[str, ModelConfig] = {
    "llama-3.2-3b": ModelConfig(
        name="Llama 3.2 3B Instruct",
        path=str(DEFAULT_MODELS_DIR / "llama-3.2-3b-instruct-q4_k_m.gguf"),
        n_ctx=2048,
        n_threads=4,
        temperature=0.7,
        stop_sequences=["<|eot_id|>", "<|end_of_text|>"],
    ),
    "phi-3.5-mini": ModelConfig(
        name="Phi-3.5 Mini Instruct",
        path=str(DEFAULT_MODELS_DIR / "phi-3.5-mini-instruct-q4_k_m.gguf"),
        n_ctx=4096,  # Phi-3.5 has larger context
        n_threads=4,
        temperature=0.7,
        stop_sequences=["<|end|>", "<|assistant|>"],
    ),
    "qwen2.5-3b": ModelConfig(
        name="Qwen2.5 3B Instruct",
        path=str(DEFAULT_MODELS_DIR / "qwen2.5-3b-instruct-q4_k_m.gguf"),
        n_ctx=2048,
        n_threads=4,
        temperature=0.7,
        stop_sequences=["<|im_end|>", "
im_start>"],
    ),
}


# Default model (fallback)
DEFAULT_MODEL_KEY = "llama-3.2-3b"


def get_model_config(model_key: Optional[str] = None) -> ModelConfig:
    """
    Get model configuration by key.
    
    Args:
        model_key: Model identifier (e.g., "llama-3.2-3b"). If None, uses default.
        
    Returns:
        ModelConfig for the specified model
        
    Raises:
        ValueError: If model_key is not found in registry
    """
    key = model_key or DEFAULT_MODEL_KEY
    
    if key not in MODEL_REGISTRY:
        available = ", ".join(MODEL_REGISTRY.keys())
        raise ValueError(f"Model '{key}' not found. Available models: {available}")
    
    return MODEL_REGISTRY[key]


def list_available_models() -> list[str]:
    """List all available model keys."""
    return list(MODEL_REGISTRY.keys())


def find_model_file(model_key: Optional[str] = None) -> Optional[str]:
    """
    Find model file path and verify it exists.
    
    Args:
        model_key: Model identifier. If None, uses default.
        
    Returns:
        Path to model file if it exists, None otherwise
    """
    config = get_model_config(model_key)
    model_path = Path(config.path)
    
    return str(model_path) if model_path.exists() else None
