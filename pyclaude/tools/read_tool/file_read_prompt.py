"""Prompt for FileReadTool matching src/tools/FileReadTool/prompt.ts"""

FILE_READ_TOOL_PROMPT = """You have access to a Read tool for reading files from the filesystem.

## Usage

Use the Read tool to:
- Read file contents
- View specific line ranges
- Read images (encoded as base64)

## Examples

```
Use Read tool to read: path/to/file.py
Use Read tool to read: file.ts with offset 10 and limit 50
```

## Parameters

- file_path: Path to the file to read
- offset: Line number to start from (optional)
- limit: Number of lines to read (optional)
"""


def get_read_prompt() -> str:
    """Get the prompt for the Read tool."""
    return FILE_READ_TOOL_PROMPT


__all__ = ["FILE_READ_TOOL_PROMPT", "get_read_prompt"]