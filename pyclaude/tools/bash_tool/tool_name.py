"""Tool name matching src/tools/BashTool/toolName.ts"""

# The official name of the Bash tool
TOOL_NAME = "Bash"

# Alternative names/aliases
TOOL_ALIASES = ["bash", "shell", "terminal", "cmd", "execute"]


def get_tool_name() -> str:
    """Get the official tool name."""
    return TOOL_NAME


def is_bash_command(command: str) -> bool:
    """Check if a command looks like a bash command."""
    cmd_lower = command.strip().lower()
    return any(cmd_lower.startswith(alias) for alias in TOOL_ALIASES)


__all__ = ["TOOL_NAME", "TOOL_ALIASES", "get_tool_name", "is_bash_command"]