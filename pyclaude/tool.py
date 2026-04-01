"""
Tool definitions and interfaces.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Protocol, runtime_checkable, Union, Optional


class ToolType(str, Enum):
    """Types of tools."""
    BASH = 'bash'
    EDIT = 'edit'
    READ = 'read'
    AGENT = 'agent'
    TOOL = 'tool'
    MCP = 'mcp'
    WEBSEARCH = 'websearch'
    REPL = 'repl'
    SKILL = 'skill'
    COMPACT = 'compact'
    EXIT = 'exit'


class ToolStatus(str, Enum):
    """Tool execution status."""
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    ERROR = 'error'
    DENIED = 'denied'


@dataclass
class ToolInputSchema:
    """JSON Schema for tool input."""
    type: str = 'object'
    properties: dict[str, Any] = None
    required: list[str] = None

    def __post_init__(self):
        if self.properties is None:
            self.properties = {}
        if self.required is None:
            self.required = []


@dataclass
class ToolDefinition:
    """Tool definition."""
    name: str
    description: str
    input_schema: Union[ToolInputSchema, dict]
    type: ToolType = ToolType.TOOL


@dataclass
class ToolUse:
    """A tool use in a message."""
    id: str
    name: str
    input: dict[str, Any]
    type: str = 'tool_use'


@dataclass
class ToolResult:
    """Result from tool execution."""
    type: str = 'tool_result'
    tool_use_id: str = ''
    content: str = ''
    is_error: bool = False


@dataclass
class ToolProgress:
    """Progress update from tool execution."""
    tool_use_id: str
    progress: float = 0.0
    message: str = ''
    extra: dict[str, Any] = None

    def __post_init__(self):
        if self.extra is None:
            self.extra = {}


# Progress event types
@dataclass
class BashProgress:
    """Progress for bash tool."""
    tool_use_id: str
    command: str
    line: str = ''
    exit_code: Optional[int] = None


@dataclass
class EditProgress:
    """Progress for edit tool."""
    tool_use_id: str
    file_path: str
    action: str = ''  # 'replace', 'insert', 'delete'


@dataclass
class ReadProgress:
    """Progress for read tool."""
    tool_use_id: str
    file_path: str
    lines_read: int = 0


@dataclass
class AgentProgress:
    """Progress for agent tool."""
    tool_use_id: str
    agent_id: str
    status: str = ''


@dataclass
class MCPProgress:
    """Progress for MCP tool."""
    tool_use_id: str
    server_name: str
    tool_name: str


@dataclass
class REPLProgress:
    """Progress for REPL tool."""
    tool_use_id: str
    output: str = ''
    error: str = ''


@dataclass
class SkillProgress:
    """Progress for skill tool."""
    tool_use_id: str
    skill_name: str
    step: str = ''


@dataclass
class WebSearchProgress:
    """Progress for web search."""
    tool_use_id: str
    query: str
    results_count: int = 0


@dataclass
class TaskOutputProgress:
    """Progress for task output."""
    task_id: str
    output: str = ''


# Tool permission types
class PermissionMode(str, Enum):
    """Permission mode."""
    DEFAULT = 'default'
    AUTO_ACCEPT = 'auto_accept'
    AUTO_DENY = 'auto_deny'
    BYPASS = 'bypass'


class PermissionResult(str, Enum):
    """Permission check result."""
    ALLOW = 'allow'
    DENY = 'deny'
    ASK = 'ask'


@dataclass
class ToolPermissionContext:
    """Context for tool permission checks."""
    mode: PermissionMode = PermissionMode.DEFAULT
    additional_working_directories: dict[str, Any] = None
    always_allow_rules: dict[str, Any] = None
    always_deny_rules: dict[str, Any] = None
    always_ask_rules: dict[str, Any] = None
    is_bypass_permissions_mode_available: bool = False

    def __post_init__(self):
        if self.additional_working_directories is None:
            self.additional_working_directories = {}
        if self.always_allow_rules is None:
            self.always_allow_rules = {}
        if self.always_deny_rules is None:
            self.always_deny_rules = {}
        if self.always_ask_rules is None:
            self.always_ask_rules = {}


def get_empty_tool_permission_context() -> ToolPermissionContext:
    """Get an empty tool permission context."""
    return ToolPermissionContext()


# Validation result
@dataclass
class ValidationResult:
    """Result of input validation."""
    result: bool
    message: str = ''
    error_code: int = 0


# Query chain tracking
@dataclass
class QueryChainTracking:
    """Tracks query chain for nested queries."""
    chain_id: str
    depth: int = 0


# Tool use context
@dataclass
class ToolUseContext:
    """Context passed to tool execution."""
    tool_name: str
    tool_use_id: str
    permission_context: ToolPermissionContext
    abort_controller: Any = None
    progress_callback: Callable[[ToolProgress], None] = None


# SetToolJSXFn type
SetToolJSXFn = Callable[[Optional[dict]], None]
"""Function to set tool JSX (for displaying tool UI)."""


# CanUseToolFn type
@runtime_checkable
class CanUseToolFn(Protocol):
    """Protocol for tool permission check function."""
    def __call__(self, tool_name: str) -> PermissionResult: ...


# Tool base class
class Tool:
    """Base class for all tools."""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: dict,
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema

    async def execute(
        self,
        input_dict: dict,
        get_app_state: Callable,
        set_app_state: Callable,
        abort_controller: Any = None,
    ) -> dict:
        """Execute the tool with given input."""
        raise NotImplementedError(f"Tool {self.name} not implemented")

    def validate_input(self, input_dict: dict) -> tuple[bool, str]:
        """Validate tool input."""
        return True, ""


# Export common types
__all__ = [
    'Tool',
    'ToolType',
    'ToolStatus',
    'ToolDefinition',
    'ToolInputSchema',
    'ToolUse',
    'ToolResult',
    'ToolProgress',
    'ToolPermissionContext',
    'PermissionMode',
    'PermissionResult',
    'ValidationResult',
    'QueryChainTracking',
    'ToolUseContext',
    'SetToolJSXFn',
    'get_empty_tool_permission_context',
    'BashProgress',
    'EditProgress',
    'ReadProgress',
    'AgentProgress',
    'MCPProgress',
    'REPLProgress',
    'SkillProgress',
    'WebSearchProgress',
    'TaskOutputProgress',
]