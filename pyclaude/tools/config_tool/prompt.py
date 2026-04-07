"""Prompt for ConfigTool matching src/tools/ConfigTool/prompt.ts"""

CONFIG_TOOL_PROMPT = """You have access to a Config tool for viewing and modifying Claude Code settings.

## Usage

Use the Config tool to:
- View current configuration
- Update settings
- Add or remove configuration options

## Settings

- autoApprove: Automatically approve safe commands
- model: Default AI model
- maxTokens: Maximum response tokens
- temperature: Model creativity
- theme: UI appearance
- terminalShell: Default shell

## Examples

```
Use Config tool to view current settings.
Use Config tool to set autoApprove to true.
Use Config tool to change model to claude-opus-4-6.
```
"""


def get_config_prompt() -> str:
    """Get the prompt for the Config tool."""
    return CONFIG_TOOL_PROMPT


__all__ = ["CONFIG_TOOL_PROMPT", "get_config_prompt"]