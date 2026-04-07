"""Built-in agents matching src/tools/AgentTool/builtInAgents.ts"""
from typing import Dict, Any, Optional, Callable


class BuiltInAgents:
    """Registry of built-in agent types."""

    AGENTS = {
        "general-purpose": {
            "name": "General Purpose Agent",
            "description": "A general purpose agent for various tasks",
            "prompt_template": "You are a helpful assistant.",
        },
        "explore": {
            "name": "Explore Agent",
            "description": "Explores codebase and gathers information",
            "prompt_template": "Explore the codebase and provide information about {topic}.",
        },
        "plan": {
            "name": "Plan Agent",
            "description": "Creates implementation plans",
            "prompt_template": "Create a detailed implementation plan for: {task}",
        },
        "verification": {
            "name": "Verification Agent",
            "description": "Verifies code changes",
            "prompt_template": "Verify the following changes: {changes}",
        },
        "claude-code-guide": {
            "name": "Claude Code Guide Agent",
            "description": "Answers questions about Claude Code",
            "prompt_template": "Answer questions about Claude Code CLI.",
        },
        "statusline-setup": {
            "name": "Statusline Setup Agent",
            "description": "Configures statusline settings",
            "prompt_template": "Set up the statusline configuration.",
        },
    }

    @classmethod
    def get_agent(cls, agent_type: str) -> Optional[Dict[str, Any]]:
        """Get agent configuration by type."""
        return cls.AGENTS.get(agent_type)

    @classmethod
    def list_agents(cls) -> Dict[str, Dict[str, str]]:
        """List all available built-in agents."""
        return cls.AGENTS

    @classmethod
    def is_built_in(cls, agent_type: str) -> bool:
        """Check if an agent type is built-in."""
        return agent_type in cls.AGENTS


__all__ = ["BuiltInAgents"]