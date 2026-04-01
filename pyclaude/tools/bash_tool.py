"""
BashTool - Execute shell commands.

Python adaptation of the Bash tool for executing shell commands.
"""

from typing import Any, Dict, Optional, Callable
import asyncio
import os
import subprocess
import time
from dataclasses import dataclass


BASH_TOOL_NAME = "Bash"

DESCRIPTION = """- Use this tool to execute shell commands in a terminal
- Returns the command output (stdout/stderr)
- Supports long-running commands with timeout configuration
- Can run commands in background mode"""

# Search commands for collapsible display
BASH_SEARCH_COMMANDS = {'find', 'grep', 'rg', 'ag', 'ack', 'locate', 'which', 'whereis'}

# Read/view commands for collapsible display
BASH_READ_COMMANDS = {'cat', 'head', 'tail', 'less', 'more', 'wc', 'stat', 'file', 'strings'}

# Directory-listing commands
BASH_LIST_COMMANDS = {'ls', 'tree', 'du'}

# Commands that produce no stdout on success
BASH_NO_OUTPUT_COMMANDS = {'cd', 'exit', 'return', 'true', 'false', ':'}

DEFAULT_TIMEOUT_MS = 30 * 60 * 1000  # 30 minutes


@dataclass
class BashToolInput:
    """Input schema for BashTool."""
    command: str
    timeout: Optional[int] = None
    description: Optional[str] = None


@dataclass
class BashToolOutput:
    """Output schema for BashTool."""
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: float


def parse_command(command: str) -> Dict[str, Any]:
    """Parse a shell command to determine its type and properties."""
    # Get the base command
    parts = command.strip().split()
    base_cmd = parts[0] if parts else ""

    return {
        "is_search": base_cmd in BASH_SEARCH_COMMANDS,
        "is_read": base_cmd in BASH_READ_COMMANDS,
        "is_list": base_cmd in BASH_LIST_COMMANDS,
        "has_no_output": base_cmd in BASH_NO_OUTPUT_COMMANDS,
        "is_background": "&" in command,
    }


async def execute_bash(
    input_dict: Dict[str, Any],
    get_app_state: Callable,
    set_app_state: Callable,
    abort_controller: Optional[Any] = None,
) -> Dict[str, Any]:
    """Execute a bash command."""
    start_time = time.time()

    try:
        command = input_dict.get("command", "")
        timeout_ms = input_dict.get("timeout", DEFAULT_TIMEOUT_MS)

        if not command:
            return {
                "success": False,
                "error": "command is required",
            }

        # Parse command for metadata
        cmd_info = parse_command(command)

        # Execute command
        result = await _run_command(command, timeout_ms, abort_controller)

        duration_ms = (time.time() - start_time) * 1000

        return {
            "success": result["exit_code"] == 0,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "exit_code": result["exit_code"],
            "duration_ms": duration_ms,
            **cmd_info,
        }

    except asyncio.TimeoutError:
        return {
            "success": False,
            "error": f"Command timed out after {timeout_ms}ms",
            "exit_code": 124,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "exit_code": 1,
        }


async def _run_command(
    command: str,
    timeout_ms: int,
    abort_controller: Optional[Any] = None,
) -> Dict[str, str]:
    """Run a shell command."""
    # Get current working directory
    cwd = os.getcwd()

    try:
        # Run command with subprocess
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

        # Wait for completion with timeout
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout_ms / 1000,
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise

        return {
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "exit_code": process.returncode or 0,
        }

    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": 1,
        }


def get_default_timeout_ms() -> int:
    """Get the default timeout for bash commands."""
    return DEFAULT_TIMEOUT_MS


__all__ = [
    "BASH_TOOL_NAME",
    "DESCRIPTION",
    "BashToolInput",
    "BashToolOutput",
    "execute_bash",
    "parse_command",
    "get_default_timeout_ms",
]