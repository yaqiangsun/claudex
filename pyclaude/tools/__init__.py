"""
Tools module - Tool implementations.

This module contains various tool implementations:
- BashTool - Execute shell commands
- ReadTool - Read files
- EditTool - Edit files
- WriteTool - Write files
- GlobTool - File globbing
- GrepTool - Search files
- etc.
"""

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class BaseTool(ABC):
    """Base class for all tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(
        self,
        input_dict: Dict[str, Any],
        get_app_state: callable,
        set_app_state: callable,
        abort_controller: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Execute the tool with given input."""
        pass


def get_all_tools() -> list:
    """Get all available tools."""
    from .bash_tool import BashTool
    from .read_tool import ReadTool
    from .edit_tool import EditTool
    from .write_tool import WriteTool
    from .glob_tool import GlobTool
    from .grep_tool import GrepTool
    from .agent_tool import AgentTool

    return [
        BashTool(),
        ReadTool(),
        EditTool(),
        WriteTool(),
        GlobTool(),
        GrepTool(),
        AgentTool(),
    ]


__all__ = ['BaseTool', 'get_all_tools']