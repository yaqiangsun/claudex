"""Claude In Chrome Skill - Python implementation of src/skills/bundled/claudeInChrome.ts

This skill provides Chrome browser automation tools.
Requires MCP server 'claude-in-chrome' to be configured.
"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


# Base Chrome prompt for browser automation
BASE_CHROME_PROMPT = """# Chrome Browser Automation

You have access to Chrome browser automation tools that can:
- Click elements on web pages
- Fill forms and input text
- Capture screenshots
- Read console logs
- Navigate to URLs
- And more browser interactions

## Getting Started
Call mcp__claude-in-chrome__tabs_context_mcp to get information about
the user's current browser tabs before performing any actions.
"""

SKILL_ACTIVATION_MESSAGE = """
Now that this skill is invoked, you have access to Chrome browser automation tools.
You can now use the mcp__claude-in-chrome__* tools to interact with web pages.

IMPORTANT: Start by calling mcp__claude-in-chrome__tabs_context_mcp to get information
about the user's current browser tabs.
"""

# MCP tools available from claude-in-chrome
# Note: These are dynamically discovered from the MCP server at runtime
CLAUDE_IN_CHROME_MCP_TOOLS = [
    'mcp__claude-in-chrome__tabs_context_mcp',
    'mcp__claude-in-chrome__click_element',
    'mcp__claude-in-chrome__type_text',
    'mcp__claude-in-chrome__get_visible_text',
    'mcp__claude-in-chrome__screenshot',
    # ... additional tools available from the MCP server
]


def should_auto_enable_claude_in_chrome() -> bool:
    """Check if Claude in Chrome should be auto-enabled.

    In the original TS, this checks for Chrome extension configuration.
    For now, returns False as it requires platform-specific setup.
    """
    # TODO: Implement proper detection based on Chrome extension/MCP setup
    return False


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get claude-in-chrome skill prompt."""
    prompt = f"{BASE_CHROME_PROMPT}\n{SKILL_ACTIVATION_MESSAGE}"
    if args:
        prompt += f"\n## Task\n\n{args}"
    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the claude-in-chrome skill.

    This skill is only enabled when Claude in Chrome is configured.
    """
    if not should_auto_enable_claude_in_chrome():
        return

    register_bundled_skill(BundledSkillDefinition(
        name='claude-in-chrome',
        description=(
            'Automates your Chrome browser to interact with web pages - clicking elements, '
            'filling forms, capturing screenshots, reading console logs, and navigating sites. '
            'Opens pages in new tabs within your existing Chrome session. '
            'Requires site-level permissions before executing (configured in the extension).'
        ),
        when_to_use=(
            'When the user wants to interact with web pages, automate browser tasks, '
            'capture screenshots, read console logs, or perform any browser-based actions. '
            'Always invoke BEFORE attempting to use any mcp__claude-in-chrome__* tools.'
        ),
        allowed_tools=CLAUDE_IN_CHROME_MCP_TOOLS,
        user_invocable=True,
        is_enabled=should_auto_enable_claude_in_chrome,
        get_prompt_for_command=get_prompt,
    ))