"""Prompt for WebFetchTool matching src/tools/WebFetchTool/prompt.ts"""

WEB_FETCH_TOOL_PROMPT = """You have access to a WebFetch tool for fetching web content.

## Usage

Use the WebFetch tool to:
- Fetch content from URLs
- Extract text from web pages
- Get specific sections from articles

## Examples

```
Use WebFetch tool to fetch: https://example.com/article
Use WebFetch tool to extract: main content from https://news.site.com
```

## Guidelines

- Only fetch from preapproved domains
- Respect rate limits
- Extract relevant content
"""


def get_web_fetch_prompt() -> str:
    """Get the prompt for the WebFetch tool."""
    return WEB_FETCH_TOOL_PROMPT


__all__ = ["WEB_FETCH_TOOL_PROMPT", "get_web_fetch_prompt"]