"""Session command - manage conversation sessions."""

import os
import json
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime


SESSIONS_DIR = Path.home() / '.claude' / 'sessions'


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the session command."""
    args = args.strip().lower() if args else ''

    if not args or args == 'list':
        return await list_sessions()

    if args == 'current':
        return await show_current_session()

    if args == 'save':
        return await save_session()

    if args.startswith('load '):
        session_id = args[5:].strip()
        return await load_session(session_id)

    if args.startswith('delete '):
        session_id = args[7:].strip()
        return await delete_session(session_id)

    return {'type': 'text', 'value': '''Usage: /session [command]

Commands:
  list              - List all sessions
  current           - Show current session info
  save              - Save current session
  load <id>         - Load a session by ID
  delete <id>       - Delete a session
'''}


async def list_sessions() -> Dict[str, Any]:
    """List all sessions."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    sessions = []
    for f in SESSIONS_DIR.glob('*.json'):
        try:
            with open(f) as fp:
                data = json.load(fp)
                sessions.append({
                    'id': f.stem,
                    'name': data.get('name', 'Unnamed'),
                    'created': data.get('created_at', ''),
                    'message_count': len(data.get('messages', [])),
                })
        except Exception:
            pass

    if not sessions:
        return {'type': 'text', 'value': 'No saved sessions. Use /session save to save the current session.'}

    lines = ['Sessions:']
    for s in sessions:
        lines.append(f"  {s['id'][:8]}... - {s['name']} ({s['message_count']} messages)")

    return {'type': 'text', 'value': '\n'.join(lines)}


async def show_current_session() -> Dict[str, Any]:
    """Show current session info."""
    from ...bootstrap import get_session_id, get_cwd

    session_id = get_session_id()
    cwd = get_cwd()

    lines = [
        f'Session ID: {session_id}',
        f'Working directory: {cwd}',
    ]

    return {'type': 'text', 'value': '\n'.join(lines)}


async def save_session() -> Dict[str, Any]:
    """Save current session."""
    from ...history import get_history
    from ...bootstrap import get_session_id

    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    session_id = get_session_id()
    history = get_history()

    session_data = {
        'id': session_id,
        'created_at': datetime.now().isoformat(),
        'messages': [
            {'role': m.role, 'content': m.content}
            for m in history.get_messages()
        ],
    }

    session_file = SESSIONS_DIR / f'{session_id}.json'
    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2)

    return {'type': 'text', 'value': f'Session saved: {session_id[:8]}...'}


async def load_session(session_id: str) -> Dict[str, Any]:
    """Load a session."""
    session_file = SESSIONS_DIR / f'{session_id}.json'

    if not session_file.exists():
        # Try with prefix
        matches = list(SESSIONS_DIR.glob(f'{session_id}*.json'))
        if matches:
            session_file = matches[0]
        else:
            return {'type': 'text', 'value': f'Session "{session_id}" not found.'}

    with open(session_file) as f:
        session_data = json.load(f)

    # Load messages into history
    from ...history import get_history
    history = get_history()
    history.clear()

    for msg in session_data.get('messages', []):
        history.add_message(msg['role'], msg['content'])

    return {'type': 'text', 'value': f'Loaded session: {session_data.get("name", session_id)}'}


async def delete_session(session_id: str) -> Dict[str, Any]:
    """Delete a session."""
    session_file = SESSIONS_DIR / f'{session_id}.json'

    if not session_file.exists():
        return {'type': 'text', 'value': f'Session "{session_id}" not found.'}

    session_file.unlink()
    return {'type': 'text', 'value': f'Deleted session: {session_id[:8]}...'}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'session',
    'description': 'Manage conversation sessions',
    'supports_non_interactive': True,
}


call = execute