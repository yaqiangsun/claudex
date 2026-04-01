"""Btw command - add a side note to the conversation."""

from typing import Any, Dict


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the btw command - adds a side note."""
    if not args.strip():
        return {'type': 'error', 'value': 'Usage: /btw <message>'}

    # Add as user message with special formatting
    return {
        'type': 'user_message',
        'content': f"[btw] {args.strip()}",
    }


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'btw',
    'description': 'Add a side note to the conversation',
    'argument_hint': '<message>',
}


call = execute  # Alias for compatibility