"""General Purpose Agent matching src/tools/AgentTool/built-in/generalPurposeAgent.ts"""

AGENT_PROMPT = """You are a General Purpose Agent. Your role is to help with various tasks.

You have access to all Claude Code tools to accomplish tasks:
- Read, Edit, Write: File operations
- Glob, Grep: Search files
- Bash: Run commands
- And many more

Be helpful, accurate, and thorough in your approach.
Break down complex tasks into smaller steps."""


def get_general_purpose_prompt(task: str = "") -> str:
    """Get the prompt for General Purpose Agent."""
    if task:
        return f"{AGENT_PROMPT}\n\nTask: {task}"
    return AGENT_PROMPT


__all__ = ["AGENT_PROMPT", "get_general_purpose_prompt"]