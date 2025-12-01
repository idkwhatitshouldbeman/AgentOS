from agent.agent_core import Agent, AgentConfig
from agent.llm_interface import EchoBackend
from agent.types import Message


def test_agent_echo_backend_basic():
    backend = EchoBackend()
    agent = Agent(backend=backend, config=AgentConfig(max_response_tokens=100))

    user_message = Message(role="user", content="hello world")
    result = agent.run([user_message])

    assert len(result.messages) == 1
    assert result.messages[0].role == "assistant"
    assert "hello world" in result.messages[0].content


def test_agent_uses_max_tokens_limit():
    backend = EchoBackend()
    agent = Agent(backend=backend, config=AgentConfig(max_response_tokens=5))

    long_text = "abcdefghijklmnopqrstuvwxyz"
    result = agent.run([Message(role="user", content=long_text)])

    # EchoBackend truncates to max_tokens
    assert result.messages[0].content.startswith("echo: ")
    assert len(result.messages[0].content) <= len("echo: ") + 5


