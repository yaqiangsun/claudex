"""Status command - show session status."""

import os
from typing import Any, Dict, List
from datetime import datetime


async def execute(args: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the status command."""
    from ...state import get_app_state, get_session_id
    from ...utils import get_cwd, is_darwin

    app_state = get_app_state()
    cwd = get_cwd()
    session_id = get_session_id()

    # Build status info
    lines: List[str] = [
        f"Session: {session_id[:8]}...",
        f"Working directory: {cwd}",
        f"Platform: {'macOS' if is_darwin() else 'Linux/Windows'}",
        f"Model: {app_state.main_loop_model or 'default'}",
    ]

    # Add timing info
    start_time = getattr(app_state, 'start_time', None)
    if start_time:
        elapsed = datetime.now().timestamp() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        lines.append(f"Session time: {minutes}m {seconds}s")

    return {'type': 'text', 'value': '\n'.join(lines)}


# Command metadata
CONFIG = {
    'type': 'local',
    'name': 'status',
    'description': 'Show session status',
    'supports_non_interactive': True,
}


call = execute  # Alias for compatibility