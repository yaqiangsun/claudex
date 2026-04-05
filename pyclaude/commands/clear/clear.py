"""Clear command - clear screen, cache, or conversation."""

import os
import shutil
from pathlib import Path
from typing import Any, Dict


CLAUDE_DIR = Path.home() / '.claude'


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the clear command."""
    args = args.strip().lower() if args else ''

    if not args or args == 'screen':
        # Clear the terminal screen
        os.system('clear' if os.name != 'nt' else 'cls')
        return {'type': 'skip', 'value': ''}

    if args == 'cache' or args == 'caches':
        return await clear_caches()

    if args == 'conversation' or args == 'history':
        return await clear_conversation(context)

    if args == 'all':
        result1 = await clear_caches()
        result2 = await clear_conversation(context)
        return {'type': 'text', 'value': result1['value'] + '\n' + result2['value']}

    return {'type': 'text', 'value': '''Usage: /clear [what]

Options:
  screen        - Clear the terminal screen
  cache/caches  - Clear cached data
  conversation - Clear conversation history
  all           - Clear everything
'''}


async def clear_caches() -> Dict[str, Any]:
    """Clear caches."""
    cleared = []

    # Clear file read cache
    read_cache_dir = CLAUDE_DIR / 'cache' / 'file_read'
    if read_cache_dir.exists():
        shutil.rmtree(read_cache_dir)
        cleared.append('file read cache')

    # Clear MCP cache
    mcp_cache_dir = CLAUDE_DIR / 'cache' / 'mcp'
    if mcp_cache_dir.exists():
        shutil.rmtree(mcp_cache_dir)
        cleared.append('MCP cache')

    # Clear image cache
    image_cache_dir = CLAUDE_DIR / 'cache' / 'images'
    if image_cache_dir.exists():
        shutil.rmtree(image_cache_dir)
        cleared.append('image cache')

    if not cleared:
        return {'type': 'text', 'value': 'No caches to clear.'}

    return {'type': 'text', 'value': f'Cleared: {", ".join(cleared)}'}


async def clear_conversation(context: Dict[str, Any]) -> Dict[str, Any]:
    """Clear conversation history."""
    # Get context functions
    set_messages = context.get('set_messages')

    # Clear messages
    if set_messages:
        set_messages(lambda _: [])

    # Reset conversation ID if available
    set_conversation_id = context.get('set_conversation_id')
    if set_conversation_id:
        import uuid
        set_conversation_id(str(uuid.uuid4()))

    # Reset turn stats if available
    reset_turn_stats = context.get('reset_turn_stats')
    if reset_turn_stats:
        reset_turn_stats()

    return {'type': 'text', 'value': 'Conversation cleared.'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'clear',
    'description': 'Clear screen, cache, or conversation',
    'aliases': ['cls'],
    'supports_non_interactive': True,
}


call = execute