"""Compact command - clear conversation history but keep a summary."""

import os
from typing import Any, Dict, Optional

from ...services.compact import (
    compact_conversation,
    build_post_compact_messages,
    is_compact_disabled,
    ERROR_MESSAGE_NOT_ENOUGH_MESSAGES,
)


def is_enabled() -> bool:
    """Check if compact command is enabled."""
    return not is_compact_disabled()


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the compact command."""
    messages = context.get('messages', [])
    set_messages = context.get('set_messages')
    get_app_state = context.get('get_app_state')
    set_app_state = context.get('set_app_state')
    read_file_state = context.get('read_file_state', {})
    model = context.get('model')

    if len(messages) == 0:
        return {'type': 'error', 'value': ERROR_MESSAGE_NOT_ENOUGH_MESSAGES}

    custom_instructions = args.strip() if args else None

    # Build context for compaction
    tool_context = {
        'get_app_state': get_app_state,
        'set_app_state': set_app_state,
        'read_file_state': read_file_state,
        'model': model,
    }

    try:
        # Perform the compaction
        compaction_result = await compact_conversation(
            messages=messages,
            context=tool_context,
            suppress_follow_up_questions=False,
            custom_instructions=custom_instructions,
            is_auto_compact=False,
        )

        # Build the new message list
        new_messages = build_post_compact_messages(compaction_result)

        # Update messages in the REPL/context
        if set_messages:
            set_messages(lambda _: new_messages)

        # Build display text
        display_parts = ["Compacted"]

        # Add upgrade message tip if applicable
        # (simplified - full version would check for model upgrades)

        display_text = " | ".join(display_parts)

        return {
            'type': 'compact',
            'compactionResult': {
                'preCompactTokenCount': compaction_result.pre_compact_token_count,
                'postCompactTokenCount': compaction_result.post_compact_token_count,
                'truePostCompactTokenCount': compaction_result.true_post_compact_token_count,
            },
            'displayText': display_text,
        }

    except ValueError as e:
        # Handle known error messages
        error_msg = str(e)
        if ERROR_MESSAGE_NOT_ENOUGH_MESSAGES in error_msg:
            return {'type': 'error', 'value': ERROR_MESSAGE_NOT_ENOUGH_MESSAGES}
        return {'type': 'error', 'value': f'Error during compaction: {error_msg}'}
    except Exception as e:
        return {'type': 'error', 'value': f'Error during compaction: {str(e)}'}


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