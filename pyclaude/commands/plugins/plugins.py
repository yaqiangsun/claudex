"""Plugins command - manage plugins."""

import os
import json
from pathlib import Path
from typing import Any, Dict, List


PLUGINS_DIR = Path.home() / '.claude' / 'plugins'


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the plugins command."""
    args = args.strip().lower() if args else ''

    if not args or args == 'list':
        return await list_plugins()

    if args == 'installed':
        return await list_installed_plugins()

    if args.startswith('enable '):
        plugin_name = args[7:].strip()
        return await enable_plugin(plugin_name)

    if args.startswith('disable '):
        plugin_name = args[8:].strip()
        return await disable_plugin(plugin_name)

    if args.startswith('search '):
        query = args[7:].strip()
        return await search_plugins(query)

    return {'type': 'text', 'value': '''Usage: /plugins [command]

Commands:
  list              - List available plugins
  installed         - List installed plugins
  enable <name>     - Enable a plugin
  disable <name>    - Disable a plugin
  search <query>    - Search for plugins
'''}


async def list_plugins() -> Dict[str, Any]:
    """List available plugins."""
    PLUGINS_DIR.mkdir(parents=True, exist_ok=True)

    plugins = []
    for f in PLUGINS_DIR.glob('*.json'):
        try:
            with open(f) as fp:
                data = json.load(fp)
                plugins.append({
                    'name': f.stem,
                    'enabled': data.get('enabled', True),
                    'version': data.get('version', 'unknown'),
                })
        except Exception:
            pass

    if not plugins:
        return {'type': 'text', 'value': 'No plugins configured.'}

    lines = ['Installed plugins:']
    for p in plugins:
        status = '✓' if p['enabled'] else '✗'
        lines.append(f'  {status} {p["name"]} (v{p["version"]})')

    return {'type': 'text', 'value': '\n'.join(lines)}


async def list_installed_plugins() -> Dict[str, Any]:
    """List installed plugins."""
    return await list_plugins()


async def enable_plugin(name: str) -> Dict[str, Any]:
    """Enable a plugin."""
    plugin_file = PLUGINS_DIR / f'{name}.json'

    if not plugin_file.exists():
        return {'type': 'text', 'value': f'Plugin "{name}" not found.'}

    with open(plugin_file) as f:
        data = json.load(f)

    data['enabled'] = True

    with open(plugin_file, 'w') as f:
        json.dump(data, f, indent=2)

    return {'type': 'text', 'value': f'Enabled plugin: {name}'}


async def disable_plugin(name: str) -> Dict[str, Any]:
    """Disable a plugin."""
    plugin_file = PLUGINS_DIR / f'{name}.json'

    if not plugin_file.exists():
        return {'type': 'text', 'value': f'Plugin "{name}" not found.'}

    with open(plugin_file) as f:
        data = json.load(f)

    data['enabled'] = False

    with open(plugin_file, 'w') as f:
        json.dump(data, f, indent=2)

    return {'type': 'text', 'value': f'Disabled plugin: {name}'}


async def search_plugins(query: str) -> Dict[str, Any]:
    """Search for plugins."""
    return {'type': 'text', 'value': f'Searching for plugins matching "{query}"... (not implemented)'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'plugins',
    'description': 'Manage plugins',
    'supports_non_interactive': True,
}


call = execute