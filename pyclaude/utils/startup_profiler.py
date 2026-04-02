"""
Startup profiler utilities.

Profile startup performance.
"""

import time
from typing import Dict, Any


def record_startup_marker(name: str) -> None:
    """Record startup marker."""
    pass


def get_startup_profile() -> Dict[str, float]:
    """Get startup profile."""
    return {}


__all__ = [
    "record_startup_marker",
    "get_startup_profile",
]