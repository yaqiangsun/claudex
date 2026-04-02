"""
Session environment utilities.

Session environment variables.
"""

import os
from typing import Dict


def get_session_environment() -> Dict[str, str]:
    """Get session environment variables."""
    # Placeholder
    return {
        "CLAUDE_CODE_SESSION_ID": os.environ.get("CLAUDE_CODE_SESSION_ID", ""),
        "CLAUDE_CODE_CWD": os.getcwd(),
    }


def update_session_env(key: str, value: str) -> None:
    """Update session environment."""
    os.environ[key] = value


__all__ = [
    "get_session_environment",
    "update_session_env",
]