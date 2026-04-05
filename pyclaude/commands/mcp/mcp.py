"""MCP command - manage Model Context Protocol servers."""

import os
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List


MCP_DIR = Path.home() / '.claude' / 'mcp'
DEFAULT_TOOLS = ['Bash', 'Read', 'Edit', 'Write', 'Glob', 'Grep']


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the mcp command."""
    args = args.strip()
    parts = args.split()

    if not args or parts[0] == 'list':
        return await list_mcp_servers()

    if parts[0] == 'add':
        if len(parts) < 2:
            return {'type': 'text', 'value': 'Usage: /mcp add <name> <command> [args...]'}
        name = parts[1]
        command = ' '.join(parts[2:]) if len(parts) > 2 else ''
        return await add_mcp_server(name, command)

    if parts[0] == 'remove' or parts[0] == 'delete':
        if len(parts) < 2:
            return {'type': 'text', 'value': 'Usage: /mcp remove <name>'}
        name = parts[1]
        return await remove_mcp_server(name)

    if parts[0] == 'start':
        if len(parts) < 2:
            return {'type': 'text', 'value': 'Usage: /mcp start <name>'}
        name = parts[1]
        return await start_mcp_server(name)

    if parts[0] == 'stop':
        if len(parts) < 2:
            return {'type': 'text', 'value': 'Usage: /mcp stop <name>'}
        name = parts[1]
        return await stop_mcp_server(name)

    return {'type': 'text', 'value': '''Usage: /mcp [command]

Commands:
  list              - List all MCP servers
  add <name> <cmd> - Add an MCP server
  remove <name>    - Remove an MCP server
  start <name>     - Start an MCP server
  stop <name>      - Stop an MCP server
'''}


async def list_mcp_servers() -> Dict[str, Any]:
    """List all MCP servers."""
    MCP_DIR.mkdir(parents=True, exist_ok=True)

    servers = []
    for f in MCP_DIR.glob('*.json'):
        try:
            with open(f) as fp:
                data = json.load(fp)
                servers.append({
                    'name': f.stem,
                    'command': data.get('command', ''),
                    'enabled': data.get('enabled', True),
                })
        except Exception:
            pass

    if not servers:
        return {'type': 'text', 'value': 'No MCP servers configured. Use /mcp add <name> <command> to add one.'}

    lines = ['MCP Servers:']
    for s in servers:
        status = '✓' if s['enabled'] else '✗'
        lines.append(f'  {status} {s["name"]}: {s["command"]}')

    return {'type': 'text', 'value': '\n'.join(lines)}


async def add_mcp_server(name: str, command: str) -> Dict[str, Any]:
    """Add an MCP server."""
    MCP_DIR.mkdir(parents=True, exist_ok=True)

    config = {
        'command': command,
        'enabled': True,
        'timeout': 30000,
    }

    config_file = MCP_DIR / f'{name}.json'
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    return {'type': 'text', 'value': f'Added MCP server "{name}" with command: {command}'}


async def remove_mcp_server(name: str) -> Dict[str, Any]:
    """Remove an MCP server."""
    config_file = MCP_DIR / f'{name}.json'

    if not config_file.exists():
        return {'type': 'text', 'value': f'MCP server "{name}" not found.'}

    config_file.unlink()
    return {'type': 'text', 'value': f'Removed MCP server "{name}"'}


async def start_mcp_server(name: str) -> Dict[str, Any]:
    """Start an MCP server."""
    config_file = MCP_DIR / f'{name}.json'

    if not config_file.exists():
        return {'type': 'text', 'value': f'MCP server "{name}" not found.'}

    return {'type': 'text', 'value': f'Starting MCP server "{name}"... (not implemented yet)'}


async def stop_mcp_server(name: str) -> Dict[str, Any]:
    """Stop an MCP server."""
    return {'type': 'text', 'value': f'Stopping MCP server "{name}"... (not implemented yet)'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'mcp',
    'description': 'Manage Model Context Protocol servers',
    'supports_non_interactive': True,
}


call = execute