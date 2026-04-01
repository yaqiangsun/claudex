"""Query configuration."""

import os
from dataclasses import dataclass
from typing import Optional

from ..state import get_session_id


@dataclass
class QueryConfigGates:
    """Runtime gates (env/statsig)."""
    streaming_tool_execution: bool
    emit_tool_use_summaries: bool
    is_ant: bool
    fast_mode_enabled: bool


@dataclass
class QueryConfig:
    """Immutable values snapshotted once at query() entry."""
    session_id: str
    gates: QueryConfigGates


def is_env_truthy(value: Optional[str]) -> bool:
    """Check if env value is truthy."""
    return value is not None and value.lower() in ('1', 'true', 'yes')


def build_query_config() -> QueryConfig:
    """Build query configuration from current environment."""
    return QueryConfig(
        session_id=get_session_id(),
        gates=QueryConfigGates(
            # TODO: Add statsig feature gate check
            streaming_tool_execution=False,
            emit_tool_use_summaries=is_env_truthy(
                os.environ.get('CLAUDE_CODE_EMIT_TOOL_USE_SUMMARIES')
            ),
            is_ant=os.environ.get('USER_TYPE') == 'ant',
            fast_mode_enabled=not is_env_truthy(
                os.environ.get('CLAUDE_CODE_DISABLE_FAST_MODE')
            ),
        ),
    )