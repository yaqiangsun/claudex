"""
Subprocess environment utility.
"""
import os
from typing import Dict

def get_subprocess_env() -> Dict[str, str]:
    env = os.environ.copy()
    env['CLAUDECODE'] = '1'
    return env

def subprocess_env() -> Dict[str, str]:
    return get_subprocess_env()

__all__ = ['get_subprocess_env', 'subprocess_env']