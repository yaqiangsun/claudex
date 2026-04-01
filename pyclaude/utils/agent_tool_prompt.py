"""
AgentTool prompt generation.

Python adaptation for generating the Agent tool prompt.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


AGENT_TOOL_NAME = "Agent"


@dataclass
class AgentDefinition:
    """Definition of an agent."""
    agent_type: str
    when_to_use: str
    tools: Optional[List[str]] = None
    disallowed_tools: Optional[List[str]] = None


def get_tools_description(agent: AgentDefinition) -> str:
    """Get the description of tools available to an agent."""
    tools = agent.tools or []
    disallowed = agent.disallowed_tools or []

    if tools and disallowed:
        deny_set = set(disallowed)
        effective = [t for t in tools if t not in deny_set]
        return ", ".join(effective) if effective else "None"
    elif tools:
        return ", ".join(tools)
    elif disallowed:
        return f"All tools except {', '.join(disallowed)}"
    return "All tools"


def format_agent_line(agent: AgentDefinition) -> str:
    """Format one agent line for the agent listing."""
    tools_desc = get_tools_description(agent)
    return f"- {agent.agent_type}: {agent.when_to_use} (Tools: {tools_desc})"


async def get_prompt(
    agent_definitions: List[AgentDefinition],
    is_coordinator: bool = False,
    allowed_agent_types: Optional[List[str]] = None,
) -> str:
    """Generate the prompt for the Agent tool."""
    # Filter agents by allowed types
    effective_agents = agent_definitions
    if allowed_agent_types:
        effective_agents = [a for a in agent_definitions if a.agent_type in allowed_agent_types]

    # Format agent list
    agent_list = "\n".join(format_agent_line(a) for a in effective_agents)

    shared = f"""Launch a new agent to handle complex, multi-step tasks autonomously.

The {AGENT_TOOL_NAME} tool launches specialized agents (subprocesses) that autonomously handle complex tasks. Each agent type has specific capabilities and tools available to it.

Available agent types and the tools they have access to:
{agent_list}

When using the {AGENT_TOOL_NAME} tool, specify a subagent_type parameter to select which agent type to use. If omitted, the general-purpose agent is used."""

    if is_coordinator:
        return shared

    # Full prompt for non-coordinator
    return f"""{shared}

When NOT to use the {AGENT_TOOL_NAME} tool:
- If you want to read a specific file path, use the Read tool or Glob tool instead of the {AGENT_TOOL_NAME} tool, to find the match more quickly
- If you are searching for a specific class definition like "class Foo", use Grep instead, to find the match more quickly
- If you are searching for code within a specific file or set of 2-3 files, use the Read tool instead of the {AGENT_TOOL_NAME} tool, to find the match more quickly
- Other tasks that are not related to the agent descriptions above

Usage notes:
- Always include a short description (3-5 words) summarizing what the agent will do
- When the agent is done, it will return a single message back to you. The result returned by the agent is not visible to the user. To show the user the result, you should send a text message back to the user with a concise summary of the result.
- You can optionally run agents in the background using the run_in_background parameter. When an agent runs in the background, you will be automatically notified when it completes — do NOT sleep, poll, or proactively check on its progress. Continue with other work or respond to the user instead.
- To continue a previously spawned agent, use SendMessage with the agent's ID or name as the `to` field. The agent resumes with its full context preserved.
- The agent's outputs should generally be trusted
- Clearly tell the agent whether you expect it to write code or just to do research (search, file reads, web fetches, etc.)
- If the user specifies that they want you to run agents "in parallel", you MUST send a single message with multiple {AGENT_TOOL_NAME} tool use content blocks.

Example usage:

<example>
user: "Please write a function that checks if a number is prime"
assistant: I'm going to use the Write tool to write the following code:
<code>
def is_prime(n):
    if n <= 1: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True
</code>
<commentary>
Since a significant piece of code was written and the task was completed, now use the Agent tool to launch a test-runner agent
</commentary>
assistant: Uses the {AGENT_TOOL_NAME} tool to launch the test-runner agent
</example>"""


__all__ = [
    "AGENT_TOOL_NAME",
    "AgentDefinition",
    "get_tools_description",
    "format_agent_line",
    "get_prompt",
]