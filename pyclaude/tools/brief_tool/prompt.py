"""Prompt for BriefTool matching src/tools/BriefTool/prompt.ts"""

BRIEF_TOOL_PROMPT = """You have access to a Brief tool for creating focused summaries.

## Usage

Use the Brief tool when you need to:
- Summarize long conversations or documents
- Extract key points from code
- Create concise summaries for reports

## Examples

```
Use Brief tool to summarize: The key findings from the research.
Use Brief tool to extract: The main arguments from this legal document.
```

The tool will analyze the input and provide a concise summary.
"""


def get_brief_prompt() -> str:
    """Get the prompt for the Brief tool."""
    return BRIEF_TOOL_PROMPT


__all__ = ["BRIEF_TOOL_PROMPT", "get_brief_prompt"]