"""BashTool package matching src/tools/BashTool/"""
import asyncio
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Callable
import os

from .. import BaseTool

# Tool constants
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


class BashTool(BaseTool):
    """Tool for executing shell commands."""

    def __init__(self):
        super().__init__(BASH_TOOL_NAME, DESCRIPTION)
        self.input_schema = {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The command to execute"},
                "timeout": {"type": "number", "description": "Timeout in milliseconds"},
                "description": {"type": "string", "description": "Description of the command"},
            },
            "required": ["command"],
        }

    async def execute(
        self,
        input_dict: Dict[str, Any],
        get_app_state: Callable,
        set_app_state: Callable,
        abort_controller: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Execute a bash command."""
        return await execute_bash(input_dict, get_app_state, set_app_state, abort_controller)


async def _run_command(
    command: str,
    timeout_ms: int,
    abort_controller: Optional[Any] = None,
) -> Dict[str, str]:
    """Run a shell command."""
    cwd = os.getcwd()

    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

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

        cmd_info = parse_command(command)
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


def get_default_timeout_ms() -> int:
    """Get the default timeout for bash commands."""
    return DEFAULT_TIMEOUT_MS


def parse_command(command: str) -> Dict[str, Any]:
    """Parse a shell command to determine its type and properties."""
    parts = command.strip().split()
    base_cmd = parts[0] if parts else ""

    return {
        "is_search": base_cmd in BASH_SEARCH_COMMANDS,
        "is_read": base_cmd in BASH_READ_COMMANDS,
        "is_list": base_cmd in BASH_LIST_COMMANDS,
        "has_no_output": base_cmd in BASH_NO_OUTPUT_COMMANDS,
        "is_background": "&" in command,
    }


from .bash_command_helpers import ParsedCommand, split_command, is_unsafe_compound_command
from .bash_permissions import PermissionLevel, BashPermissions, check_permission
from .bash_security import BashSecurity, bash_command_is_safe, DANGEROUS_COMMANDS, MODIFYING_COMMANDS
from .command_semantics import CommandType, classify_command, get_command_intent
from .comment_label import COMMENT_LABELS, extract_comment_label, strip_comment_label
from .destructive_command_warning import DESTRUCTIVE_PATTERNS, check_destructive, get_warning_message
from .mode_validation import BashMode, MODE_ALLOWLIST, validate_mode, is_mode_restricted
from .path_validation import PROTECTED_PATHS, is_protected_path, has_path_traversal, validate_paths
from .read_only_validation import READ_ONLY_COMMANDS, is_read_only_command, validate_read_only
from .sed_edit_parser import SedEditParser, parse_sed_edit
from .sed_validation import DANGEROUS_SED_PATTERNS, validate_sed_command, is_sed_safe
from .should_use_sandbox import SANDBOX_REQUIRED_COMMANDS, SANDBOX_SAFE_COMMANDS, should_use_sandbox, get_sandbox_recommendation
from .tool_name import TOOL_NAME, TOOL_ALIASES, get_tool_name, is_bash_command
from .utils import run_command, parse_command_args, get_working_directory
from .prompt import BASH_TOOL_PROMPT, get_bash_prompt

__all__ = [
    # Core tool
    "BashTool",
    "BashToolInput",
    "BashToolOutput",
    "BASH_TOOL_NAME",
    "DESCRIPTION",
    "DEFAULT_TIMEOUT_MS",
    "get_default_timeout_ms",
    # Execute functions
    "execute_bash",
    # Helper functions
    "parse_command",
    # Constants
    "BASH_SEARCH_COMMANDS",
    "BASH_READ_COMMANDS",
    "BASH_LIST_COMMANDS",
    "BASH_NO_OUTPUT_COMMANDS",
    # Submodules
    "ParsedCommand",
    "split_command",
    "is_unsafe_compound_command",
    "PermissionLevel",
    "BashPermissions",
    "check_permission",
    "BashSecurity",
    "bash_command_is_safe",
    "DANGEROUS_COMMANDS",
    "MODIFYING_COMMANDS",
    "CommandType",
    "classify_command",
    "get_command_intent",
    "COMMENT_LABELS",
    "extract_comment_label",
    "strip_comment_label",
    "DESTRUCTIVE_PATTERNS",
    "check_destructive",
    "get_warning_message",
    "BashMode",
    "MODE_ALLOWLIST",
    "validate_mode",
    "is_mode_restricted",
    "PROTECTED_PATHS",
    "is_protected_path",
    "has_path_traversal",
    "validate_paths",
    "READ_ONLY_COMMANDS",
    "is_read_only_command",
    "validate_read_only",
    "SedEditParser",
    "parse_sed_edit",
    "DANGEROUS_SED_PATTERNS",
    "validate_sed_command",
    "is_sed_safe",
    "SANDBOX_REQUIRED_COMMANDS",
    "SANDBOX_SAFE_COMMANDS",
    "should_use_sandbox",
    "get_sandbox_recommendation",
    "TOOL_NAME",
    "TOOL_ALIASES",
    "get_tool_name",
    "is_bash_command",
    "run_command",
    "parse_command_args",
    "get_working_directory",
    "BASH_TOOL_PROMPT",
    "get_bash_prompt",
]