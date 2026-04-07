"""Mode validation matching src/tools/BashTool/modeValidation.ts"""
from typing import Dict, Any, Optional
from enum import Enum


class BashMode(str, Enum):
    """Bash execution modes."""
    NORMAL = "normal"
    READ_ONLY = "read_only"
    SANDBOX = "sandbox"
    RESTRICTED = "restricted"


# Commands allowed in each mode
MODE_ALLOWLIST = {
    BashMode.READ_ONLY: [
        'cat', 'head', 'tail', 'less', 'more', 'grep', 'find', 'ls',
        'stat', 'file', 'diff', 'git diff', 'git log', 'git show',
    ],
    BashMode.SANDBOX: [
        # Limited commands allowed in sandbox
        'echo', 'pwd', 'cd', 'ls', 'cat', 'grep', 'find', 'git status',
    ],
    BashMode.RESTRICTED: [
        # Only very safe commands
        'echo', 'pwd', 'ls', 'git status',
    ],
}


def validate_mode(command: str, mode: BashMode) -> Dict[str, Any]:
    """Validate command against mode restrictions."""
    if mode == BashMode.NORMAL:
        return {"allowed": True, "mode": mode}

    # Get allowed commands for mode
    allowed = MODE_ALLOWLIST.get(mode, [])

    # Check if command starts with any allowed command
    command_base = command.strip().split()[0] if command.strip() else ""

    is_allowed = any(
        command.startswith(allowed_cmd)
        for allowed_cmd in allowed
    )

    return {
        "allowed": is_allowed,
        "mode": mode,
        "command_base": command_base,
    }


def is_mode_restricted(mode: BashMode) -> bool:
    """Check if mode has restrictions."""
    return mode != BashMode.NORMAL


__all__ = ["BashMode", "MODE_ALLOWLIST", "validate_mode", "is_mode_restricted"]