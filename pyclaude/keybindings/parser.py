"""Parse keybinding."""
import re


def parse_keybinding(keyseq: str) -> dict:
    """Parse a keybinding string into components."""
    parts = keyseq.split('+')
    modifiers = []
    key = parts[-1] if parts else ''

    for part in parts[:-1]:
        part_lower = part.lower()
        if part_lower in ('ctrl', 'control'):
            modifiers.append('ctrl')
        elif part_lower in ('alt', 'option'):
            modifiers.append('alt')
        elif part_lower in ('shift', 'shift'):
            modifiers.append('shift')
        elif part_lower in ('cmd', 'command', 'super'):
            modifiers.append('cmd')

    return {'key': key.lower(), 'modifiers': modifiers}


__all__ = ['parse_keybinding']