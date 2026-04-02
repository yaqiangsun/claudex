"""
Shell config utilities.

Shell configuration handling.
"""

import os
from typing import Dict, List


def get_shell_config_paths() -> Dict[str, str]:
    """Get shell config file paths."""
    home = os.path.expanduser("~")
    return {
        "bash": os.path.join(home, ".bashrc"),
        "zsh": os.path.join(home, ".zshrc"),
    }


def read_file_lines(path: str) -> List[str]:
    """Read file as lines."""
    try:
        with open(path) as f:
            return f.readlines()
    except Exception:
        return []


__all__ = [
    "get_shell_config_paths",
    "read_file_lines",
]