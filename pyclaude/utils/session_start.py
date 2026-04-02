"""
Session start utilities.

Session start handling.
"""

import os
from typing import Dict, Any


def get_session_start_info() -> Dict[str, Any]:
    """Get session start information."""
    return {
        "session_id": os.environ.get("CLAUDE_CODE_SESSION_ID", ""),
        "cwd": os.getcwd(),
        "timestamp": os.environ.get("CLAUDE_CODE_START_TIME", ""),
    }


__all__ = ["get_session_start_info"]