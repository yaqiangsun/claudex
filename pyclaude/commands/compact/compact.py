"""Compact command - clear conversation history but keep a summary."""

import os
from typing import Any, Dict, Optional


def is_enabled() -> bool:
    """Check if compact command is enabled."""
    return os.environ.get('DISABLE_COMPACT', '').lower() not in ('1', 'true', 'yes')


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the compact command."""
    messages = context.get('messages', [])
    set_messages = context.get('set_messages')
    agent_id = context.get('agent_id')

    if len(messages) == 0:
        return {'type': 'error', 'value': 'No messages to compact'}

    custom_instructions = args.strip()

    # Placeholder: full implementation requires compact service
    # This is a simplified version that just clears old messages

    # Keep the last few messages as summary context
    keep_count = min(4, len(messages))
    kept_messages = messages[-keep_count:]

    # Update messages
    if set_messages:
        set_messages(lambda _: kept_messages)

    return {
        'type': 'compact',
        'displayText': 'Conversation has been compacted',
    }


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'compact',
    'description': 'Clear conversation history but keep a summary in context',
    'is_enabled': is_enabled,
    'supports_non_interactive': True,
    'argument_hint': '<optional custom summarization instructions>',
}


call = execute  # Alias for compatibility