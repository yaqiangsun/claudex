"""
Generic process utils utility.
"""
import os
import signal
from typing import Optional

def kill_process(pid: int, force: bool = False) -> bool:
    try:
        os.kill(pid, signal.SIGKILL if force else signal.SIGTERM)
        return True
    except Exception:
        return False

def get_process_info(pid: int) -> Optional[dict]:
    return None

__all__ = ['kill_process', 'get_process_info']