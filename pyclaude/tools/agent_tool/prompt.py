"""Prompt for AgentTool matching src/tools/AgentTool/prompt.ts"""

AGENT_TOOL_PROMPT = """You have access to an Agent tool that can spawn sub-agents to handle tasks.

## Usage

When you need to delegate work to a sub-agent, use the Agent tool with:
- name: The agent's name or type
- prompt: What the agent should do
- mode: "parallel" for independent tasks, "sequential" for dependent tasks

## Agent Types

- **general-purpose**: A general assistant for various tasks
- **explore**: Explore and analyze codebase
- **plan**: Create implementation plans
- **verification**: Verify code changes
- **custom**: Use your own prompt

## Examples

```
Use Agent tool to explore the codebase structure.
Use Agent tool to create a plan for implementing feature X.
Use Agent tool to verify that the tests pass.
```

The agent will report back with its results when complete.
"""


def get_agent_prompt() -> str:
    """Get the prompt for the Agent tool."""
    return AGENT_TOOL_PROMPT


__all__ = ["AGENT_TOOL_PROMPT", "get_agent_prompt"]