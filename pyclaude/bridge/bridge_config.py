"""Bridge configuration utilities."""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass

from .types import BridgeConfig


@dataclass
class BridgeEnvConfig:
    """Configuration from environment variables."""
    enabled: bool = False
    url: Optional[str] = None
    api_key: Optional[str] = None
    environment_id: Optional[str] = None
    session_id: Optional[str] = None


def get_env_bridge_config() -> BridgeEnvConfig:
    """Get bridge configuration from environment variables."""
    return BridgeEnvConfig(
        enabled=os.environ.get('CLAUDE_BRIDGE_ENABLED', '').lower() == 'true',
        url=os.environ.get('CLAUDE_BRIDGE_URL'),
        api_key=os.environ.get('CLAUDE_BRIDGE_API_KEY'),
        environment_id=os.environ.get('CLAUDE_BRIDGE_ENV_ID'),
        session_id=os.environ.get('CLAUDE_BRIDGE_SESSION_ID'),
    )


def merge_bridge_config(
    base: BridgeConfig,
    env: BridgeEnvConfig,
) -> BridgeConfig:
    """Merge environment config into base config."""
    if env.enabled:
        base.enabled = True
    if env.url:
        base.url = env.url
    if env.api_key:
        base.api_key = env.api_key
    if env.environment_id:
        base.environment_id = env.environment_id
    if env.session_id:
        base.session_id = env.session_id
    return base


def load_bridge_config() -> BridgeConfig:
    """Load bridge configuration from all sources."""
    # Start with defaults
    config = BridgeConfig()

    # Merge environment config
    env_config = get_env_bridge_config()
    config = merge_bridge_config(config, env_config)

    return config


# Default bridge port
DEFAULT_BRIDGE_PORT = 3100


def get_bridge_url() -> str:
    """Get the bridge WebSocket URL."""
    env_config = get_env_bridge_config()
    if env_config.url:
        return env_config.url

    # Default to localhost
    host = os.environ.get('CLAUDE_BRIDGE_HOST', 'localhost')
    port = int(os.environ.get('CLAUDE_BRIDGE_PORT', DEFAULT_BRIDGE_PORT))

    return f'ws://{host}:{port}'


__all__ = [
    'BridgeEnvConfig',
    'get_env_bridge_config',
    'merge_bridge_config',
    'load_bridge_config',
    'get_bridge_url',
    'DEFAULT_BRIDGE_PORT',
]