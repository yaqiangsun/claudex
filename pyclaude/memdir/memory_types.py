"""Memory types."""
from typing import Literal


MemoryType = Literal['user', 'feedback', 'project', 'reference']

MEMORY_FRONTMATTER_EXAMPLE = [
    '```markdown',
    '---',
    'name: example_memory',
    'description: one-line description',
    'type: user',
    '---',
    '```',
]

TYPES_SECTION_INDIVIDUAL = [
    '## Types of memory',
    '',
    '- **user**: User role, preferences, goals',
    '- **feedback**: Guidance from the user about how to approach work',
    '- **project**: Project-specific context, deadlines, decisions',
    '- **reference**: External system pointers',
]

WHAT_NOT_TO_SAVE_SECTION = [
    '## What NOT to save in memory',
    '',
    '- Code patterns, conventions, architecture - derivable from code',
    '- Git history, recent changes - derivable from git',
    '- Debugging solutions - the fix is in the code',
    '- Anything in CLAUDE.md files',
    '- Ephemeral task details',
]

WHEN_TO_ACCESS_SECTION = [
    '## When to access memories',
    '',
    'When memories seem relevant, or the user references prior-conversation work.',
]

TRUSTING_RECALL_SECTION = [
    '## Trusting your recall',
    '',
    'Memory records can become stale over time. Use memory as context for what was true at a given point in time.',
]

__all__ = [
    'MemoryType',
    'MEMORY_FRONTMATTER_EXAMPLE',
    'TYPES_SECTION_INDIVIDUAL',
    'WHAT_NOT_TO_SAVE_SECTION',
    'WHEN_TO_ACCESS_SECTION',
    'TRUSTING_RECALL_SECTION',
]