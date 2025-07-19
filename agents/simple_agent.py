"""Very small agent that simply forwards prompts to OpenAI."""

from __future__ import annotations

from typing import List, Dict

import openai
from dotenv import load_dotenv
import os

from prompts.base_prompts import DEFAULT_SYSTEM_PROMPT


from memory.memory_manager import MemoryManager


class SimpleAgent:
    """A basic LLM-backed agent that optionally tracks conversation history."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        memory_manager: MemoryManager | None = None,
    ) -> None:
        """Initialize the agent, configure the OpenAI API key and memory."""
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.system_prompt = system_prompt
        self.memory = memory_manager or MemoryManager()

    def _build_messages(self, prompt: str) -> List[Dict[str, str]]:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory.get_messages())
        messages.append({"role": "user", "content": prompt})
        return messages

    def respond(self, prompt: str) -> str:
        """Return the LLM's response to ``prompt``."""
        messages = self._build_messages(prompt)
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        content = response["choices"][0]["message"]["content"].strip()
        self.memory.add("user", prompt)
        self.memory.add("assistant", content)
        return content
