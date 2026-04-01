"""
Agent context for analytics attribution using contextvars.

This module provides a way to track agent identity across async operations
without parameter drilling. Supports two agent types:

1. Subagents (Agent tool): Run in-process for quick, delegated tasks.
   Context: SubagentContext with agent_type: 'subagent'

2. In-process teammates: Part of a swarm with team coordination.
   Context: TeammateAgentContext with agent_type: 'teammate'
"""

from contextvars import ContextVar
from typing import Optional, Dict, Any, Callable, TypeVar
from dataclasses import dataclass, field


T = TypeVar('T')


@dataclass
class SubagentContext:
    """Context for subagents (Agent tool agents)."""
    agent_id: str
    parent_session_id: Optional[str] = None
    agent_type: str = 'subagent'
    subagent_name: Optional[str] = None
    is_built_in: bool = False
    invoking_request_id: Optional[str] = None
    invocation_kind: Optional[str] = None
    invocation_emitted: bool = False


@dataclass
class TeammateAgentContext:
    """Context for in-process teammates."""
    agent_id: str
    agent_name: str
    team_name: str
    parent_session_id: str
    is_team_lead: bool
    agent_type: str = 'teammate'
    agent_color: Optional[str] = None
    plan_mode_required: bool = False
    invoking_request_id: Optional[str] = None
    invocation_kind: Optional[str] = None
    invocation_emitted: bool = False


# Type alias for any agent context
AgentContext = SubagentAgentContext | TeammateAgentContext


# Use contextvars for async-safe context storage
_agent_context_storage: ContextVar[Optional[AgentContext]] = ContextVar(
    'agent_context',
    default=None
)


def get_agent_context() -> Optional[AgentContext]:
    """Get the current agent context, if any.

    Returns None if not running within an agent context.
    """
    return _agent_context_storage.get()


def run_with_agent_context(context: AgentContext, fn: Callable[..., T], *args, **kwargs) -> T:
    """Run an async function with the given agent context.

    All async operations within the function will have access to this context.
    """
    token = _agent_context_storage.set(context)
    try:
        return fn(*args, **kwargs)
    finally:
        _agent_context_storage.reset(token)


def is_subagent_context(context: Optional[AgentContext]) -> bool:
    """Type guard to check if context is a SubagentContext."""
    if context is None:
        return False
    return isinstance(context, SubagentContext)


def is_teammate_agent_context(context: Optional[AgentContext]) -> bool:
    """Type guard to check if context is a TeammateAgentContext."""
    if context is None:
        return False
    from .agent_swarms_enabled import is_agent_swarms_enabled

    if is_agent_swarms_enabled():
        return isinstance(context, TeammateAgentContext)
    return False


def get_subagent_log_name() -> Optional[str]:
    """Get the subagent name suitable for analytics logging.

    Returns the agent type name for built-in agents, "user-defined" for custom agents,
    or None if not running within a subagent context.
    """
    context = get_agent_context()
    if not is_subagent_context(context) or not context.subagent_name:
        return None

    return context.subagent_name if context.is_built_in else "user-defined"


def consume_invoking_request_id() -> Optional[Dict[str, Any]]:
    """Get the invoking request_id for the current agent context — once per invocation.

    Returns the id on the first call after a spawn/resume, then None until the next boundary.
    Also None on the main thread or when the spawn path had no request_id.
    """
    context = get_agent_context()
    if not context or not context.invoking_request_id or context.invocation_emitted:
        return None

    context.invocation_emitted = True
    return {
        "invoking_request_id": context.invoking_request_id,
        "invocation_kind": context.invocation_kind,
    }


# Alias for backwards compatibility
SubagentAgentContext = SubagentContext


__all__ = [
    "SubagentContext",
    "TeammateAgentContext",
    "AgentContext",
    "get_agent_context",
    "run_with_agent_context",
    "is_subagent_context",
    "is_teammate_agent_context",
    "get_subagent_log_name",
    "consume_invoking_request_id",
]