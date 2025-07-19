"""Agent wrapper that critiques and optionally retries responses."""

from __future__ import annotations

import os
import re
from typing import List, Dict

import openai
from dotenv import load_dotenv

from prompts.base_prompts import REFLECTION_SYSTEM_PROMPT
from agents.react_agent import ReActAgent


class ReflectionAgent:
    """Wrap another agent and improve its answers via a critique step."""

    def __init__(
        self,
        base_agent: ReActAgent | None = None,
        model: str = "gpt-3.5-turbo",
        critique_prompt: str = REFLECTION_SYSTEM_PROMPT,
    ) -> None:
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.base_agent = base_agent or ReActAgent()
        self.model = model
        self.critique_prompt = critique_prompt

    def _critique(self, question: str, answer: str) -> str:
        """Return the critic model's response to ``answer``."""
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.critique_prompt},
            {
                "role": "user",
                "content": (
                    f"Question: {question}\nAnswer: {answer}\n"
                    "Provide feedback and, if needed, a corrected final answer."
                ),
            },
        ]
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response["choices"][0]["message"]["content"].strip()

    def critique(self, question: str, answer: str) -> str:
        """Public method to critique a precomputed answer."""
        content = self._critique(question, answer)
        match = re.search(r"Final Answer\s*:\s*(.*)", content, re.I)
        if match:
            return match.group(1).strip()
        return answer

    def respond(self, question: str) -> str:
        initial = self.base_agent.respond(question)
        return self.critique(question, initial)
