"""Entrypoint for the vision router service."""

from lattice.config import ServiceConfig


def main() -> None:
    """Run the vision router service placeholder."""

    config = ServiceConfig(name="vision-router")
    print(f"Starting {config.name} on {config.host}:{config.port}")


if __name__ == "__main__":
    main()
