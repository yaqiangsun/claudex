"""Theme command - manage color themes."""

import os
import json
from pathlib import Path
from typing import Any, Dict


THEMES = {
    'default': 'Default terminal colors',
    'dark': 'Dark theme',
    'light': 'Light theme',
    'monokai': 'Monokai colors',
    'dracula': 'Dracula colors',
    'nord': 'Nord colors',
}


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the theme command."""
    args = args.strip().lower() if args else ''

    if not args or args == 'list':
        return await list_themes()

    if args == 'current':
        return await show_current_theme()

    if args in THEMES:
        return await set_theme(args)

    return {'type': 'text', 'value': f'Unknown theme: {args}\n\nAvailable themes:\n  ' + '\n  '.join(f'{k}: {v}' for k, v in THEMES.items())}


async def list_themes() -> Dict[str, Any]:
    """List available themes."""
    current = os.environ.get('CLAUDE_THEME', 'default')

    lines = ['Available themes:']
    for name, desc in THEMES.items():
        marker = ' (current)' if name == current else ''
        lines.append(f'  {name}: {desc}{marker}')

    return {'type': 'text', 'value': '\n'.join(lines)}


async def show_current_theme() -> Dict[str, Any]:
    """Show current theme."""
    theme = os.environ.get('CLAUDE_THEME', 'default')
    return {'type': 'text', 'value': f'Current theme: {theme}'}


async def set_theme(theme: str) -> Dict[str, Any]:
    """Set the theme."""
    os.environ['CLAUDE_THEME'] = theme
    return {'type': 'text', 'value': f'Switched to theme: {theme}'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'theme',
    'description': 'Manage color themes',
    'supports_non_interactive': True,
}


call = execute