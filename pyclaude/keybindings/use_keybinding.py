"""Use keybinding hook."""
from typing import Any, Callable


def use_keybinding(
    key: str,
    action: Callable,
    context: dict[str, Any] | None = None,
) -> None:
    """Register a keybinding with an action."""
    pass  # Placeholder - would integrate with input handler


__all__ = ['use_keybinding']