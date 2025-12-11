"""Entrypoint for the audio router service."""

from lattice.config import ServiceConfig


def main() -> None:
    """Run the audio router service placeholder."""

    config = ServiceConfig(name="audio-router")
    print(f"Starting {config.name} on {config.host}:{config.port}")


if __name__ == "__main__":
    main()
