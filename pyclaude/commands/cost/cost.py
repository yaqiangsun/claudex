"""Cost command - show API usage and cost."""

import os
from typing import Any, Dict
from datetime import datetime


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the cost command."""
    args = args.strip().lower() if args else ''

    if args == 'reset':
        return await reset_cost()

    return await show_cost()


async def show_cost() -> Dict[str, Any]:
    """Show current cost."""
    from ...state import get_state
    from ...bootstrap import get_bootstrap_state

    state = get_state()
    bootstrap = get_bootstrap_state()

    # Get usage from state
    total_cost = getattr(state, 'total_cost_usd', 0) or bootstrap.total_cost_usd
    total_input = getattr(state, 'total_input_tokens', 0)
    total_output = getattr(state, 'total_output_tokens', 0)
    total_api_duration = getattr(state, 'total_api_duration', 0) or bootstrap.total_api_duration

    lines = [
        'API Usage',
        '=' * 40,
        f'Total cost: ${total_cost:.4f}',
        f'Input tokens: {total_input:,}',
        f'Output tokens: {total_output:,}',
        f'API duration: {total_api_duration/1000:.1f}s',
    ]

    return {'type': 'text', 'value': '\n'.join(lines)}


async def reset_cost() -> Dict[str, Any]:
    """Reset cost counters."""
    from ...state import get_state
    from ...bootstrap import get_bootstrap_state

    state = get_state()
    bootstrap = get_bootstrap_state()

    # Reset counters
    state.total_cost_usd = 0
    state.total_input_tokens = 0
    state.total_output_tokens = 0
    bootstrap.total_cost_usd = 0

    return {'type': 'text', 'value': 'Cost counters reset.'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'cost',
    'description': 'Show API usage and cost',
    'aliases': ['usage', 'credits'],
    'supports_non_interactive': True,
}


call = execute