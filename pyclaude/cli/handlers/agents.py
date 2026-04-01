"""
Agents subcommand handler - prints the list of configured agents.
Dynamically imported only when `claude agents` runs.
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ResolvedAgent:
    """Resolved agent definition."""
    agent_type: str
    model: Optional[str] = None
    memory: Optional[str] = None
    source: str = ''
    overridden_by: Optional[str] = None


# Placeholder - full implementation requires agent loading from files
AGENT_SOURCE_GROUPS = [
    ('Built-in', 'builtin'),
    ('Project', 'project'),
    ('User', 'user'),
]


def resolve_agent_model_display(agent: ResolvedAgent) -> Optional[str]:
    """Get the display string for agent model."""
    return agent.model


def compare_agents_by_name(agent1: ResolvedAgent, agent2: ResolvedAgent) -> int:
    """Compare agents by name."""
    return agent1.agent_type.lower() < agent2.agent_type.lower()


def get_override_source_label(override_source: str) -> str:
    """Get the label for override source."""
    return override_source


def format_agent(agent: ResolvedAgent) -> str:
    """Format agent for display."""
    parts = [agent.agent_type]
    model = resolve_agent_model_display(agent)
    if model:
        parts.append(model)
    if agent.memory:
        parts.append(f"{agent.memory} memory")
    return ' · '.join(parts)


def get_active_agents_from_list(agents: List[ResolvedAgent]) -> List[ResolvedAgent]:
    """Get active agents from list (non-overridden)."""
    return [a for a in agents if not a.overridden_by]


def get_agent_definitions_with_overrides(cwd: str) -> dict:
    """Get agent definitions with overrides applied."""
    # Placeholder - loads agents from cwd
    return {'allAgents': []}


def resolve_agent_overrides(
    all_agents: List[ResolvedAgent],
    active_agents: List[ResolvedAgent],
) -> List[ResolvedAgent]:
    """Resolve agent overrides."""
    return all_agents


async def agents_handler() -> None:
    """Handle the agents subcommand."""
    from ...utils.cwd import get_cwd

    cwd = get_cwd()
    result = await get_agent_definitions_with_overrides(cwd)
    all_agents = result.get('allAgents', [])
    active_agents = get_active_agents_from_list(all_agents)
    resolved_agents = resolve_agent_overrides(all_agents, active_agents)

    lines: List[str] = []
    total_active = 0

    for label, source in AGENT_SOURCE_GROUPS:
        group_agents = [
            a for a in resolved_agents
            if a.source == source
        ]
        group_agents.sort(key=lambda a: a.agent_type.lower())

        if len(group_agents) == 0:
            continue

        lines.append(f"{label}:")
        for agent in group_agents:
            if agent.overridden_by:
                winner_source = get_override_source_label(agent.overridden_by)
                lines.append(f"  (shadowed by {winner_source}) {format_agent(agent)}")
            else:
                lines.append(f"  {format_agent(agent)}")
                total_active += 1
        lines.append('')

    if len(lines) == 0:
        print('No agents found.')
    else:
        print(f"{total_active} active agents\n")
        print('\n'.join(lines).rstrip())