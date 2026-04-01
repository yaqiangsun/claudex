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


# Placeholder for tool implementations
__all__ = ['BaseTool']