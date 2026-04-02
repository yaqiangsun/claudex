"""Keybinding schema."""
from typing import Any, TypedDict


class KeybindingSchema(TypedDict):
    """Schema for keybinding configuration."""

    key: str
    action: str
    description: str
    context: str | None


__all__ = ['KeybindingSchema']