"""
Command types for CLI commands.

Python adaptation of TypeScript command types.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class CommandSource(str, Enum):
    """Source of command definition."""
    BUILTIN = "builtin"
    MCP = "mcp"
    PLUGIN = "plugin"
    BUNDLED = "bundled"


@dataclass
class LocalCommandResult:
    """Result of a local command."""

    def __init__(self, result_type: str, **kwargs):
        self.type = result_type
        self.__dict__.update(kwargs)


def text_result(value: str) -> LocalCommandResult:
    """Create a text result."""
    return LocalCommandResult("text", value=value)


def compact_result(compaction_result: Dict[str, Any], display_text: Optional[str] = None) -> LocalCommandResult:
    """Create a compact result."""
    return LocalCommandResult("compact", compaction_result=compaction_result, display_text=display_text)


def skip_result() -> LocalCommandResult:
    """Create a skip result."""
    return LocalCommandResult("skip")


@dataclass
class PromptCommand:
    """Prompt/slash command definition."""
    type: str = "prompt"
    progress_message: str = ""
    content_length: int = 0
    arg_names: Optional[List[str]] = None
    allowed_tools: Optional[List[str]] = None
    model: Optional[str] = None
    source: str = "builtin"
    disable_non_interactive: bool = False


__all__ = [
    "CommandSource",
    "LocalCommandResult",
    "PromptCommand",
    "text_result",
    "compact_result",
    "skip_result",
]