"""Agent display utilities matching src/tools/AgentTool/agentDisplay.ts"""
from typing import Optional, Dict, Any
from .constants import AgentStatus


class AgentDisplay:
    """Handles displaying agent status and information."""

    @staticmethod
    def format_status(status: AgentStatus) -> str:
        """Format status for display."""
        status_icons = {
            AgentStatus.IDLE: "○",
            AgentStatus.RUNNING: "▶",
            AgentStatus.PAUSED: "⏸",
            AgentStatus.COMPLETED: "✓",
            AgentStatus.FAILED: "✗",
        }
        return status_icons.get(status, "?")

    @staticmethod
    def format_agent_info(name: str, status: AgentStatus, description: str = "") -> str:
        """Format agent information for display."""
        icon = AgentDisplay.format_status(status)
        parts = [f"{icon} {name}"]
        if description:
            parts.append(f"- {description}")
        return " ".join(parts)


__all__ = ["AgentDisplay"]