"""
Git utility.
"""
from typing import Optional, Dict, Any

def get_git_root() -> Optional[str]:
    import subprocess
    try:
        result = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None

def is_git_repo() -> bool:
    return get_git_root() is not None

__all__ = ['get_git_root', 'is_git_repo']