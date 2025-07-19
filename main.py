"""CLI entry point for agent_sandbox."""

from agents.simple_agent import SimpleAgent


def main():
    agent = SimpleAgent()
    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        print("Agent:", agent.respond(user_input))


if __name__ == "__main__":
    main()
