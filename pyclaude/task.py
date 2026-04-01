"""
Task definitions for background operations.
"""

import secrets
from enum import Enum
from typing import TYPE_CHECKING, Callable, Protocol, runtime_checkable, Optional

if TYPE_CHECKING:
    from .state import AppState


class TaskType(str, Enum):
    """Types of background tasks."""
    LOCAL_BASH = 'local_bash'
    LOCAL_AGENT = 'local_agent'
    REMOTE_AGENT = 'remote_agent'
    IN_PROCESS_TEAMMATE = 'in_process_teammate'
    LOCAL_WORKFLOW = 'local_workflow'
    MONITOR_MCP = 'monitor_mcp'
    DREAM = 'dream'


class TaskStatus(str, Enum):
    """Task status values."""
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    KILLED = 'killed'


def is_terminal_task_status(status: TaskStatus) -> bool:
    """
    True when a task is in a terminal state and will not transition further.
    Used to guard against injecting messages into dead teammates, evicting
    finished tasks from AppState, and orphan-cleanup paths.
    """
    return status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.KILLED)


# Task ID prefixes
TASK_ID_PREFIXES: dict[str, str] = {
    TaskType.LOCAL_BASH: 'b',
    TaskType.LOCAL_AGENT: 'a',
    TaskType.REMOTE_AGENT: 'r',
    TaskType.IN_PROCESS_TEAMMATE: 't',
    TaskType.LOCAL_WORKFLOW: 'w',
    TaskType.MONITOR_MCP: 'm',
    TaskType.DREAM: 'd',
}

# Case-insensitive-safe alphabet (digits + lowercase) for task IDs.
# 36^8 ≈ 2.8 trillion combinations
TASK_ID_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyz'


def generate_task_id(task_type: TaskType) -> str:
    """Generate a unique task ID."""
    prefix = TASK_ID_PREFIXES.get(task_type, 'x')
    random_bytes = secrets.token_bytes(8)
    id = prefix
    for byte in random_bytes:
        id += TASK_ID_ALPHABET[byte % len(TASK_ID_ALPHABET)]
    return id


@runtime_checkable
class Task(Protocol):
    """Protocol for task implementations."""
    name: str
    type: TaskType

    async def kill(self, task_id: str, set_app_state: Callable) -> None: ...


# Type aliases
TaskHandle = dict
SetAppState = Callable[[Callable[['AppState'], 'AppState']], None]


class TaskContext:
    """Context passed to task implementations."""
    def __init__(
        self,
        abort_controller: 'AbortController',
        get_app_state: Callable[[], 'AppState'],
        set_app_state: SetAppState,
    ):
        self.abort_controller = abort_controller
        self.get_app_state = get_app_state
        self.set_app_state = set_app_state


class AbortController:
    """Simple abort controller for tasks."""
    def __init__(self):
        self._aborted = False

    def abort(self):
        self._aborted = True

    @property
    def is_aborted(self) -> bool:
        return self._aborted


# Base fields shared by all task states
@dataclass
class TaskStateBase:
    id: str
    type: TaskType
    status: TaskStatus
    description: str
    tool_use_id: Optional[str] = None
    start_time: int = 0
    end_time: Optional[int] = None
    total_paused_ms: Optional[int] = None
    output_file: str = ''
    output_offset: int = 0
    notified: bool = False


from dataclasses import dataclass


def create_task_state_base(
    id: str,
    task_type: TaskType,
    description: str,
    tool_use_id: Optional[str] = None,
) -> TaskStateBase:
    """Create a base task state."""
    from .utils.task import get_task_output_path
    return TaskStateBase(
        id=id,
        type=task_type,
        status=TaskStatus.PENDING,
        description=description,
        tool_use_id=tool_use_id,
        start_time=0,
        output_file=get_task_output_path(id),
        output_offset=0,
        notified=False,
    )


LocalShellSpawnInput = dict  # Simplified - full type has more fields