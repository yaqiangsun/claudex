"""Stats command - show session statistics."""

import os
from typing import Any, Dict
from datetime import datetime


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the stats command."""
    args = args.strip().lower() if args else ''

    if args == 'reset':
        return await reset_stats()

    return await show_stats()


async def show_stats() -> Dict[str, Any]:
    """Show session statistics."""
    from ...bootstrap import get_bootstrap_state

    bootstrap = get_bootstrap_state()

    # Calculate elapsed time
    elapsed = datetime.now().timestamp() - bootstrap.start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)

    lines = [
        'Session Statistics',
        '=' * 40,
        f'Session time: {minutes}m {seconds}s',
        f'Total cost: ${bootstrap.total_cost_usd:.4f}',
        f'API duration: {bootstrap.total_api_duration/1000:.1f}s',
        f'Tool duration: {bootstrap.total_tool_duration/1000:.1f}s',
        f'Turns: {bootstrap.turn_tool_count} tool calls',
        f'Lines added: {bootstrap.total_lines_added}',
        f'Lines removed: {bootstrap.total_lines_removed}',
    ]

    return {'type': 'text', 'value': '\n'.join(lines)}


async def reset_stats() -> Dict[str, Any]:
    """Reset statistics."""
    from ...bootstrap import get_bootstrap_state

    bootstrap = get_bootstrap_state()

    bootstrap.total_cost_usd = 0
    bootstrap.total_api_duration = 0
    bootstrap.total_tool_duration = 0
    bootstrap.total_lines_added = 0
    bootstrap.total_lines_removed = 0

    return {'type': 'text', 'value': 'Statistics reset.'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'stats',
    'description': 'Show session statistics',
    'aliases': ['statistics'],
    'supports_non_interactive': True,
}


call = execute