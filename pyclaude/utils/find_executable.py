"""
Find an executable by searching PATH, similar to `which`.
"""

import shutil
from typing import Dict, List


def find_executable(exe: str, args: List[str]) -> Dict[str, any]:
    """Find an executable by searching PATH.

    Returns {cmd: str, args: list} to match the spawn API shape.
    cmd is the resolved path if found, or the original name if not.
    args is always the pass-through of the input args.
    """
    resolved = shutil.which(exe)
    return {"cmd": resolved or exe, "args": args}


__all__ = ["find_executable"]