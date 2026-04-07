"""Bash command helpers matching src/tools/BashTool/bashCommandHelpers.ts"""
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass


@dataclass
class ParsedCommand:
    """A parsed bash command."""
    command: str
    args: list[str]
    is_compound: bool = False


def split_command(command: str) -> list[str]:
    """Split a compound command into segments."""
    # Simple split on &&, ||, ;, |
    import re
    parts = re.split(r'([&|;])', command)
    segments = []
    current = ""
    for part in parts:
        if part in '&|;':
            if current.strip():
                segments.append(current.strip())
            current = ""
        else:
            current += part
    if current.strip():
        segments.append(current.strip())
    return segments


def is_unsafe_compound_command(command: str) -> bool:
    """Check if a compound command might be unsafe."""
    segments = split_command(command)
    return len(segments) > 1


__all__ = ["ParsedCommand", "split_command", "is_unsafe_compound_command"]