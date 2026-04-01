"""
Settings hook - access current settings from AppState.

Python adaptation.
"""

from typing import Dict, Any, Optional, Callable


# Global settings storage
_settings: Dict[str, Any] = {}
_subscribers: set[Callable] = set()


def get_settings() -> Dict[str, Any]:
    """Get current settings."""
    return _settings.copy()


def set_settings(new_settings: Dict[str, Any]) -> None:
    """Update settings and notify subscribers."""
    global _settings
    _settings = new_settings.copy()
    _notify_subscribers()


def subscribe_to_settings(callback: Callable) -> Callable:
    """Subscribe to settings changes.

    Returns unsubscribe function.
    """
    _subscribers.add(callback)

    def unsubscribe():
        _subscribers.discard(callback)

    return unsubscribe


def _notify_subscribers() -> None:
    """Notify all subscribers of settings change."""
    for callback in _subscribers:
        callback()


def use_settings() -> Dict[str, Any]:
    """Hook to get current settings."""
    return get_settings()


__all__ = [
    "use_settings",
    "get_settings",
    "set_settings",
    "subscribe_to_settings",
]