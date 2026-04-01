"""
Command registry and base types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional, Union


class CommandSource(str, Enum):
    """Source of the command."""
    BUILTIN = 'builtin'
    SKILLS = 'skills'
    PLUGIN = 'plugin'
    MANAGED = 'managed'
    BUNDLED = 'bundled'
    MCP = 'mcp'


class CommandAvailability(str, Enum):
    """Availability requirements for commands."""
    CLAUDE_AI = 'claude-ai'  # claude.ai OAuth subscriber
    CONSOLE = 'console'  # Console API key user


class CommandResultDisplay(str, Enum):
    """How to display command result."""
    SKIP = 'skip'
    SYSTEM = 'system'
    USER = 'user'


@dataclass
class CommandBase:
    """Base command definition."""
    name: str
    description: str
    availability: Optional[list[CommandAvailability]] = None
    is_enabled: Optional[Callable[[], bool]] = None
    is_hidden: bool = False
    aliases: list[str] = field(default_factory=list)
    is_mcp: bool = False
    argument_hint: Optional[str] = None
    when_to_use: Optional[str] = None
    version: Optional[str] = None
    disable_model_invocation: bool = False
    user_invocable: bool = True
    loaded_from: Optional[str] = None
    kind: Optional[str] = None
    immediate: bool = False
    is_sensitive: bool = False


@dataclass
class PromptCommand(CommandBase):
    """Prompt-type command (skill-like)."""
    type: str = 'prompt'
    progress_message: str = ''
    content_length: int = 0
    arg_names: Optional[list[str]] = None
    allowed_tools: Optional[list[str]] = None
    model: Optional[str] = None
    source: str = 'builtin'
    plugin_info: Optional[dict] = None
    disable_non_interactive: bool = False
    hooks: Optional[dict] = None
    skill_root: Optional[str] = None
    context: str = 'inline'  # 'inline' or 'fork'
    agent: Optional[str] = None
    effort: Optional[str] = None
    paths: Optional[list[str]] = None

    async def get_prompt_for_command(self, args: str, context: dict) -> list[dict]:
        """Get prompt content for this command."""
        raise NotImplementedError


@dataclass
class LocalCommand(CommandBase):
    """Local non-interactive command."""
    type: str = 'local'
    supports_non_interactive: bool = True

    async def call(self, args: str, context: dict) -> 'LocalCommandResult':
        """Execute the command."""
        raise NotImplementedError


@dataclass
class LocalJSXCommand(CommandBase):
    """Local JSX/UI command."""
    type: str = 'local-jsx'
    supports_non_interactive: bool = True

    async def call(self, on_done: Callable, context: dict, args: str) -> Any:
        """Execute the command with UI."""
        raise NotImplementedError


# Type alias for any command
Command = Union[PromptCommand, LocalCommand, LocalJSXCommand]


@dataclass
class LocalCommandResult:
    """Result from a local command."""
    type: str = 'text'  # 'text', 'compact', 'skip'
    value: str = ''
    compaction_result: Optional[dict] = None
    display_text: Optional[str] = None


# Global command registry
_command_registry: dict[str, Command] = {}


def register_command(command: Command) -> None:
    """Register a command."""
    _command_registry[command.name] = command
    # Also register aliases
    if hasattr(command, 'aliases'):
        for alias in command.aliases:
            _command_registry[alias] = command


def get_command(name: str) -> Optional[Command]:
    """Get a command by name."""
    return _command_registry.get(name)


def get_all_commands() -> dict[str, Command]:
    """Get all registered commands."""
    return dict(_command_registry)


def get_command_names() -> list[str]:
    """Get list of all command names."""
    return list(_command_registry.keys())


# Command result callback
LocalJSXCommandOnDone = Callable[[Optional[str], Optional[dict]], None]
"""Callback when a local JSX command completes."""


# Helper functions
def get_command_name(cmd: CommandBase) -> str:
    """Get the user-visible name of a command."""
    if hasattr(cmd, 'user_facing_name') and callable(cmd.user_facing_name):
        return cmd.user_facing_name()
    return cmd.name


def is_command_enabled(cmd: CommandBase) -> bool:
    """Check if a command is enabled."""
    if cmd.is_enabled is None:
        return True
    return cmd.is_enabled()


def meets_availability_requirement(
    cmd: CommandBase,
    auth_type: Optional[str] = None,
) -> bool:
    """Check if user meets availability requirements."""
    if not cmd.availability:
        return True
    if not auth_type:
        return False
    return auth_type in [a.value for a in cmd.availability]


# Export
__all__ = [
    'Command',
    'CommandBase',
    'PromptCommand',
    'LocalCommand',
    'LocalJSXCommand',
    'LocalCommandResult',
    'CommandSource',
    'CommandAvailability',
    'CommandResultDisplay',
    'register_command',
    'get_command',
    'get_all_commands',
    'get_command_names',
    'get_command_name',
    'is_command_enabled',
    'meets_availability_requirement',
]