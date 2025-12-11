"""Entrypoint for the LLM router service."""

from lattice.config import ServiceConfig


def main() -> None:
    """Run the LLM router service placeholder."""

    config = ServiceConfig(name="llm-router")
    print(f"Starting {config.name} on {config.host}:{config.port}")


if __name__ == "__main__":
    main()
