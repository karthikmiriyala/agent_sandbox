"""Example tests for the sandbox."""

from agents.simple_agent import SimpleAgent


def test_echo():
    agent = SimpleAgent()
    assert agent.respond("hello") == "hello"
