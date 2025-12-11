"""Placeholder Redis client helper."""

from typing import Any


def connect_redis(redis_url: str) -> Any:
    """Return a placeholder Redis connection reference."""

    return {"redis": redis_url}
