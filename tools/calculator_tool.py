<<<<<<< HEAD
"""A simple calculator tool."""

def calculate(expression: str) -> float:
    """Evaluate a math expression using Python's eval."""
    try:
        return float(eval(expression, {"__builtins__": {}}))
    except Exception:
        raise ValueError("Invalid expression")
=======
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
>>>>>>> 943389f03079c71901d6e2fe832f3ac596696f09
