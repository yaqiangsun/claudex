"""
Hooks utility.
"""
from typing import Callable, Any, List

class Hooks:
    def __init__(self):
        self._hooks: List[Callable] = []

    def register(self, hook: Callable) -> None:
        self._hooks.append(hook)

    def execute(self, *args, **kwargs) -> Any:
        for hook in self._hooks:
            hook(*args, **kwargs)

_hooks = Hooks()

def get_hooks() -> Hooks:
    return _hooks

__all__ = ['Hooks', 'get_hooks']