"""
Cron tasks utility.
"""
import asyncio
from typing import Callable, Dict, Any

class CronTasks:
    def __init__(self):
        self._tasks: Dict[str, Any] = {}

    def schedule(self, name: str, func: Callable, interval: int) -> None:
        self._tasks[name] = {'func': func, 'interval': interval}

cron_tasks = CronTasks()

def get_cron_tasks() -> CronTasks:
    return cron_tasks

__all__ = ['CronTasks', 'get_cron_tasks']