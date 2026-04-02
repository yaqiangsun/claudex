"""
Graceful shutdown utilities.

Handle graceful shutdown.
"""

import signal
import sys
from typing import Callable, List


_shutdown_handlers: List[Callable] = []


def register_shutdown_handler(handler: Callable) -> None:
    """Register shutdown handler."""
    _shutdown_handlers.append(handler)


def graceful_shutdown(exit_code: int = 0) -> None:
    """Perform graceful shutdown."""
    for handler in _shutdown_handlers:
        try:
            handler()
        except Exception:
            pass
    sys.exit(exit_code)


def graceful_shutdown_sync(exit_code: int = 0) -> None:
    """Synchronous graceful shutdown."""
    graceful_shutdown(exit_code)


__all__ = [
    "register_shutdown_handler",
    "graceful_shutdown",
    "graceful_shutdown_sync",
]