"""
MCP instructions delta utilities.

Handle MCP instruction changes.
"""

from typing import Dict, Any, Optional


def compute_mcp_delta(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
    """Compute delta between MCP configs."""
    added = {k: v for k, v in new.items() if k not in old}
    removed = {k: v for k, v in old.items() if k not in new}
    return {"added": added, "removed": removed}


__all__ = ["compute_mcp_delta"]