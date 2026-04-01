"""
Status notice helpers for agent descriptions.
"""

from typing import List, Dict, Any

AGENT_DESCRIPTIONS_THRESHOLD = 15_000


def rough_token_count_estimation(text: str) -> int:
    """Rough token count estimation (roughly 4 chars per token)."""
    return len(text) // 4


def get_agent_descriptions_total_tokens(agent_definitions: Dict[str, Any]) -> int:
    """Calculate cumulative token estimate for agent descriptions."""
    if not agent_definitions:
        return 0

    active_agents = agent_definitions.get("activeAgents", [])
    total = 0
    for agent in active_agents:
        if agent.get("source") != "built-in":
            description = f"{agent.get('agentType', '')}: {agent.get('whenToUse', '')}"
            total += rough_token_count_estimation(description)

    return total


__all__ = [
    "AGENT_DESCRIPTIONS_THRESHOLD",
    "rough_token_count_estimation",
    "get_agent_descriptions_total_tokens",
]