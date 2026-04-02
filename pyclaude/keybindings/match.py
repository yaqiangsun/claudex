"""Match keybinding."""
from typing import Any


def match_keybinding(key: str, bindings: dict[str, Any]) -> dict | None:
    """Match a keypress against bindings."""
    key_lower = key.lower()
    return bindings.get(key_lower)


__all__ = ['match_keybinding']