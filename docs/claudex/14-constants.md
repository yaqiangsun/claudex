# 14 - 常量定义

对应 TypeScript: `src/constants/` - 22 个常量文件

## 14.1 常量分类

```python
# pyclaude/constants/__init__.py
from pyclaude.constants.api_limits import *
from pyclaude.constants.tool_limits import *
from pyclaude.constants.prompts import *
from pyclaude.constants.keys import *
```

## 14.2 API 限制

```python
# pyclaude/constants/api_limits.py
from dataclasses import dataclass


@dataclass
class APILimits:
    """API 限制"""
    MAX_TOKENS_PER_REQUEST: int = 8192
    MAX_CONTEXT_WINDOW: int = 200000
    MAX_TOOLS_PER_REQUEST: int = 1000
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 50
    RATE_LIMIT_TOKENS_PER_MINUTE: int = 100000


# 全局常量
API_LIMITS = APILimits()
DEFAULT_MAX_TOKENS = 8192
DEFAULT_TEMPERATURE = 1.0
DEFAULT_MODEL = "claude-sonnet-4-20250514"
```

## 14.3 工具限制

```python
# pyclaude/constants/tool_limits.py
TOOL_NAME_MAX_LENGTH = 64
TOOL_DESCRIPTION_MAX_LENGTH = 300
INPUT_SCHEMA_MAX_DEPTH = 10
MAX_CONCURRENT_TOOL_CALLS = 10
TOOL_TIMEOUT_SECONDS = 300
```

## 14.4 提示词

```python
# pyclaude/constants/prompts.py
SYSTEM_PROMPT = """You are Claude Code, an AI programming assistant.

You have access to a set of tools for interacting with the file system, running commands, and other tasks.

When you write code, prefer clean, maintainable solutions. When refactoring, preserve the original intent.

You should:
1. Understand the user's goal before taking action
2. Ask clarifying questions when needed
3. Explain your reasoning when making significant changes
4. Admit when you don't know something

Available tools: {tools_list}
"""

TOOL_USE_PROMPT = """You have used the {tool_name} tool. Here's the result:

{result}

Please continue your response."""

ERROR_PROMPT = """An error occurred:

{error}

Please handle this error appropriately and continue if possible."""

CONTEXT_COMPRESSION_PROMPT = """Please summarize the following conversation, preserving key context and decisions:

{conversation}

Summary should include:
1. Main topics discussed
2. Decisions made
3. Outstanding tasks
4. Important context"""
```

## 14.5 快捷键

```python
# pyclaude/constants/keybindings.py
from typing import dict

DEFAULT_KEYBINDINGS: dict[str, str] = {
    "ctrl+c": "quit",
    "ctrl+l": "clear",
    "ctrl+n": "new_session",
    "ctrl+p": "prev_command",
    "ctrl+a": "beginning_of_line",
    "ctrl+e": "end_of_line",
    "ctrl+u": "clear_line",
    "ctrl+w": "delete_word",
    "ctrl+r": "search_history",
    "tab": "complete",
    "up": "prev_history",
    "down": "next_history",
}

VIM_KEYBINDINGS: dict[str, str] = {
    "i": "insert_mode",
    "esc": "normal_mode",
    ":": "command_mode",
    "dd": "delete_line",
    "yy": "yank_line",
    "p": "paste",
    "u": "undo",
    "ctrl+r": "redo",
}
```

## 14.6 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `apiLimits` | `APILimits` | `pyclaude/constants/api_limits.py` |
| `toolLimits` | 常量 | `pyclaude/constants/tool_limits.py` |
| `prompts` | 提示词 | `pyclaude/constants/prompts.py` |
| `keybindings` | `DEFAULT_KEYBINDINGS` | `pyclaude/constants/keybindings.py` |