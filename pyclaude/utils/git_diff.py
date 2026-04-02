"""
Git diff utility.
"""
import subprocess
from typing import Optional

def get_git_diff(path: Optional[str] = None) -> str:
    cmd = ['git', 'diff']
    if path:
        cmd.append(path)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception:
        return ''

__all__ = ['get_git_diff']