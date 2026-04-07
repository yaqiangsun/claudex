"""Bash security matching src/tools/BashTool/bashSecurity.ts"""
import re
from typing import Dict, Any, List, Optional


# Dangerous commands that should require extra scrutiny
DANGEROUS_COMMANDS = [
    r'rm\s+-rf',
    r'dd\s+',
    r'mkfs\.',
    r':\(\)\{',  # Fork bomb
    r'>\s*/dev/sd',  # Direct disk write
    r'chmod\s+777',
    r'chown\s+-R',
    r'sudo\s+rm',
    r'>\s*/etc/',
    r'drop\s+database',
]


# Commands that modify system state
MODIFYING_COMMANDS = [
    r'rm\s+',
    r'mv\s+',
    r'cp\s+',
    r'del\s+',
    r'format\s+',
    r'mkdir\s+',
    r'touch\s+',
]


class BashSecurity:
    """Security checks for bash commands."""

    @staticmethod
    def is_dangerous(command: str) -> bool:
        """Check if command is potentially dangerous."""
        for pattern in DANGEROUS_COMMANDS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def is_modifying(command: str) -> bool:
        """Check if command modifies the system."""
        for pattern in MODIFYING_COMMANDS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def check_safety(command: str) -> Dict[str, Any]:
        """Perform comprehensive safety check."""
        return {
            "is_dangerous": BashSecurity.is_dangerous(command),
            "is_modifying": BashSecurity.is_modifying(command),
            "needs_confirmation": BashSecurity.is_dangerous(command) or BashSecurity.is_modifying(command),
        }


def bash_command_is_safe(command: str) -> bool:
    """Quick check if bash command is safe."""
    return not BashSecurity.is_dangerous(command)


__all__ = ["BashSecurity", "bash_command_is_safe", "DANGEROUS_COMMANDS", "MODIFYING_COMMANDS"]