"""
Cron tasks lock utility.
"""
import asyncio

class CronTasksLock:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def acquire(self):
        await self._lock.acquire()

    def release(self):
        self._lock.release()

_cron_lock = CronTasksLock()

def get_cron_tasks_lock() -> CronTasksLock:
    return _cron_lock

__all__ = ['CronTasksLock', 'get_cron_tasks_lock']