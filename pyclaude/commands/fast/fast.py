"""Fast mode command - toggle fast mode."""

import os
from typing import Any, Dict


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the fast command."""
    args = args.strip().lower() if args else ''

    if args == 'on' or args == 'enable':
        os.environ['CLAUDE_FAST_MODE'] = 'true'
        return {'type': 'text', 'value': 'Fast mode enabled. Uses Haiku model for faster responses.'}

    if args == 'off' or args == 'disable':
        if 'CLAUDE_FAST_MODE' in os.environ:
            del os.environ['CLAUDE_FAST_MODE']
        return {'type': 'text', 'value': 'Fast mode disabled.'}

    if args == 'status':
        is_fast = os.environ.get('CLAUDE_FAST_MODE') == 'true'
        return {'type': 'text', 'value': f'Fast mode: {"enabled" if is_fast else "disabled"}'}

    # Toggle
    is_fast = os.environ.get('CLAUDE_FAST_MODE') == 'true'
    if is_fast:
        del os.environ['CLAUDE_FAST_MODE']
        return {'type': 'text', 'value': 'Fast mode disabled.'}
    else:
        os.environ['CLAUDE_FAST_MODE'] = 'true'
        return {'type': 'text', 'value': 'Fast mode enabled.'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'fast',
    'description': 'Toggle fast mode (uses faster model)',
    'aliases': ['quick'],
    'supports_non_interactive': True,
}


call = execute