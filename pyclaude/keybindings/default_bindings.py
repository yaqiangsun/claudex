"""Default Keybindings."""
from typing import Any

DEFAULT_BINDINGS: dict[str, dict[str, Any]] = {
    'ctrl+c': {'action': 'interrupt', 'description': 'Interrupt current task'},
    'ctrl+z': {'action': 'suspend', 'description': 'Suspend to background'},
    'ctrl+l': {'action': 'clear', 'description': 'Clear screen'},
    'ctrl+a': {'action': 'selectAll', 'description': 'Select all'},
    'ctrl+e': {'action': 'endOfLine', 'description': 'Move to end of line'},
    'ctrl+u': {'action': 'clearLine', 'description': 'Clear current line'},
    'ctrl+k': {'action': 'killToEnd', 'description': 'Kill to end of line'},
    'ctrl+w': {'action': 'killWord', 'description': 'Kill previous word'},
    'escape': {'action': 'normalMode', 'description': 'Enter normal mode'},
    'enter': {'action': 'submit', 'description': 'Submit input'},
    'tab': {'action': 'complete', 'description': 'Autocomplete'},
    'up': {'action': 'historyUp', 'description': 'Previous history'},
    'down': {'action': 'historyDown', 'description': 'Next history'},
    'left': {'action': 'cursorLeft', 'description': 'Move cursor left'},
    'right': {'action': 'cursorRight', 'description': 'Move cursor right'},
}

__all__ = ['DEFAULT_BINDINGS']