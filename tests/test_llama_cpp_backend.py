"""
Tests for llama.cpp backend.

These tests use mocked llama.cpp calls to ensure the backend interface works correctly.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from agent.llama_cpp_backend import LlamaCppBackend
from agent.types import Message


def test_llama_cpp_backend_initialization():
    """Test that LlamaCppBackend can be instantiated with valid parameters."""
    backend = LlamaCppBackend(
        model_path="/fake/path/model.gguf",
        n_ctx=2048,
        n_threads=4,
        temperature=0.8,
        top_p=0.95,
    )
    assert backend.model_path == "/fake/path/model.gguf"
    assert backend.n_ctx == 2048
    assert backend.n_threads == 4
    assert backend.temperature == 0.8
    assert backend.top_p == 0.95


@patch("agent.llama_cpp_backend.Llama")
def test_llama_cpp_generate_with_mock(mock_llama_class):
    """Test generate() with mocked llama.cpp."""
    # Setup mock
    mock_model = Mock()
    mock_model.return_value = {
        "choices": [{"text": " Hello! How can I help you today?"}]
    }
    mock_llama_class.return_value = mock_model

    # Create backend and generate
    backend = LlamaCppBackend(model_path="/fake/model.gguf")
    messages = [Message(role="user", content="Hi")]
    result = backend.generate(messages, max_tokens=100)

    # Verify
    assert result.role == "assistant"
    assert "Hello" in result.content
    mock_model.assert_called_once()


@patch("agent.llama_cpp_backend.Llama")
def test_message_formatting(mock_llama_class):
    """Test that messages are formatted correctly."""
    mock_model = Mock()
    mock_model.return_value = {"choices": [{"text": "Response"}]}
    mock_llama_class.return_value = mock_model

    backend = LlamaCppBackend(model_path="/fake/model.gguf")
    messages = [
        Message(role="system", content="You are helpful"),
        Message(role="user", content="Hello"),
    ]
    
    backend.generate(messages)
    
    # Check that the prompt was formatted with ChatML tags
    call_args = mock_model.call_args
    prompt = call_args[0][0]
    assert "<|im_start|>system" in prompt
    assert "You are helpful" in prompt
    assert "<|im_start|>user" in prompt
    assert "Hello" in prompt
    assert "<|im_start|>assistant" in prompt


@patch("agent.llama_cpp_backend.Llama")
def test_lazy_loading(mock_llama_class):
    """Test that model is loaded lazily."""
    backend = LlamaCppBackend(model_path="/fake/model.gguf")
    
    # Model should not be loaded yet
    assert backend._model is None
    mock_llama_class.assert_not_called()
    
    # Now trigger loading
    mock_model = Mock()
    mock_model.return_value = {"choices": [{"text": "Hi"}]}
    mock_llama_class.return_value = mock_model
    
    backend.generate([Message(role="user", content="test")])
    
    # Model should be loaded now
    assert backend._model is not None
    mock_llama_class.assert_called_once()


@patch("agent.llama_cpp_backend.Llama")
def test_token_counting(mock_llama_class):
    """Test token counting functionality."""
    mock_model = Mock()
    mock_model.tokenize.return_value = [1, 2, 3, 4, 5]  # 5 tokens
    mock_llama_class.return_value = mock_model
    
    backend = LlamaCppBackend(model_path="/fake/model.gguf")
    count = backend.count_tokens("Hello world")
    
    assert count == 5
    mock_model.tokenize.assert_called_once()


def test_import_error_handling():
    """Test that helpful error is raised if llama-cpp-python not installed."""
    with patch.dict("sys.modules", {"llama_cpp": None}):
        backend = LlamaCppBackend(model_path="/fake/model.gguf")
        
        with pytest.raises(ImportError, match="llama-cpp-python is not installed"):
            backend.generate([Message(role="user", content="test")])


# NOTE: Real model tests should be run manually or in a separate slow test suite:
# - Test actual model loading with a real .gguf file
# - Test generation quality with different temperatures
# - Test context window handling
# - Test stop sequence functionality

