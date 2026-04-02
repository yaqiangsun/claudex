"""
System prompt utilities.

System prompt handling.
"""

from typing import List


def get_system_prompt() -> str:
    """Get default system prompt."""
    return "You are Claude Code, an AI coding assistant."


def build_system_prompt(components: List[str]) -> str:
    """Build system prompt from components."""
    return "\n\n".join(components)


__all__ = [
    "get_system_prompt",
    "build_system_prompt",
]