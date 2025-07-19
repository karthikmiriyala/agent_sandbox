"""A simple ReAct agent that uses tools based on LLM reasoning."""

from __future__ import annotations

import os
import re
from typing import List, Dict

import openai
from dotenv import load_dotenv

from prompts.base_prompts import DEFAULT_SYSTEM_PROMPT
from agents.tool_agent import ToolAgent


class ReActAgent:
    """Iteratively reason and act using tools until a final answer is produced."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        tool_agent: ToolAgent | None = None,
        max_steps: int = 5,
    ) -> None:
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.system_prompt = system_prompt
        self.tools = tool_agent or ToolAgent()
        self.max_steps = max_steps

    def _call_llm(self, question: str, scratchpad: str) -> str:
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": question},
        ]
        if scratchpad:
            messages.append({"role": "assistant", "content": scratchpad})
        response = openai.ChatCompletion.create(model=self.model, messages=messages)
        return response["choices"][0]["message"]["content"].strip()

    def respond(self, question: str) -> str:
        scratchpad = ""
        for _ in range(self.max_steps):
            output = self._call_llm(question, scratchpad)

            final = re.search(r"Final Answer\s*:\s*(.*)", output, re.I)
            if final:
                return final.group(1).strip()

            action = re.search(r"Action\s*:\s*(\w+)\[(.*)\]", output)
            if action:
                tool_name, tool_input = action.group(1), action.group(2)
                try:
                    observation = self.tools.run_tool(tool_name, tool_input)
                except Exception as exc:  # pragma: no cover - shouldn't happen in tests
                    observation = f"Error: {exc}"
                scratchpad += f"\nThought: {output}\nObservation: {observation}"
                continue

            # If neither action nor final answer detected, assume output is answer
            return output

        return "Unable to find answer"
