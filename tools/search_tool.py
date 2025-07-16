"""A placeholder search tool exposed as a LangChain ``Tool``."""

from langchain.tools import tool


@tool("Search")
def search(query: str) -> str:
    """Return a canned search result."""
    return f"Results for: {query}"


TOOLS = [search]
