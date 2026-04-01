"""
Tasks module - Task definitions and execution.

This module handles background task management including:
- Local shell tasks
- Local agent tasks
- Remote agent tasks
- In-process teammate tasks
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class TaskType(str, Enum):
    """Task type definitions."""
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
    """Check if task status is terminal."""
    return status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.KILLED)


@dataclass
class TaskState:
    """Task state definition."""
    id: str
    type: TaskType
    status: TaskStatus
    description: str
    start_time: float = 0
    end_time: Optional[float] = None


__all__ = [
    'TaskType',
    'TaskStatus',
    'TaskState',
    'is_terminal_task_status',
]