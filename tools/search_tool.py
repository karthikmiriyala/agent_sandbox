<<<<<<< HEAD
"""A placeholder search tool."""

def search(query: str) -> str:
    """Return a canned search result."""
    return f"Results for: {query}"
=======
"""A placeholder search tool exposed as a LangChain ``Tool``."""

from langchain.tools import tool


@tool("Search")
def search(query: str) -> str:
    """Return a canned search result."""
    return f"Results for: {query}"


TOOLS = [search]
>>>>>>> 943389f03079c71901d6e2fe832f3ac596696f09
