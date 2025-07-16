<<<<<<< HEAD
"""A simple code execution tool (unsafe!)."""

=======
"""A simple code execution tool (unsafe!) exposed as a LangChain ``Tool``."""

from langchain.tools import tool


@tool("Execute")
>>>>>>> 943389f03079c71901d6e2fe832f3ac596696f09
def execute(code: str) -> str:
    """Execute Python code and return the output."""
    local_vars = {}
    exec(code, {}, local_vars)
    return str(local_vars.get("result", ""))
<<<<<<< HEAD
=======


TOOLS = [execute]
>>>>>>> 943389f03079c71901d6e2fe832f3ac596696f09
