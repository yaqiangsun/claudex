"""Server types."""
from typing import Any, TypedDict


class ServerConfig(TypedDict):
    """Server configuration."""

    host: str
    port: int
    ssl: bool


class DirectConnectSession(TypedDict):
    """Direct connect session."""

    session_id: str
    org_uuid: str
    config: dict[str, Any]


__all__ = ['ServerConfig', 'DirectConnectSession']