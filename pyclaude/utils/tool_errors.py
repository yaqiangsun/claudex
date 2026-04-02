"""
Tool errors utilities.

Tool error handling.
"""

from typing import Optional


class ToolError(Exception):
    """Tool error."""

    def __init__(self, message: str, tool_name: Optional[str] = None):
        super().__init__(message)
        self.tool_name = tool_name


def format_tool_error(error: Exception) -> str:
    """Format tool error for display."""
    return f"Tool error: {str(error)}"


__all__ = [
    "ToolError",
    "format_tool_error",
]