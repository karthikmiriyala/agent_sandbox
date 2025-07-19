"""Simple in-memory store for recent chat messages."""

from __future__ import annotations

from typing import Dict, List


class MemoryManager:
    """Maintain the recent conversation as a list of messages."""

    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.buffer: List[Dict[str, str]] = []

    def add(self, role: str, content: str) -> None:
        """Add a message and ensure the buffer does not exceed ``capacity``."""
        self.buffer.append({"role": role, "content": content})
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def get_messages(self) -> List[Dict[str, str]]:
        """Return the current conversation history."""
        return list(self.buffer)
