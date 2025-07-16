"""A simple calculator tool."""

def calculate(expression: str) -> float:
    """Evaluate a math expression using Python's eval."""
    try:
        return float(eval(expression, {"__builtins__": {}}))
    except Exception:
        raise ValueError("Invalid expression")
