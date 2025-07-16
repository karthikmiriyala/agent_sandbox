"""Example tests for the sandbox."""

import openai
from agents.simple_agent import SimpleAgent
from agents.tool_agent import ToolAgent


def test_simple_agent(monkeypatch):
    """Ensure the agent forwards prompts to OpenAI and loads API key."""

    def fake_create(model, messages):
        return {"choices": [{"message": {"content": "hi"}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    agent = SimpleAgent()
    assert openai.api_key == "test-key"
    assert agent.respond("hello") == "hi"


def test_tool_agent():
    """Verify tools run via ToolAgent."""

    agent = ToolAgent()
    assert set(agent.list_tool_names()) == {"Calculator", "Search", "Execute"}
    assert agent.run_tool("Calculator", "2+2") == "4.0"
    assert agent.run_tool("Search", "test") == "Results for: test"
    assert agent.run_tool("Execute", "result = 5") == "5"
