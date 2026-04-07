"""Prompt for LSPTool matching src/tools/LSPTool/prompt.ts"""

LSP_TOOL_PROMPT = """You have access to an LSP tool for Language Server Protocol operations.

## Usage

Use the LSP tool to:
- Find symbol definitions
- Find references to symbols
- Get code completions
- Format code

## Examples

```
Use LSP tool to find definition of functionName
Use LSP tool to find all references to Variable
Use LSP tool to format current file
```

## Features

- Go to definition
- Find references
- Code actions
- Format document
- Rename symbol
"""


def get_lsp_prompt() -> str:
    """Get the prompt for the LSP tool."""
    return LSP_TOOL_PROMPT


__all__ = ["LSP_TOOL_PROMPT", "get_lsp_prompt"]