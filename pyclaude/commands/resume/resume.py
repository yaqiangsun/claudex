"""Resume command - resume a previous conversation."""

import os
from typing import Any, Dict, List, Optional
from pathlib import Path


def get_sessions_dir() -> Path:
    """Get the sessions directory."""
    # Try to find .claude directory
    cwd = os.getcwd()
    claude_dir = Path(cwd) / '.claude'
    if not claude_dir.exists():
        # Try parent directories
        for parent in Path(cwd).parents:
            claude_dir = parent / '.claude'
            if claude_dir.exists():
                break
    return claude_dir / 'sessions'


def list_sessions() -> List[Dict[str, Any]]:
    """List available sessions."""
    sessions_dir = get_sessions_dir()
    sessions = []

    if not sessions_dir.exists():
        return sessions

    for session_file in sorted(sessions_dir.glob('*.jsonl'), reverse=True):
        # Parse session file to get info
        try:
            with open(session_file, 'r') as f:
                first_line = f.readline()
                if first_line:
                    import json
                    data = json.loads(first_line)
                    sessions.append({
                        'id': session_file.stem,
                        'preview': data.get('content', [{}])[0].get('text', '')[:50] if data.get('content') else '',
                        'file': str(session_file),
                    })
        except Exception:
            sessions.append({
                'id': session_file.stem,
                'preview': '',
                'file': str(session_file),
            })

    return sessions


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the resume command."""
    if not args.strip():
        # List available sessions
        sessions = list_sessions()
        if not sessions:
            return {'type': 'text', 'value': 'No previous sessions found.'}

        lines = ['Available sessions:']
        for s in sessions[:10]:
            lines.append(f"  {s['id'][:8]}... - {s['preview']}")

        return {'type': 'text', 'value': '\n'.join(lines)}

    # Resume specific session
    session_id = args.strip()
    return {
        'type': 'resume',
        'session_id': session_id,
    }


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'resume',
    'description': 'Resume a previous conversation',
    'aliases': ['continue'],
    'argument_hint': '[conversation id or search term]',
}


call = execute  # Alias for compatibility