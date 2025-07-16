"""Simple in-memory store for recent messages."""

class MemoryManager:
    def __init__(self):
        self.buffer = []

    def add(self, message: str) -> None:
        self.buffer.append(message)
        if len(self.buffer) > 10:
            self.buffer.pop(0)

    def history(self) -> str:
        return "\n".join(self.buffer)
