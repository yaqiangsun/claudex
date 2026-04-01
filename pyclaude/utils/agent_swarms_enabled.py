"""
Check if agent swarms (teammates) feature is enabled.
"""

import os


def is_agent_swarms_enabled() -> bool:
    """Check if agent swarms/teammates feature is enabled.

    Controlled by CLAUDE_CODE_AGENT_SWARMS environment variable.
    """
    return os.environ.get("CLAUDE_CODE_AGENT_SWARMS", "").lower() == "true"


__all__ = ["is_agent_swarms_enabled"]