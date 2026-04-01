"""Help command - show help and available commands."""

from typing import Any, Dict, List


# List of available commands
AVAILABLE_COMMANDS = [
    {'name': 'help', 'description': 'Show help and available commands'},
    {'name': 'clear', 'description': 'Clear conversation history'},
    {'name': 'compact', 'description': 'Compact conversation but keep summary'},
    {'name': 'commit', 'description': 'Create a git commit'},
    {'name': 'resume', 'description': 'Resume a previous conversation'},
    {'name': 'version', 'description': 'Print version info'},
    {'name': 'status', 'description': 'Show session status'},
    {'name': 'tasks', 'description': 'List running tasks'},
    {'name': 'skills', 'description': 'Manage skills'},
    {'name': 'config', 'description': 'Open config panel'},
    {'name': 'mcp', 'description': 'Manage MCP servers'},
    {'name': 'doctor', 'description': 'Run diagnostics'},
]


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, str]:
    """Execute the help command."""
    if args.strip():
        # Show help for specific command
        cmd = args.strip().lstrip('/')
        for command in AVAILABLE_COMMANDS:
            if command['name'] == cmd:
                return {
                    'type': 'text',
                    'value': f"/{command['name']} - {command['description']}",
                }
        return {
            'type': 'text',
            'value': f"Unknown command: /{cmd}",
        }

    # Show general help
    lines = ['Available commands:', '']
    for cmd in AVAILABLE_COMMANDS:
        lines.append(f"  /{cmd['name']} - {cmd['description']}")
    lines.append('')
    lines.append('Type /help <command> for more info on a specific command.')

    return {'type': 'text', 'value': '\n'.join(lines)}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'help',
    'description': 'Show help and available commands',
}


call = execute  # Alias for compatibility