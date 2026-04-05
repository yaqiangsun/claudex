"""Hook for checking if a tool can be used."""
from typing import Dict, Any, Optional


# Tool permission states
class ToolPermissionState:
    """States for tool permissions."""
    ALLOWED = "allowed"
    DENIED = "denied"
    PENDING = "pending"
    NOT_FOUND = "not_found"


def use_can_use_tool(tool_name: str, permissions: Optional[Dict[str, str]] = None) -> bool:
    """Check if a tool can be used based on permissions.

    Args:
        tool_name: Name of the tool to check
        permissions: Dict of tool_name -> permission state

    Returns:
        True if tool is allowed, False otherwise
    """
    if permissions is None:
        return True

    return permissions.get(tool_name, ToolPermissionState.ALLOWED) == ToolPermissionState.ALLOWED


__all__ = ['use_can_use_tool', 'ToolPermissionState']