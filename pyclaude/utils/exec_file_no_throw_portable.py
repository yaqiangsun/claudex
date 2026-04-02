"""
Exec file no throw portable utility.
"""
import subprocess
from typing import Tuple, Optional

def exec_file_no_throw(command: list, timeout: Optional[int] = None) -> Tuple[int, str, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, '', str(e)

__all__ = ['exec_file_no_throw']