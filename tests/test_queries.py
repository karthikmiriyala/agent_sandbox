"""Example tests for the sandbox."""

import openai
from agents.simple_agent import SimpleAgent
from agents.tool_agent import ToolAgent
from memory.memory_manager import MemoryManager


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


def test_memory_tracking(monkeypatch):
    """SimpleAgent should incorporate chat history using MemoryManager."""

    def fake_create(model, messages):
        # expecting previous history plus new prompt
        assert messages[-3]["content"] == "first"
        assert messages[-2]["content"] == "second"
        assert messages[-1] == {"role": "user", "content": "third"}
        return {"choices": [{"message": {"content": "ok"}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)
    monkeypatch.setenv("OPENAI_API_KEY", "key")

    memory = MemoryManager()
    memory.add("user", "first")
    memory.add("assistant", "second")
    agent = SimpleAgent(memory_manager=memory)

    assert agent.respond("third") == "ok"
    history = memory.get_messages()
    assert history[-2:] == [
        {"role": "user", "content": "third"},
        {"role": "assistant", "content": "ok"},
    ]


def test_react_agent(monkeypatch):
    """ReActAgent should call tools based on LLM output."""

    from agents.react_agent import ReActAgent

    responses = [
        "Thought: use math\nAction: Calculator[2+2]",
        "Thought: done\nFinal Answer: 4.0",
    ]

    calls = []

    def fake_create(model, messages):
        calls.append(messages)
        return {"choices": [{"message": {"content": responses.pop(0)}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)
    monkeypatch.setenv("OPENAI_API_KEY", "key")

    agent = ReActAgent()
    assert agent.respond("calc") == "4.0"
    assert len(calls) == 2
    assert "Observation: 4.0" in calls[1][-1]["content"]


def test_reflection_agent(monkeypatch):
    """ReflectionAgent should critique and improve answers."""

    from agents.reflection_agent import ReflectionAgent

    def fake_base(question):
        return "bad answer"

    class DummyAgent:
        def respond(self, q):
            return fake_base(q)

    responses = ["Critique\nFinal Answer: good"]

    def fake_create(model, messages):
        return {"choices": [{"message": {"content": responses.pop(0)}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)
    monkeypatch.setenv("OPENAI_API_KEY", "k")

    agent = ReflectionAgent(base_agent=DummyAgent())
    assert agent.respond("q") == "good"


def test_multi_agent(monkeypatch):
    """MultiAgent should chain planner, executor, and critic."""

    from agents.multi_agent import MultiAgent

    calls = []

    def fake_create(model, messages):
        calls.append(messages)
        # planner -> executor -> critic
        if len(calls) == 1:
            return {"choices": [{"message": {"content": "do 2+2"}}]}
        elif len(calls) == 2:
            return {"choices": [{"message": {"content": "Final Answer: 4.0"}}]}
        else:
            return {"choices": [{"message": {"content": "Final Answer: ok"}}]}

    monkeypatch.setattr(openai.ChatCompletion, "create", fake_create)
    monkeypatch.setenv("OPENAI_API_KEY", "k")

    agent = MultiAgent()
    assert agent.run("calc") == "ok"
