"""
Claude Code hints utilities.

Claude Code hint protocol handling.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ClaudeCodeHint:
    """A Claude Code hint."""
    type: str
    content: str
    plugin_id: Optional[str] = None


def parse_hints(content: str) -> List[ClaudeCodeHint]:
    """Parse hints from content."""
    # Placeholder - would parse <claude-code-hint /> tags
    return []


def extract_plugin_hints(hints: List[ClaudeCodeHint]) -> List[str]:
    """Extract unique plugin IDs from hints."""
    return list(set(h.plugin_id for h in hints if h.plugin_id))


__all__ = [
    "ClaudeCodeHint",
    "parse_hints",
    "extract_plugin_hints",
]