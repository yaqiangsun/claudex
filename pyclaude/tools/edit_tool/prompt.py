"""Prompt for EditTool matching src/tools/FileEditTool/prompt.ts"""

EDIT_TOOL_PROMPT = """You have access to an Edit tool for modifying files.

## Usage

Use the Edit tool to:
- Replace text in a file
- Insert new text
- Delete text

## Examples

```
Use Edit tool to replace: old_string with new_string in file.py
Use Edit tool to insert: new_function() after existing code
Use Edit tool to delete: the old implementation
```

## Guidelines

- Provide enough context in old_string for unique identification
- Use the exact text from the file including whitespace
- For multi-line edits, include the complete block
"""


def get_edit_prompt() -> str:
    """Get the prompt for the Edit tool."""
    return EDIT_TOOL_PROMPT


__all__ = ["EDIT_TOOL_PROMPT", "get_edit_prompt"]