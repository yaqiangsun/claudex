"""Help command - show help and available commands."""

from typing import Any, Dict, List


# Base list of available commands (can be dynamically extended)
AVAILABLE_COMMANDS = [
    {'name': 'help', 'description': 'Show help and available commands'},
    {'name': 'clear', 'description': 'Clear screen, cache, or conversation'},
    {'name': 'compact', 'description': 'Compact conversation but keep summary'},
    {'name': 'commit', 'description': 'Create a git commit'},
    {'name': 'branch', 'description': 'Branch the conversation'},
    {'name': 'resume', 'description': 'Resume a previous conversation'},
    {'name': 'session', 'description': 'Manage sessions'},
    {'name': 'version', 'description': 'Print version info'},
    {'name': 'status', 'description': 'Show session status'},
    {'name': 'stats', 'description': 'Show session statistics'},
    {'name': 'cost', 'description': 'Show API usage and cost'},
    {'name': 'model', 'description': 'Switch between Claude models'},
    {'name': 'theme', 'description': 'Change color theme'},
    {'name': 'fast', 'description': 'Toggle fast mode'},
    {'name': 'skills', 'description': 'Manage skills'},
    {'name': 'plugins', 'description': 'Manage plugins'},
    {'name': 'config', 'description': 'Manage settings'},
    {'name': 'mcp', 'description': 'Manage MCP servers'},
    {'name': 'doctor', 'description': 'Run diagnostics'},
    {'name': 'exit', 'description': 'Exit Claude Code'},
    {'name': 'login', 'description': 'Authenticate with Claude API'},
    {'name': 'diff', 'description': 'Show git diff'},
    {'name': 'files', 'description': 'Manage files'},
]


def get_available_commands() -> List[Dict[str, Any]]:
    """Get available commands, dynamically fetching descriptions from COMMANDS registry."""
    # Try to get dynamic descriptions from COMMANDS registry
    try:
        from .. import get_command_description
        result = []
        for cmd in AVAILABLE_COMMANDS:
            name = cmd['name']
            desc = get_command_description(name) if name != 'help' else cmd['description']
            result.append({'name': name, 'description': desc})
        return result
    except Exception:
        return AVAILABLE_COMMANDS


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
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
    lines = [
        'Claude Code Commands',
        '=' * 40,
        '',
    ]

    # Get commands with dynamic descriptions
    commands = get_available_commands()

    # Group commands by category
    core = ['help', 'exit', 'clear', 'compact']
    git = ['commit', 'diff', 'branch', 'resume', 'session']
    settings = ['config', 'model', 'theme', 'fast', 'login']
    management = ['status', 'stats', 'cost', 'doctor']
    plugins = ['mcp', 'plugins', 'skills']

    def print_group(title, cmds):
        lines.append(f'{title}:')
        for c in cmds:
            for cmd in commands:
                if cmd['name'] == c:
                    lines.append(f"  /{cmd['name']} - {cmd['description']}")
        lines.append('')

    print_group('Core', core)
    print_group('Git', git)
    print_group('Settings', settings)
    print_group('Session', management)
    print_group('Plugins', plugins)

    lines.append('Type /help <command> for more info on a specific command.')

    return {'type': 'text', 'value': '\n'.join(lines)}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'help',
    'description': 'Show help and available commands',
    'aliases': ['?', 'h'],
    'supports_non_interactive': True,
}


call = execute