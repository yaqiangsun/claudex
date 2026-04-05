"""Hook for command keybindings."""
from typing import Dict, Callable, Optional, Any


class CommandKeybindings:
    """Manages keyboard shortcuts for commands."""

    def __init__(self):
        self._bindings: Dict[str, Callable] = {}
        self._keymap: Dict[str, str] = {}

    def register(self, key: str, command: str, handler: Callable) -> None:
        """Register a keybinding."""
        self._bindings[command] = handler
        self._keymap[key] = command

    def unregister(self, key: str) -> None:
        """Unregister a keybinding."""
        command = self._keymap.pop(key, None)
        if command:
            self._bindings.pop(command, None)

    def execute(self, key: str, *args, **kwargs) -> Any:
        """Execute command associated with key."""
        command = self._keymap.get(key)
        if command and command in self._bindings:
            return self._bindings[command](*args, **kwargs)
        return None

    def get_command_for_key(self, key: str) -> Optional[str]:
        """Get command name for a key."""
        return self._keymap.get(key)


__all__ = ['CommandKeybindings']