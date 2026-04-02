"""
Claude.md utility.

Claude.md file handling.
"""

import os
from typing import Optional


def get_claude_md_path() -> Optional[str]:
    """Get claude.md file path."""
    return os.environ.get('CLAUDE_CODE_CLAUDE_MD_PATH')


def find_claude_md(start_dir: str = '.') -> Optional[str]:
    """Find claude.md file in directory tree."""
    import os
    current = start_dir
    while True:
        md_path = os.path.join(current, 'CLAUDE.md')
        if os.path.exists(md_path):
            return md_path
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None


__all__ = ['get_claude_md_path', 'find_claude_md']