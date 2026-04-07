"""Agent tool utilities matching src/tools/AgentTool/agentToolUtils.ts"""
from typing import Dict, Any, Optional, List, Callable
from .constants import AgentStatus
import uuid


class AgentToolUtils:
    """Utility functions for agent tool operations."""

    @staticmethod
    def generate_agent_id() -> str:
        """Generate a unique agent ID."""
        return f"agent_{uuid.uuid4().hex[:8]}"

    @staticmethod
    def validate_agent_name(name: str) -> bool:
        """Validate agent name."""
        if not name:
            return False
        # Agent names should be alphanumeric with hyphens/underscores
        return all(c.isalnum() or c in '-_' for c in name)

    @staticmethod
    def parse_agent_args(args: str) -> Dict[str, Any]:
        """Parse agent arguments from string."""
        result = {}
        parts = args.split()
        i = 0
        while i < len(parts):
            if parts[i].startswith('--'):
                key = parts[i][2:]
                if i + 1 < len(parts) and not parts[i + 1].startswith('--'):
                    result[key] = parts[i + 1]
                    i += 2
                else:
                    result[key] = True
                    i += 1
            else:
                i += 1
        return result

    @staticmethod
    def should_agent_stop(status: AgentStatus, reason: Optional[str] = None) -> bool:
        """Determine if agent should stop."""
        if status in (AgentStatus.COMPLETED, AgentStatus.FAILED):
            return True
        if reason and reason.lower() in ('exit', 'quit', 'done', 'stop'):
            return True
        return False

    @staticmethod
    def format_agent_result(result: Dict[str, Any]) -> str:
        """Format agent result for display."""
        if "error" in result:
            return f"Error: {result['error']}"
        if "output" in result:
            return result["output"]
        return str(result)


__all__ = ["AgentToolUtils"]