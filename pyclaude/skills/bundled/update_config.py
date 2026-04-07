"""Update Config Skill - Python implementation of src/skills/bundled/updateConfig.ts"""
from __future__ import annotations
from typing import Any

from pyclaude.skills.bundled import BundledSkillDefinition, register_bundled_skill


SETTINGS_EXAMPLES_DOCS = """## Settings File Locations

Choose the appropriate file based on scope:

| File | Scope | Git | Use For |
|------|-------|-----|---------|
| `~/.claude/settings.json` | Global | N/A | Personal preferences for all projects |
| `.claude/settings.json` | Project | Commit | Team-wide hooks, permissions, plugins |
| `.claude/settings.local.json` | Project | Gitignore | Personal overrides for this project |

Settings load in order: user → project → local (later overrides earlier).

## Settings Schema Reference

### Permissions
```json
{
  "permissions": {
    "allow": ["Bash(npm:*)", "Edit(.claude)", "Read"],
    "deny": ["Bash(rm -rf:*)"],
    "ask": ["Write(/etc/*)"],
    "defaultMode": "default" | "plan" | "acceptEdits" | "dontAsk",
    "additionalDirectories": ["/extra/dir"]
  }
}
```

### Environment Variables
```json
{
  "env": {
    "DEBUG": "true",
    "MY_API_KEY": "value"
  }
}
```

### Model & Agent
```json
{
  "model": "sonnet",
  "agent": "agent-name",
  "alwaysThinkingEnabled": true
}
```

### Attribution (Commits & PRs)
```json
{
  "attribution": {
    "commit": "Custom commit trailer text",
    "pr": "Custom PR description text"
  }
}
```

### MCP Server Management
```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["server1", "server2"],
  "disabledMcpjsonServers": ["blocked-server"]
}
```

### Plugins
```json
{
  "enabledPlugins": {
    "formatter@anthropic-tools": true
  }
}
```

### Other Settings
- `language`: Preferred response language
- `cleanupPeriodDays`: Days to keep transcripts (default: 30)
- `respectGitignore`: Whether to respect .gitignore (default: true)
"""

HOOKS_DOCS = """## Hooks Configuration

Hooks run commands at specific points in Claude Code's lifecycle.

### Hook Structure
```json
{
  "hooks": {
    "EVENT_NAME": [
      {
        "matcher": "ToolName|OtherTool",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here",
            "timeout": 60,
            "statusMessage": "Running..."
          }
        ]
      }
    ]
  }
}
```

### Hook Events
- PermissionRequest - Run before permission prompt
- PreToolUse - Run before tool, can block
- PostToolUse - Run after successful tool
- PostToolUseFailure - Run after tool fails
- Notification - Run on notifications
- Stop - Run when Claude stops
- PreCompact/PostCompact - Before/after compaction
- UserPromptSubmit - When user submits
- SessionStart - When session starts

### Hook Types
1. **Command Hook** - Runs a shell command
2. **Prompt Hook** - Evaluates a condition with LLM
3. **Agent Hook** - Runs an agent with tools
"""

UPDATE_CONFIG_PROMPT = f"""# Update Config Skill

Modify Claude Code configuration by updating settings.json files.

## When Hooks Are Required (Not Memory)

If the user wants something to happen automatically in response to an EVENT, they need a **hook** configured in settings.json.

**These require hooks:**
- "Before compacting, ask me what to preserve" → PreCompact hook
- "After writing files, run prettier" → PostToolUse hook
- "When I run bash commands, log them" → PreToolUse hook

## CRITICAL: Read Before Write

**Always read the existing settings file before making changes.** Merge new settings with existing ones.

## CRITICAL: Use AskUserQuestion for Ambiguity

When the user's request is ambiguous, use AskUserQuestion.

## Decision: Config Tool vs Direct Edit

**Use the Config tool** for: theme, editorMode, verbose, model, language, alwaysThinkingEnabled, permissions.defaultMode

**Edit settings.json directly** for: hooks, permissions rules, env vars, MCP config, plugins

## Workflow
1. Clarify intent
2. Read existing file
3. Merge carefully
4. Edit file
5. Confirm

{SETTINGS_EXAMPLES_DOCS}

{HOOKS_DOCS}

## Example Workflows

### Adding a Hook
User: "Format my code after Claude writes it"
1. Clarify: Which formatter? (prettier, gofmt, etc.)
2. Read: .claude/settings.json (or create if missing)
3. Merge: Add to existing hooks

### Adding Permissions
User: "Allow npm commands without prompting"
1. Read: Existing permissions
2. Merge: Add Bash(npm:*) to allow array
"""


def get_prompt(args: str = '') -> list[dict[str, Any]]:
    if args.startswith('[hooks-only]'):
        req = args[len('[hooks-only]'):].strip()
        prompt = HOOKS_DOCS
        if req:
            prompt += f'\n\n## Task\n\n{req}'
        return [{'type': 'text', 'text': prompt}]

    prompt = UPDATE_CONFIG_PROMPT
    if args:
        prompt += f'\n\n## User Request\n\n{args}'

    return [{'type': 'text', 'text': prompt}]


def register() -> None:
    """Register the update-config skill."""
    register_bundled_skill(BundledSkillDefinition(
        name='update-config',
        description='Use this skill to configure Claude Code via settings.json. For permissions, env vars, hooks, or any settings.json changes.',
        allowed_tools=['Read'],
        user_invocable=True,
        get_prompt_for_command=get_prompt,
    ))