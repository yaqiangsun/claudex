"""Claude API Skill - Python implementation of src/skills/bundled/claudeApi.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


PROMPT = """# Claude API Skill

Build apps with the Claude API or Anthropic SDK.

## Your Task
Help the user build applications using the Claude API.

## Detecting Language
Look for:
- Python: .py, requirements.txt, pyproject.toml
- TypeScript: .ts, .tsx, package.json
- Java: .java, pom.xml, build.gradle
- Go: .go, go.mod
- Ruby: .rb, Gemfile

## Common Tasks
- Single classification/summarization/extraction → use messages API
- Chat UI with streaming → use streaming responses
- Long conversations → use compaction strategies
- Prompt caching → implement cache controls
- Function calling → use tools
- Batch processing → use batch API
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get claude-api skill prompt."""
    prompt = PROMPT
    # Note: In full implementation, would detect language and include relevant docs
    if args:
        prompt += f'\n\n## User Request\n\n{args}'
    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the claude-api skill (BUILDING_CLAUDE_APPS feature)."""
    # Note: In full implementation, would lazy-load content from claudeApiContent
    # and detect language from project files
    register_bundled_skill(BundledSkillDefinition(
        name='claude-api',
        description='Build apps with the Claude API or Anthropic SDK. Trigger when user asks about Claude API, Anthropic SDKs, or Agent SDK.',
        allowed_tools=['Read', 'Grep', 'Glob', 'WebFetch'],
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))