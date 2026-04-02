"""
Format utilities.

Python adaptation.
"""

from typing import Optional, Any


def format_duration(ms: int) -> str:
    """Format milliseconds to duration string (e.g., '1m 23s')."""
    if ms < 0:
        ms = 0
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60

    if hours > 0:
        return f"{hours}h {minutes % 60}m"
    if minutes > 0:
        return f"{minutes}m {seconds % 60}s"
    if seconds > 0:
        return f"{seconds}s"
    return f"{ms}ms"


def format_bytes(bytes_count: int) -> str:
    """Format bytes to human-readable string."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(bytes_count)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    return f"{size:.2f} {units[unit_index]}"


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with thousands separators."""
    if isinstance(num, int):
        return f"{num:,}"
    return f"{num:,.{decimals}f}"


def truncate_string(s: str, max_length: int, ellipsis: str = "...") -> str:
    """Truncate string to max length."""
    if len(s) <= max_length:
        return s
    return s[: max_length - len(ellipsis)] + ellipsis


__all__ = [
    "format_duration",
    "format_bytes",
    "format_number",
    "truncate_string",
]