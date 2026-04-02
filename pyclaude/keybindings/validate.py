"""Validate keybinding."""


def validate_keybinding(keybinding: str) -> bool:
    """Validate a keybinding string."""
    # Simple validation
    return bool(keybinding and len(keybinding) > 0)


__all__ = ['validate_keybinding']