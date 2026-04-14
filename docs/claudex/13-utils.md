# 13 - 工具库

对应 TypeScript: `src/utils/` - 329 个工具函数

## 13.1 工具函数分类

Python 版本将按照功能分类组织工具函数：

```
pyclaude/utils/
├── __init__.py
├── bash/          # Bash 相关工具
├── git/           # Git 操作工具
├── permissions/   # 权限检查工具
├── messages/      # 消息处理工具
├── model/         # 模型相关工具
├── files/         # 文件操作工具
├── strings/       # 字符串处理工具
├── dates/         # 日期处理工具
└── ...
```

## 13.2 核心工具模块

### 13.2.1 Bash 工具

```python
# pyclaude/utils/bash.py
import asyncio
from typing import Optional, tuple


async def run_bash(
    command: str,
    cwd: Optional[str] = None,
    env: Optional[dict] = None,
    timeout: Optional[int] = None,
) -> tuple[int, str, str]:
    """执行 Bash 命令

    Returns:
        (exit_code, stdout, stderr)
    """
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
        env=env,
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout,
        )
        return (
            process.returncode or 0,
            stdout.decode("utf-8"),
            stderr.decode("utf-8"),
        )
    except asyncio.TimeoutError:
        process.kill()
        raise


def escape_shell_arg(arg: str) -> str:
    """转义 shell 参数"""
    return f"'{arg.replace("'", "'\\''")}'"


def is_dangerous_command(command: str) -> bool:
    """检查是否为危险命令"""
    dangerous = [
        "rm -rf",
        "dd if=",
        ":(){:|:&};:",
        "mkfs",
        "> /dev/sda",
        "chmod -R 777",
        "chown -R",
    ]
    return any(d in command for d in dangerous)
```

### 13.2.2 Git 工具

```python
# pyclaude/utils/git.py
import asyncio
from typing import Optional
from dataclasses import dataclass


@dataclass
class GitStatus:
    """Git 状态"""
    branch: str
    staged: list[str]
    modified: list[str]
    untracked: list[str]
    conflicted: list[str]


async def get_git_root(path: str = ".") -> Optional[str]:
    """获取 Git 根目录"""
    exit_code, stdout, _ = await run_bash("git rev-parse --show-toplevel", cwd=path)
    return stdout.strip() if exit_code == 0 else None


async def get_git_status(path: str = ".") -> Optional[GitStatus]:
    """获取 Git 状态"""
    exit_code, stdout, _ = await run_bash("git status --porcelain", cwd=path)
    if exit_code != 0:
        return None

    staged, modified, untracked, conflicted = [], [], [], []

    for line in stdout.strip().split("\n"):
        if not line:
            continue
        status = line[:2]
        file = line[3:]

        if status[0] in "MARC":
            staged.append(file)
        if status[1] == "M":
            modified.append(file)
        if status == "??":
            untracked.append(file)
        if "UU" in status:
            conflicted.append(file)

    # 获取当前分支
    _, branch, _ = await run_bash("git branch --show-current", cwd=path)

    return GitStatus(
        branch=branch.strip(),
        staged=staged,
        modified=modified,
        untracked=untracked,
        conflicted=conflicted,
    )


async def get_git_diff(path: str = ".") -> str:
    """获取 Git diff"""
    _, stdout, _ = await run_bash("git diff", cwd=path)
    return stdout


async def git_commit(message: str, path: str = ".") -> bool:
    """执行 git commit"""
    exit_code, _, _ = await run_bash(f'git commit -m "{message}"', cwd=path)
    return exit_code == 0
```

### 13.2.3 消息处理工具

```python
# pyclaude/utils/messages.py
from typing import Optional
import re


def extract_code_blocks(text: str) -> list[tuple[str, str]]:
    """提取代码块

    Returns:
        [(language, code), ...]
    """
    pattern = r"```(\w*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def format_message(role: str, content: str) -> dict:
    """格式化消息"""
    return {
        "role": role,
        "content": content,
    }


def truncate_content(content: str, max_length: int = 1000) -> str:
    """截断内容"""
    if len(content) <= max_length:
        return content
    return content[:max_length] + f"\n... (truncated, {len(content)} total)"


def escapeMarkdown(text: str) -> str:
    """转义 Markdown 特殊字符"""
    special = r"\_*[]()#+.!-"
    for char in special:
        text = text.replace(char, f"\\{char}")
    return text
```

### 13.2.4 权限检查工具

```python
# pyclaude/utils/permissions.py
from pathlib import Path
from typing import Optional


PROTECTED_PATHS = [
    "/etc/passwd",
    "/etc/shadow",
    "/etc/sudoers",
    "~/.ssh",
]


def is_protected_path(path: str) -> bool:
    """检查是否为保护路径"""
    p = Path(path).resolve()
    for protected in PROTECTED_PATHS:
        if str(p).startswith(str(Path(protected).expanduser())):
            return True
    return False


def check_file_permission(path: str, write: bool = False) -> bool:
    """检查文件权限"""
    p = Path(path)
    if not p.exists():
        # 文件不存在，检查父目录
        p = p.parent

    if write:
        return p.stat().st_mode & 0o200 != 0
    return p.exists() and p.is_file()


def is_binary_file(path: str) -> bool:
    """检查是否为二进制文件"""
    binary_extensions = {
        ".exe", ".dll", ".so", ".dylib", ".o", ".a",
        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico",
        ".pdf", ".zip", ".tar", ".gz", ".7z", ".rar",
        ".mp3", ".mp4", ".wav", ".avi", ".mov",
    }
    return Path(path).suffix.lower() in binary_extensions
```

### 13.2.5 模型工具

```python
# pyclaude/utils/model.py
from typing import Optional
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """模型信息"""
    name: str
    context_window: int
    max_output_tokens: int
    supports_tools: bool


MODELS = {
    "claude-opus-4-6": ModelInfo(
        name="claude-opus-4-6",
        context_window=200000,
        max_output_tokens=8192,
        supports_tools=True,
    ),
    "claude-sonnet-4-6": ModelInfo(
        name="claude-sonnet-4-6",
        context_window=200000,
        max_output_tokens=8192,
        supports_tools=True,
    ),
    "claude-haiku-4-5": ModelInfo(
        name="claude-haiku-4-5-20251001",
        context_window=200000,
        max_output_tokens=8192,
        supports_tools=True,
    ),
}


def get_model_info(model: str) -> Optional[ModelInfo]:
    """获取模型信息"""
    return MODELS.get(model)


def estimate_tokens(text: str) -> int:
    """估算 token 数量"""
    # 简单估算: ~4 字符 = 1 token
    return len(text) // 4


def calculate_max_input_tokens(model: str, max_output: int = 8192) -> int:
    """计算最大输入 token"""
    info = get_model_info(model)
    if not info:
        return 100000
    return info.context_window - max_output
```

## 13.3 模块接口清单

| TypeScript 目录 | Python 模块 |
|-----------------|-------------|
| `utils/bash/` | `pyclaude/utils/bash.py` |
| `utils/git/` | `pyclaude/utils/git.py` |
| `utils/permissions/` | `pyclaude/utils/permissions.py` |
| `utils/messages/` | `pyclaude/utils/messages.py` |
| `utils/model/` | `pyclaude/utils/model.py` |
| `utils/files/` | `pyclaude/utils/files.py` |
| `utils/strings/` | `pyclaude/utils/strings.py` |