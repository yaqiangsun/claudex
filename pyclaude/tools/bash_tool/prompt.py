"""Prompt for BashTool matching src/tools/BashTool/prompt.ts"""

BASH_TOOL_PROMPT = """You have access to a Bash tool for running shell commands.

## Usage

When you need to run shell commands, use the Bash tool with:
- command: The shell command to execute
- description: What the command does (optional)

## Examples

```
Use Bash tool to run: ls -la
Use Bash tool to run: git status
Use Bash tool to run: npm install
```

## Safety

- Commands that modify files require appropriate permissions
- Destructive commands (rm, dd, etc.) will be warned
- Some commands may require user confirmation
- The working directory persists between commands

## Common Commands

- ls, cd, pwd - Navigate directories
- cat, grep, find - Read/search files
- git - Version control
- npm, pip, cargo - Package management
- python, node - Run scripts

Always use the least destructive approach when possible.
"""


def get_bash_prompt() -> str:
    """Get the prompt for the Bash tool."""
    return BASH_TOOL_PROMPT


__all__ = ["BASH_TOOL_PROMPT", "get_bash_prompt"]