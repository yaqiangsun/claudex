"""
Ink utility - TUI component utilities.
"""
from typing import Any

# Placeholder for ink-like TUI components
class Box:
    def __init__(self, children: list = None):
        self.children = children or []

class Text:
    def __init__(self, content: str):
        self.content = content

__all__ = ['Box', 'Text']