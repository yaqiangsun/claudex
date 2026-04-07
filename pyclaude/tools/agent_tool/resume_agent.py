"""Resume agent matching src/tools/AgentTool/resumeAgent.ts"""
from typing import Dict, Any, Optional
from .constants import AgentStatus


class ResumeAgent:
    """Handles resuming a paused agent."""

    def __init__(self, agent_registry: Dict[str, Any]):
        self.agent_registry = agent_registry

    def resume(self, agent_id: str) -> Dict[str, Any]:
        """Resume a paused agent."""
        if agent_id not in self.agent_registry:
            return {
                "success": False,
                "error": f"Agent {agent_id} not found",
            }

        agent = self.agent_registry[agent_id]
        if agent.get("status") != AgentStatus.PAUSED:
            return {
                "success": False,
                "error": f"Agent {agent_id} is not paused",
            }

        agent["status"] = AgentStatus.RUNNING
        return {
            "success": True,
            "agent_id": agent_id,
            "status": AgentStatus.RUNNING,
        }

    def can_resume(self, agent_id: str) -> bool:
        """Check if an agent can be resumed."""
        if agent_id not in self.agent_registry:
            return False
        return self.agent_registry[agent_id].get("status") == AgentStatus.PAUSED


__all__ = ["ResumeAgent"]