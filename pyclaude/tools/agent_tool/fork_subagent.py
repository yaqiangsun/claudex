"""Fork subagent matching src/tools/AgentTool/forkSubagent.ts"""
from typing import Dict, Any, Optional, Callable
import uuid
from .constants import AgentStatus


class ForkSubagent:
    """Handles forking a new subagent from the current agent."""

    def __init__(self, parent_agent_id: str):
        self.parent_agent_id = parent_agent_id

    def fork(
        self,
        prompt: str,
        agent_type: str = "general-purpose",
        tools: Optional[list[str]] = None,
    ) -> Dict[str, Any]:
        """Fork a new subagent."""
        agent_id = f"fork_{uuid.uuid4().hex[:8]}"
        return {
            "agent_id": agent_id,
            "parent_id": self.parent_agent_id,
            "prompt": prompt,
            "agent_type": agent_type,
            "tools": tools or [],
            "status": AgentStatus.IDLE,
        }

    def fork_with_context(
        self,
        parent_context: Dict[str, Any],
        prompt: str,
    ) -> Dict[str, Any]:
        """Fork a subagent with inherited context."""
        fork = self.fork(prompt)
        fork["inherited_context"] = parent_context
        return fork


__all__ = ["ForkSubagent"]