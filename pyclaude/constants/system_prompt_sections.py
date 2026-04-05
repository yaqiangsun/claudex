"""System prompt sections."""

SYSTEM_PROMPT_SECTIONS = [
    {
        'id': 'capabilities',
        'title': 'Capabilities',
        'content': 'You can read, edit, and create files, run commands, and use tools.',
    },
    {
        'id': 'guidelines',
        'title': 'Guidelines',
        'content': 'Be concise, helpful, and focus on the task at hand.',
    },
    {
        'id': 'limitations',
        'title': 'Limitations',
        'content': 'You cannot browse the web or run commands that require user interaction.',
    },
]


def get_system_prompt_section(section_id: str) -> dict:
    """Get a system prompt section by ID."""
    for section in SYSTEM_PROMPT_SECTIONS:
        if section['id'] == section_id:
            return section
    return {}


__all__ = ['SYSTEM_PROMPT_SECTIONS', 'get_system_prompt_section']