"""Working directory utilities."""

import contextvars
from typing import Optional
import os

# Context variable for cwd override (similar to AsyncLocalStorage)
_cwd_override: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar('cwd_override', default=None)

# Global state for cwd (will be set by state module)
_cwd: str = os.getcwd()
_original_cwd: str = os.getcwd()


def set_cwd_state(cwd: str) -> None:
    """Set the current working directory."""
    global _cwd
    _cwd = cwd


def get_cwd_state() -> str:
    """Get the current working directory."""
    return _cwd


def set_original_cwd(cwd: str) -> None:
    """Set the original working directory."""
    global _original_cwd
    _original_cwd = cwd


def get_original_cwd() -> str:
    """Get the original working directory."""
    return _original_cwd


def run_with_cwd_override(cwd: str, fn: callable):
    """Run a function with an overridden working directory."""
    token = _cwd_override.set(cwd)
    try:
        return fn()
    finally:
        _cwd_override.reset(token)


def pwd() -> str:
    """Get the current working directory (with override support)."""
    override = _cwd_override.get()
    if override is not None:
        return override
    return _cwd


def get_cwd() -> str:
    """Get the current working directory or original if current unavailable."""
    try:
        return pwd()
    except Exception:
        return _original_cwd