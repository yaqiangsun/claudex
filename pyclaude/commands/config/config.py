"""Config command - manage Claude Code settings."""

import os
import json
from pathlib import Path
from typing import Any, Dict


SETTINGS_FILE = Path.home() / '.claude' / 'settings.json'


def get_settings() -> Dict[str, Any]:
    """Load settings from file."""
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_settings(settings: Dict[str, Any]) -> None:
    """Save settings to file."""
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the config command."""
    args = args.strip()

    if not args:
        # Show all settings
        settings = get_settings()
        if not settings:
            return {'type': 'text', 'value': 'No settings found. Use /config set <key> <value> to set a value.'}

        lines = ['Current settings:']
        for key, value in settings.items():
            if isinstance(value, dict):
                lines.append(f'{key}:')
                for k, v in value.items():
                    lines.append(f'  {k}: {v}')
            else:
                lines.append(f'{key}: {value}')

        return {'type': 'text', 'value': '\n'.join(lines)}

    # Parse arguments
    parts = args.split()
    if len(parts) == 1:
        # Show single setting
        key = parts[0]
        settings = get_settings()
        value = settings.get(key)
        if value is None:
            return {'type': 'text', 'value': f'Setting "{key}" not found.'}
        return {'type': 'text', 'value': f'{key}: {json.dumps(value, indent=2)}'}

    if len(parts) >= 2 and parts[0] == 'set':
        # Set a value
        key = parts[1]
        value = ' '.join(parts[2:]) if len(parts) > 2 else ''

        # Try to parse as JSON
        try:
            value = json.loads(value) if value else ''
        except json.JSONDecodeError:
            pass  # Keep as string

        settings = get_settings()
        settings[key] = value
        save_settings(settings)

        return {'type': 'text', 'value': f'Set {key} = {json.dumps(value)}'}

    if len(parts) >= 2 and parts[0] == 'get':
        # Get a value
        key = parts[1]
        settings = get_settings()
        value = settings.get(key)
        if value is None:
            return {'type': 'text', 'value': f'Setting "{key}" not found.'}
        return {'type': 'text', 'value': json.dumps(value, indent=2)}

    if len(parts) >= 2 and parts[0] == 'delete':
        # Delete a value
        key = parts[1]
        settings = get_settings()
        if key in settings:
            del settings[key]
            save_settings(settings)
            return {'type': 'text', 'value': f'Deleted setting "{key}"'}
        return {'type': 'text', 'value': f'Setting "{key}" not found.'}

    return {'type': 'text', 'value': 'Usage: /config [key] | /config set <key> <value> | /config get <key> | /config delete <key>'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'config',
    'description': 'Manage Claude Code settings',
    'aliases': ['settings'],
    'supports_non_interactive': True,
}


call = execute