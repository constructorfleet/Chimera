"""Configuration loading helpers for Chimera services."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ServiceConfig:
    """Basic service configuration values."""

    name: str
    host: str = "0.0.0.0"
    port: int = 8000
    redis_url: Optional[str] = None
    mqtt_url: Optional[str] = None
    nats_url: Optional[str] = None
