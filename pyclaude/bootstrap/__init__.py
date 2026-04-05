"""Bootstrap module - initializes application state and settings.

Python adaptation of the TypeScript bootstrap/state.ts
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class BootstrapState:
    """Bootstrap state - initialized once at startup."""
    # Working directories
    original_cwd: str = ''
    project_root: str = ''
    cwd: str = ''

    # Cost tracking
    total_cost_usd: float = 0.0
    total_api_duration: float = 0.0
    total_api_duration_without_retries: float = 0.0
    total_tool_duration: float = 0.0

    # Turn statistics
    turn_hook_duration_ms: float = 0.0
    turn_tool_duration_ms: float = 0.0
    turn_classifier_duration_ms: float = 0.0
    turn_tool_count: int = 0
    turn_hook_count: int = 0
    turn_classifier_count: int = 0

    # Lines tracking
    total_lines_added: int = 0
    total_lines_removed: int = 0

    # Time tracking
    start_time: float = 0.0
    last_interaction_time: float = 0.0

    # Model
    main_loop_model_override: Optional[str] = None
    initial_main_loop_model: Optional[str] = None

    # Flags
    is_interactive: bool = True
    has_unknown_model_cost: bool = False

    # Session
    session_id: str = ''

    # User settings
    flag_settings_path: Optional[str] = None
    flag_settings_inline: Optional[Dict[str, Any]] = None


# Global bootstrap state
_bootstrap_state: Optional[BootstrapState] = None
_initialized: bool = False


def initialize_state(cwd: Optional[str] = None) -> BootstrapState:
    """Initialize bootstrap state."""
    global _bootstrap_state, _initialized

    if _bootstrap_state is not None:
        return _bootstrap_state

    working_dir = cwd or os.getcwd()

    _bootstrap_state = BootstrapState(
        original_cwd=working_dir,
        project_root=working_dir,
        cwd=working_dir,
        start_time=datetime.now().timestamp(),
        last_interaction_time=datetime.now().timestamp(),
        session_id=str(uuid.uuid4()),
        is_interactive=os.isatty(0) if hasattr(os, 'isatty') else False,
    )
    _initialized = True

    return _bootstrap_state


def is_initialized() -> bool:
    """Check if bootstrap state is initialized."""
    return _initialized


def get_bootstrap_state() -> BootstrapState:
    """Get bootstrap state, initializing if needed."""
    global _bootstrap_state

    if _bootstrap_state is None:
        initialize_state()

    return _bootstrap_state


def get_original_cwd() -> str:
    """Get original working directory."""
    return get_bootstrap_state().original_cwd


def get_project_root() -> str:
    """Get project root directory."""
    return get_bootstrap_state().project_root


def get_cwd() -> str:
    """Get current working directory."""
    state = get_bootstrap_state()
    return state.cwd or state.original_cwd


def get_session_id() -> str:
    """Get session ID."""
    return get_bootstrap_state().session_id


def set_cwd(new_cwd: str) -> None:
    """Set current working directory."""
    state = get_bootstrap_state()
    state.cwd = new_cwd


def update_cost(cost_delta: float) -> None:
    """Update total cost."""
    state = get_bootstrap_state()
    state.total_cost_usd += cost_delta


def update_tool_duration(duration_ms: float) -> None:
    """Update tool duration."""
    state = get_bootstrap_state()
    state.total_tool_duration += duration_ms
    state.turn_tool_duration_ms += duration_ms


def update_api_duration(duration_ms: float, without_retries: bool = False) -> None:
    """Update API duration."""
    state = get_bootstrap_state()
    state.total_api_duration += duration_ms
    if without_retries:
        state.total_api_duration_without_retries += duration_ms


def update_lines(added: int = 0, removed: int = 0) -> None:
    """Update lines added/removed."""
    state = get_bootstrap_state()
    state.total_lines_added += added
    state.total_lines_removed += removed


def reset_turn_stats() -> None:
    """Reset turn-level statistics."""
    state = get_bootstrap_state()
    state.turn_hook_duration_ms = 0.0
    state.turn_tool_duration_ms = 0.0
    state.turn_classifier_duration_ms = 0.0
    state.turn_tool_count = 0
    state.turn_hook_count = 0
    state.turn_classifier_count = 0


def is_interactive() -> bool:
    """Check if running in interactive mode."""
    return get_bootstrap_state().is_interactive


def is_session_persistence_disabled() -> bool:
    """Check if session persistence is disabled."""
    return os.environ.get('CLAUDE_DISABLE_PERSISTENCE') == 'true'


# Keep backwards compatibility - export get_cwd as a function too
def _get_cwd_compat() -> str:
    """Compatibility function for get_cwd."""
    return get_cwd()


__all__ = [
    'BootstrapState',
    'initialize_state',
    'is_initialized',
    'get_bootstrap_state',
    'get_original_cwd',
    'get_project_root',
    'get_cwd',
    'get_session_id',
    'set_cwd',
    'update_cost',
    'update_tool_duration',
    'update_api_duration',
    'update_lines',
    'reset_turn_stats',
    'is_interactive',
    'is_session_persistence_disabled',
]