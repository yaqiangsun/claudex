"""Clear command - clears the conversation."""

from typing import Any, Dict


async def clear_conversation(context: Dict[str, Any]) -> Dict[str, str]:
    """Clear the conversation and reset session state."""
    # Get context functions
    set_messages = context.get('set_messages')
    set_app_state = context.get('set_app_state')
    set_conversation_id = context.get('set_conversation_id')

    # Clear messages
    if set_messages:
        set_messages(lambda _: [])

    # Reset conversation ID
    if set_conversation_id:
        import uuid
        set_conversation_id(str(uuid.uuid4()))

    # Reset app state
    if set_app_state:
        def reset_state(state):
            state.messages = []
            state.conversation_id = None
            return state
        set_app_state(reset_state)

    return {'type': 'text', 'value': ''}


async def execute(context: Dict[str, Any]) -> Dict[str, str]:
    """Execute the clear command."""
    return await clear_conversation(context)