"""Spinner service - terminal spinner/progress indicator."""

import asyncio
import sys
import time
from typing import Optional
from dataclasses import dataclass


@dataclass
class SpinnerConfig:
    """Configuration for spinner."""
    message: str = 'Loading...'
    spinner_chars: str = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    interval: float = 0.1
    color: Optional[str] = None


class Spinner:
    """Terminal spinner."""

    def __init__(self, config: Optional[SpinnerConfig] = None):
        self.config = config or SpinnerConfig()
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._frame = 0

    async def start(self) -> None:
        """Start the spinner."""
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(self._spin())

    async def stop(self) -> None:
        """Stop the spinner."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._task = None

    async def update_message(self, message: str) -> None:
        """Update the spinner message."""
        self.config.message = message

    async def _spin(self) -> None:
        """Spin the spinner."""
        try:
            while self._running:
                frame = self.config.spinner_chars[self._frame % len(self.config.spinner_chars)]
                sys.stdout.write(f'\r{frame} {self.config.message}')
                sys.stdout.flush()

                self._frame += 1
                await asyncio.sleep(self.config.interval)
        except asyncio.CancelledError:
            pass
        finally:
            sys.stdout.write('\r' + ' ' * (len(self.config.message) + 2))
            sys.stdout.write('\r')
            sys.stdout.flush()


# Global spinner instance
_spinner: Optional[Spinner] = None


def get_spinner() -> Spinner:
    """Get or create the global spinner."""
    global _spinner
    if _spinner is None:
        _spinner = Spinner()
    return _spinner


async def spin(message: str = 'Loading...') -> Spinner:
    """Start spinning with a message."""
    spinner = get_spinner()
    spinner.config.message = message
    await spinner.start()
    return spinner


async def stop_spin() -> None:
    """Stop the global spinner."""
    global _spinner
    if _spinner:
        await _spinner.stop()


__all__ = ['Spinner', 'SpinnerConfig', 'get_spinner', 'spin', 'stop_spin']