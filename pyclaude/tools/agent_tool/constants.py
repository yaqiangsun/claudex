"""Constants for AgentTool matching src/tools/AgentTool/constants.ts"""
from enum import Enum


class AgentStatus(str, Enum):
    """Agent execution status."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentEventType(str, Enum):
    """Agent event types."""
    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"
    MESSAGE = "message"
    ERROR = "error"
    TOOL_USE = "tool_use"
    TOOL_RESULT = "tool_result"


DEFAULT_AGENT_TIMEOUT = 300  # 5 minutes
MAX_AGENT_ITERATIONS = 100
AGENT_PROMPT_TEMPLATE = "You are an agent running in the Claude Code environment."


__all__ = [
    "AgentStatus",
    "AgentEventType",
    "DEFAULT_AGENT_TIMEOUT",
    "MAX_AGENT_ITERATIONS",
    "AGENT_PROMPT_TEMPLATE",
]