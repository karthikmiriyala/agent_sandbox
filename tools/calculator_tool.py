"""A simple calculator tool exposed as a LangChain ``Tool``."""

from langchain.tools import tool


@tool("Calculator")
def calculate(expression: str) -> str:
    """Evaluate a math expression and return the result."""
    try:
        return str(float(eval(expression, {"__builtins__": {}})))
    except Exception as exc:
        raise ValueError("Invalid expression") from exc


TOOLS = [calculate]
