"""Very small agent that simply forwards prompts to OpenAI."""

from __future__ import annotations

from typing import List, Dict

import openai
from dotenv import load_dotenv
import os

from prompts.base_prompts import DEFAULT_SYSTEM_PROMPT


class SimpleAgent:
    """A basic LLM-backed agent with no tools or memory."""

    def __init__(self, model: str = "gpt-3.5-turbo", system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> None:
        """Initialize the agent and configure the OpenAI API key."""
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.system_prompt = system_prompt

    def _build_messages(self, prompt: str) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

    def respond(self, prompt: str) -> str:
        """Return the LLM's response to ``prompt``."""
        messages = self._build_messages(prompt)
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response["choices"][0]["message"]["content"].strip()
