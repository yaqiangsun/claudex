"""
Tasks utilities.

Task management.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import uuid


@dataclass
class Task:
    """A task."""
    id: str
    title: str
    status: str = "pending"


def create_task(title: str) -> Task:
    """Create a task."""
    return Task(id=str(uuid.uuid4()), title=title)


def get_tasks() -> List[Task]:
    """Get all tasks."""
    return []


__all__ = [
    "Task",
    "create_task",
    "get_tasks",
]