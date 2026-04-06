"""
List sessions implementation utilities.

List sessions implementation.
"""

import os
from typing import List, Dict, Any, Optional


def list_sessions_impl(directory: Optional[str] = None) -> List[Dict[str, Any]]:
    """List sessions from directory with metadata."""
    if directory is None:
        directory = os.path.expanduser("~/.claude/projects")

    sessions = []
    if os.path.exists(directory):
        for entry in os.listdir(directory):
            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                # Try to get session metadata
                custom_title = None
                first_prompt = None
                modified = None

                # Check for session.json metadata
                session_json = os.path.join(path, 'session.json')
                if os.path.exists(session_json):
                    import json
                    try:
                        with open(session_json) as f:
                            data = json.load(f)
                            custom_title = data.get('customTitle')
                            first_prompt = data.get('firstPrompt')
                            modified = data.get('modified')
                    except Exception:
                        pass

                # Get modification time if not in metadata
                if not modified:
                    try:
                        modified = str(os.path.getmtime(path))
                    except Exception:
                        modified = ""

                sessions.append({
                    "id": entry,
                    "path": path,
                    "customTitle": custom_title,
                    "firstPrompt": first_prompt,
                    "modified": modified,
                })

    # Sort by modified time (most recent first)
    sessions.sort(key=lambda x: x.get('modified', ''), reverse=True)

    return sessions


__all__ = ["list_sessions_impl"]