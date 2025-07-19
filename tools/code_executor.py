"""A simple code execution tool (unsafe!) exposed as a LangChain ``Tool``."""

from langchain.tools import tool


@tool("Execute")
def execute(code: str) -> str:
    """Execute Python code and return the output."""
    local_vars = {}
    exec(code, {}, local_vars)
    return str(local_vars.get("result", ""))


TOOLS = [execute]
