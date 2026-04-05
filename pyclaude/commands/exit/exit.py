"""Exit command - exit Claude Code."""

import sys
from typing import Any, Dict


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the exit command."""
    args = args.strip().lower() if args else ''

    if args == 'force' or args == '-f':
        # Force exit without saving
        sys.exit(0)

    # Try to save state first
    try:
        from ...history import get_history
        history = get_history()
        if history.count() > 0:
            # Would save session here
            pass
    except Exception:
        pass

    return {'type': 'exit', 'value': 'Goodbye!'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'exit',
    'description': 'Exit Claude Code',
    'aliases': ['quit', 'q', 'logout'],
    'supports_non_interactive': True,
}


call = execute