"""Simplistic multi-agent pipeline with planning, execution, and critique."""

from __future__ import annotations

import os

import openai
from dotenv import load_dotenv

from agents.simple_agent import SimpleAgent
from agents.react_agent import ReActAgent
from agents.reflection_agent import ReflectionAgent


class MultiAgent:
    """Coordinate planner, executor, and critic agents."""

    def __init__(self) -> None:
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.planner = SimpleAgent()
        self.executor = ReActAgent()
        self.critic = ReflectionAgent(base_agent=self.executor)

    def run(self, task: str) -> str:
        """Plan the task, execute it, and critique the result."""
        plan = self.planner.respond(f"Plan how to accomplish: {task}")
        result = self.executor.respond(plan)
        return self.critic.critique(task, result)
