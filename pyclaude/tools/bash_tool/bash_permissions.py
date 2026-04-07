"""Bash permissions matching src/tools/BashTool/bashPermissions.ts"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class PermissionLevel(Enum):
    """Permission levels for bash commands."""
    NONE = "none"
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ALL = "all"


@dataclass
class BashPermissions:
    """Permissions for bash tool."""
    allowed_commands: list[str] = None
    denied_commands: list[str] = None
    max_output_size: int = 1024 * 1024  # 1MB
    timeout: int = 300  # 5 seconds

    def __post_init__(self):
        if self.allowed_commands is None:
            self.allowed_commands = []
        if self.denied_commands is None:
            self.denied_commands = []


def check_permission(command: str, permissions: BashPermissions) -> bool:
    """Check if a command is allowed."""
    import re

    # Check denied commands first
    for pattern in permissions.denied_commands:
        if re.search(pattern, command):
            return False

    # Check allowed commands
    if permissions.allowed_commands:
        for pattern in permissions.allowed_commands:
            if re.search(pattern, command):
                return True
        return False

    return True


__all__ = ["PermissionLevel", "BashPermissions", "check_permission"]