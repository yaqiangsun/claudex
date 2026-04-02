"""
Editor utility.
"""
import os
from typing import Optional

def get_editor() -> str:
    return os.environ.get('EDITOR', 'vim')

def get_editor_args() -> list:
    return []

__all__ = ['get_editor', 'get_editor_args']