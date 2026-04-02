"""
Agent tool.
"""
from typing import Any, Dict

class AgentTool:
    name = "agent"
    description = "Agent tool"

    async def execute(self, params: Dict[str, Any]) -> Any:
        return {"status": "ok"}

__all__ = ['AgentTool']