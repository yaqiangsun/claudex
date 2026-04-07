"""Should use sandbox matching src/tools/BashTool/shouldUseSandbox.ts"""
from typing import Dict, Any


# Commands that should always run in sandbox
SANDBOX_REQUIRED_COMMANDS = [
    'rm', 'dd', 'mkfs', 'fdisk', 'parted',
    'shutdown', 'reboot', 'halt', 'poweroff',
    'init', 'systemctl', 'service',
]

# Commands that can run without sandbox
SANDBOX_SAFE_COMMANDS = [
    'ls', 'cat', 'grep', 'find', 'git', 'echo',
    'pwd', 'cd', 'mkdir', 'touch', 'chmod', 'chown',
]


def should_use_sandbox(command: str) -> bool:
    """Determine if command should run in sandbox."""
    import re

    cmd_base = command.strip().split()[0] if command.strip() else ""

    # Check if it's a safe command
    if cmd_base in SANDBOX_SAFE_COMMANDS:
        return False

    # Check if it requires sandbox
    if cmd_base in SANDBOX_REQUIRED_COMMANDS:
        return True

    # Default to sandbox for unknown commands
    return True


def get_sandbox_recommendation(command: str) -> Dict[str, Any]:
    """Get recommendation for sandbox usage."""
    use_sandbox = should_use_sandbox(command)
    cmd_base = command.strip().split()[0] if command.strip() else ""

    return {
        "use_sandbox": use_sandbox,
        "command": cmd_base,
        "reason": "Required for safety" if use_sandbox else "Safe command",
    }


__all__ = ["SANDBOX_REQUIRED_COMMANDS", "SANDBOX_SAFE_COMMANDS", "should_use_sandbox", "get_sandbox_recommendation"]