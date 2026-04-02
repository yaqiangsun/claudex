"""
Logo V2 utils utilities.

Logo display utilities.
"""

from typing import List


def get_logo_lines() -> List[str]:
    """Get logo lines for display."""
    return [
        "  _____ _                  ",
        " |  ___| |_ _   _ _ __   ",
        " | |_  | __| | | | '_ \\  ",
        " |  _| | |_| |_| | | | | ",
        " |_|   |__|\\__,_|_| |_| | ",
    ]


__all__ = ["get_logo_lines"]