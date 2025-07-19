"""Agent that exposes basic tools via LangChain's ``Tool`` wrapper."""

from __future__ import annotations

from typing import List

from langchain.tools import Tool

from tools.calculator_tool import calculate
from tools.search_tool import search
from tools.code_executor import execute


class ToolAgent:
    """Simple container for a set of tools."""

    def __init__(self) -> None:
        self.tools: List[Tool] = [calculate, search, execute]

    def list_tool_names(self) -> List[str]:
        """Return the names of available tools."""
        return [tool.name for tool in self.tools]

    def run_tool(self, name: str, input_text: str) -> str:
        """Execute the tool matching ``name`` with ``input_text``."""
        for tool in self.tools:
            if tool.name.lower() == name.lower():
                return tool.run(input_text)
        raise ValueError(f"Unknown tool: {name}")
