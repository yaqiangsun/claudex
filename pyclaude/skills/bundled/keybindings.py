"""Keybindings Skill - Python implementation of src/skills/bundled/keybindings.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


def is_keybinding_customization_enabled() -> bool:
    """Check if keybinding customization is enabled."""
    try:
        from pyclaude.keybindings.load_user_bindings import is_keybinding_customization_enabled
        return is_keybinding_customization_enabled()
    except ImportError:
        return False


SECTION_INTRO = """# Keybindings Skill

Create or modify `~/.claude/keybindings.json` to customize keyboard shortcuts.

## CRITICAL: Read Before Write

**Always read `~/.claude/keybindings.json` first** (it may not exist yet). Merge changes with existing bindings.
"""

SECTION_FILE_FORMAT = """## File Format
```json
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor"
      }
    }
  ]
}
```
"""

SECTION_KEYSTROKE_SYNTAX = """## Keystroke Syntax

**Modifiers** (combine with `+`):
- `ctrl` (alias: `control`)
- `alt` (aliases: `opt`, `option`)
- `shift`
- `meta` (aliases: `cmd`, `command`)

**Special keys**: `escape`, `enter`, `return`, `tab`, `space`, `backspace`, `delete`, `up`, `down`, `left`, `right`

**Chords**: Space-separated keystrokes, e.g. `ctrl+k ctrl+s`
"""

SECTION_UNBINDING = """## Unbinding Default Shortcuts
Set a key to `null` to remove its default binding:
```json
{
  "context": "Chat",
  "bindings": {
    "ctrl+s": null
  }
}
```
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    """Get keybindings skill prompt."""
    sections = [
        SECTION_INTRO,
        SECTION_FILE_FORMAT,
        SECTION_KEYSTROKE_SYNTAX,
        SECTION_UNBINDING,
        """## Behavioral Rules
1. Only include contexts the user wants to change
2. Validate that actions and contexts are known
3. Warn about reserved shortcuts
4. New bindings are additive
""",
    ]

    if args:
        sections.append(f'## User Request\n\n{args}')

    return [{'type': 'text', 'text': '\n\n'.join(sections)}]


def register() -> None:
    """Register the keybindings-help skill."""
    register_bundled_skill(BundledSkillDefinition(
        name='keybindings-help',
        description='Use when the user wants to customize keyboard shortcuts, rebind keys, or modify keybindings.json.',
        allowed_tools=['Read'],
        user_invocable=False,
        is_enabled=is_keybinding_customization_enabled,
        get_prompt_for_command=get_prompt,
    ))