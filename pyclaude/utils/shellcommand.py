"""
Shell command utility.

Shell command types and creation functions.
"""

from typing import Optional, Dict, Any


class ShellCommand:
    """Represents a shell command execution result."""

    def __init__(
        self,
        command: str,
        aborted: bool = False,
        failed: bool = False,
        code: Optional[int] = None,
        signal: Optional[str] = None,
        stdout: str = '',
        stderr: str = '',
        background_task_id: Optional[str] = None,
    ):
        self.command = command
        self.aborted = aborted
        self.failed = failed
        self.code = code
        self.signal = signal
        self.stdout = stdout
        self.stderr = stderr
        self.background_task_id = background_task_id

    @property
    def result(self) -> Any:
        """Compatibility property."""
        return self

    @property
    def success(self) -> bool:
        """Check if command succeeded."""
        return self.code == 0 and not self.aborted and not self.failed


def create_aborted_command(
    command: str = '',
    error: Optional[Dict[str, Any]] = None,
) -> ShellCommand:
    """Create an aborted command."""
    return ShellCommand(
        command=command,
        aborted=True,
        code=error.get('code') if error else 126,
        stderr=error.get('stderr') if error else '',
    )


def create_failed_command(
    error_message: str,
    code: int = 1,
) -> ShellCommand:
    """Create a failed command."""
    return ShellCommand(
        command='',
        failed=True,
        code=code,
        stderr=error_message,
    )


def wrap_spawn(child_process: Any, abort_signal: Any, timeout: int, task_output: Any, auto_background: bool = False) -> 'ShellCommand':
    """Wrap a spawned process as a ShellCommand."""
    # Simplified placeholder
    return ShellCommand(command='')


__all__ = ['ShellCommand', 'create_aborted_command', 'create_failed_command', 'wrap_spawn']