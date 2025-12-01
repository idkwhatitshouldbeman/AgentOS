"""
llama.cpp backend implementation.

This provides a concrete LLM backend using llama.cpp (via llama-cpp-python or direct bindings).
For now, this is a stub that can be expanded when llama.cpp is integrated.
"""

from __future__ import annotations

from typing import List

from .llm_interface import LLMBackend
from .types import Message


class LlamaCppBackend(LLMBackend):
    """
    llama.cpp-based backend for local LLM inference.

    This will use llama-cpp-python or similar bindings to run quantized models locally.
    """

    def __init__(self, model_path: str, n_ctx: int = 2048, n_threads: int = 4) -> None:
        """
        Initialize llama.cpp backend.

        Args:
            model_path: Path to the quantized model file (.gguf)
            n_ctx: Context window size
            n_threads: Number of threads for inference
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self._model = None  # Will be loaded lazily

    def _load_model(self) -> None:
        """Lazy-load the model (stub for now)."""
        # TODO: Implement actual llama.cpp loading
        # Example:
        # from llama_cpp import Llama
        # self._model = Llama(model_path=self.model_path, n_ctx=self.n_ctx, n_threads=self.n_threads)
        pass

    def generate(self, messages: List[Message], max_tokens: int = 256) -> Message:
        """
        Generate response using llama.cpp.

        For now, this is a stub that raises NotImplementedError.
        When implemented, it will:
        1. Convert messages to llama.cpp format
        2. Call model.generate()
        3. Return Message with assistant role
        """
        if self._model is None:
            self._load_model()

        # TODO: Implement actual generation
        # For now, raise to indicate it's not implemented yet
        raise NotImplementedError(
            "LlamaCppBackend.generate() is not yet implemented. "
            "Install llama-cpp-python and implement model loading/generation."
        )

