"""Example tests for the sandbox."""


import openai
from agents.simple_agent import SimpleAgent


def test_simple_agent(monkeypatch):
    """Ensure the agent forwards prompts to OpenAI and loads API key."""

    def fake_create(model, messages):
        return {"choices": [{"message": {"content": "hi"}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    agent = SimpleAgent()
    assert openai.api_key == "test-key"
    assert agent.respond("hello") == "hi"

