# 03 - 命令系统

对应 TypeScript: `src/commands.ts` + `src/commands/`

## 3.1 命令注册表

### 功能
- 命令注册与发现
- 命令解析与路由
- 命令执行

### Python 实现

```python
# pyclaude/commands/registry.py
from abc import ABC, abstractmethod
from typing import Optional, Any, Callable, Awaitable
from dataclasses import dataclass
from enum import Enum


class CommandType(str, Enum):
    """命令类型"""
    PROMPT = "prompt"           # 需要发送到 AI 的命令
    LOCAL = "local"             # 本地执行的命令
    LOCAL_JSX = "local-jsx"     # 本地 JSX 命令（返回 UI）


@dataclass
class Command:
    """命令定义"""
    name: str
    description: str
    command_type: CommandType
    aliases: list[str]
    handler: Callable[..., Awaitable[str]]
    parser: Optional[Callable[[str], dict[str, Any]]] = None


class CommandRegistry:
    """命令注册表"""

    def __init__(self):
        self.commands: dict[str, Command] = {}
        self._load_builtin_commands()

    def register(self, command: Command) -> None:
        """注册命令"""
        self.commands[command.name] = command
        for alias in command.aliases:
            self.commands[alias] = command

    def get(self, name: str) -> Optional[Command]:
        """获取命令"""
        return self.commands.get(name)

    def list_commands(self) -> list[Command]:
        """列出所有命令"""
        return list(self.commands.values())

    async def execute(self, name: str, args: dict[str, Any]) -> str:
        """执行命令"""
        command = self.get(name)
        if not command:
            raise ValueError(f"Command not found: {name}")
        return await command.handler(**args)

    async def parse(self, user_input: str) -> Optional[str]:
        """解析用户输入，返回命令结果如果匹配"""
        for command in self.commands.values():
            for alias in [command.name] + command.aliases:
                if user_input.strip().startswith(f"/{alias}"):
                    # 解析参数
                    args = {"input": user_input}
                    if command.parser:
                        args = command.parser(user_input)
                    return await self.execute(command.name, args)
        return None

    def _load_builtin_commands(self) -> None:
        """加载内置命令"""
        from pyclaude.commands import (
            CommitCommand,
            ConfigCommand,
            BranchCommand,
            ClearCommand,
            MCPCommand,
        )
        for cmd_class in [CommitCommand, ConfigCommand, BranchCommand, ClearCommand, MCPCommand]:
            cmd = cmd_class()
            self.register(cmd.get_command())
```

## 3.2 命令基类

```python
# pyclaude/commands/base.py
from abc import ABC, abstractmethod
from typing import Any, Callable, Awaitable
from pyclaude.commands.registry import Command, CommandType


class BaseCommand(ABC):
    """命令基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """命令名称"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """命令描述"""
        pass

    @property
    @abstractmethod
    def aliases(self) -> list[str]:
        """命令别名"""
        pass

    @property
    @abstractmethod
    def command_type(self) -> CommandType:
        """命令类型"""
        pass

    @abstractmethod
    async def execute(self, input: str, **kwargs) -> str:
        """执行命令"""
        pass

    def get_command(self) -> Command:
        """获取命令定义"""
        return Command(
            name=self.name,
            description=self.description,
            command_type=self.command_type,
            aliases=self.aliases,
            handler=self.execute,
        )
```

## 3.3 内置命令实现

对应 TypeScript: `src/commands/` 下 100+ 命令

### 核心命令示例

```python
# pclaude/commands/commit.py
from pyclaude.commands.base import BaseCommand
from pyclaude.commands.registry import CommandType


class CommitCommand(BaseCommand):
    """Git commit 命令"""

    @property
    def name(self) -> str:
        return "commit"

    @property
    def description(self) -> str:
        return "Create a git commit with auto-generated message"

    @property
    def aliases(self) -> list[str]:
        return ["c"]

    @property
    def command_type(self) -> CommandType:
        return CommandType.LOCAL

    async def execute(self, input: str, **kwargs) -> str:
        # 实现 git commit 逻辑
        return "Commit created successfully"


# pyclaude/commands/config.py
class ConfigCommand(BaseCommand):
    """配置管理命令"""

    @property
    def name(self) -> str:
        return "config"

    @property
    def description(self) -> str:
        return "Manage Claude Code configuration"

    @property
    def aliases(self) -> list[str]:
        return ["cfg"]

    @property
    def command_type(self) -> CommandType:
        return CommandType.LOCAL

    async def execute(self, input: str, **kwargs) -> str:
        # 实现配置管理逻辑
        action = kwargs.get("action", "get")
        if action == "get":
            return self._get_config()
        elif action == "set":
            return self._set_config(kwargs.get("key"), kwargs.get("value"))
        return "Unknown action"


# pyclaude/commands/branch.py
class BranchCommand(BaseCommand):
    """Git branch 命令"""

    @property
    def name(self) -> str:
        return "branch"

    @property
    def description(self) -> str:
        return "Manage git branches"

    @property
    def aliases(self) -> list[str]:
        return ["br"]

    @property
    def command_type(self) -> CommandType:
        return CommandType.LOCAL

    async def execute(self, input: str, **kwargs) -> str:
        # 实现 branch 逻辑
        pass


# pyclaude/commands/clear.py
class ClearCommand(BaseCommand):
    """清除屏幕命令"""

    @property
    def name(self) -> str:
        return "clear"

    @property
    def description(self) -> str:
        return "Clear the screen"

    @property
    def aliases(self) -> list[str]:
        return ["cl"]

    @property
    def command_type(self) -> CommandType:
        return CommandType.LOCAL

    async def execute(self, input: str, **kwargs) -> str:
        return "\033[2J\033[H"  # ANSI escape to clear screen
```

### 命令分类

| 类别 | 命令示例 |
|------|----------|
| **Git** | commit, branch, checkout, status, diff, log, pull, push |
| **配置** | config, set, get, reset |
| **MCP** | mcp, mcp-add, mcp-remove |
| **工具** | skills, tools, permissions |
| **会话** | clear, new, resume, session |
| **调试** | debug, test, lint |

## 3.4 命令加载器

对应 TypeScript: `commands.ts` 中的加载逻辑

```python
# pyclaude/commands/loader.py
from pathlib import Path
from typing import Optional
import importlib
import importlib.util


class CommandLoader:
    """命令加载器"""

    def __init__(self):
        self.loaded: set[str] = set()

    def load_from_directory(self, directory: Path) -> None:
        """从目录加载命令"""
        if not directory.exists():
            return

        for file in directory.glob("*.py"):
            if file.stem.startswith("_"):
                continue
            self._load_module(file)

    def load_from_skill(self, skill_path: Path) -> None:
        """从技能加载命令"""
        # 实现从 skill 加载命令
        pass

    def load_from_mcp(self, mcp_server: str) -> None:
        """从 MCP 加载命令"""
        # 实现从 MCP 加载命令
        pass

    def _load_module(self, file: Path) -> None:
        """加载模块"""
        spec = importlib.util.spec_from_file_location(file.stem, file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.loaded.add(file.stem)
```

## 3.5 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `commands.ts` | `registry.py` | `pyclaude/commands/registry.py` |
| `BaseCommand` | `BaseCommand(ABC)` | `pyclaude/commands/base.py` |
| `Command` | `Command` | `pyclaude/commands/registry.py` |
| `CommandType` | `enum CommandType` | `pyclaude/commands/registry.py` |
| 命令加载 | `CommandLoader` | `pyclaude/commands/loader.py` |