"""
Agent swarms enabled utility.

Check if agent swarms are enabled.
"""

import os


def is_agent_swarms_enabled() -> bool:
    """Check if agent swarms are enabled."""
    # Check environment variable
    env_value = os.environ.get('CLAUDE_CODE_AGENT_SWARMS', 'false').lower()
    if env_value in ('true', '1', 'yes'):
        return True
    return False


def is_swarm_mode() -> bool:
    """Check if running in swarm mode."""
    return os.environ.get('CLAUDE_CODE_SWARM_MODE', 'false').lower() in ('true', '1', 'yes')


__all__ = ['is_agent_swarms_enabled', 'is_swarm_mode']