"""CLI entry point for ``agent_sandbox`` with optional agent selection."""

from __future__ import annotations

import argparse

from agents.simple_agent import SimpleAgent
from agents.react_agent import ReActAgent
from agents.reflection_agent import ReflectionAgent
from agents.multi_agent import MultiAgent


def main() -> None:
    """Interact with one of the provided agents via the terminal."""
    parser = argparse.ArgumentParser(description="Run an agent interactively")
    parser.add_argument(
        "--agent",
        choices=["simple", "react", "reflection", "multi"],
        default="simple",
        help="Which agent implementation to use",
    )
    args = parser.parse_args()

    if args.agent == "react":
        agent = ReActAgent()
        run = agent.respond
    elif args.agent == "reflection":
        agent = ReflectionAgent()
        run = agent.respond
    elif args.agent == "multi":
        agent = MultiAgent()
        run = agent.run
    else:
        agent = SimpleAgent()
        run = agent.respond

    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        print("Agent:", run(user_input))


if __name__ == "__main__":
    main()
