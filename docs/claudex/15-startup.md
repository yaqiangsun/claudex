# 15 - 启动流程

对应 TypeScript: `src/main.tsx` + `src/setup.ts`

## 15.1 启动流程概述

```
命令行参数解析
    ↓
版本检查
    ↓
配置加载
    ↓
初始化 UDS 服务器（可选）
    ↓
创建 Worktree（可选）
    ↓
初始化核心组件
    ↓
启动 CLI 应用
```

## 15.2 主入口

```python
# pyclaude/main.py
import asyncio
import argparse
from pathlib import Path
import sys

from pyclaude.config import Config, load_config
from pyclaude.setup import Setup
from pyclaude.engine import QueryEngine
from pyclaude.state.store import Store
from pyclaude.state.app_state import AppState
from pyclaude.cli.app import ClaudeApp
from pyclaude.services.api import APIClient
from pyclaude.tools.registry import ToolRegistry
from pyclaude.commands.registry import CommandRegistry
from pyclaude.skills.registry import SkillRegistry


async def main():
    """主入口"""
    parser = argparse.ArgumentParser(description="Claude Code Python")
    parser.add_argument("prompt", nargs="?", help="Initial prompt")
    parser.add_argument("--model", help="Model to use")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming")
    parser.add_argument("--resume", help="Resume a session")
    parser.add_argument("--version", action="store_true", help="Show version")

    args = parser.parse_args()

    if args.version:
        print("Claude Code Python v0.1.0")
        return

    # 1. 加载配置
    config = load_config()

    # 2. 版本检查
    setup = Setup()
    await setup.check_version()

    # 3. 初始化核心组件
    api_client = APIClient(
        api_key=config.api_key,
        base_url=config.api_endpoint,
    )

    tool_registry = ToolRegistry()
    command_registry = CommandRegistry()
    skill_registry = SkillRegistry()

    app_store: Store[AppState] = Store(AppState())

    engine = QueryEngine(
        api_client=api_client,
        tool_registry=tool_registry,
        command_registry=command_registry,
        store=app_store,
        config=config.engine,
    )

    # 4. 启动 CLI
    if args.prompt:
        # 单次查询模式
        async for chunk in engine.query(args.prompt):
            print(chunk.get("text", ""), end="")
    else:
        # 交互模式
        app = ClaudeApp(engine, app_store)
        await app.run_async()


if __name__ == "__main__":
    asyncio.run(main())
```

## 15.3 配置管理

```python
# pyclaude/config.py
from dataclasses import dataclass
from pathlib import Path
import toml
from typing import Optional


@dataclass
class EngineConfig:
    """引擎配置"""
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 8192
    temperature: float = 1.0
    max_conversation_turns: int = 100


@dataclass
class Config:
    """应用配置"""
    api_key: str
    api_endpoint: str = "https://api.anthropic.com"
    engine: EngineConfig = None
    config_path: Path = None


def load_config(config_path: Optional[Path] = None) -> Config:
    """加载配置"""
    if config_path is None:
        config_path = Path.home() / ".claude" / "settings.toml"

    if not config_path.exists():
        # 使用默认配置
        api_key = get_api_key_from_env()
        return Config(api_key=api_key)

    with open(config_path) as f:
        data = toml.load(f)

    return Config(
        api_key=data.get("api_key", get_api_key_from_env()),
        api_endpoint=data.get("api_endpoint", "https://api.anthropic.com"),
        engine=EngineConfig(**data.get("engine", {})),
        config_path=config_path,
    )


def get_api_key_from_env() -> str:
    """从环境变量获取 API Key"""
    import os
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    return key


def save_config(config: Config) -> None:
    """保存配置"""
    config_path = config.config_path or Path.home() / ".claude" / "settings.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "api_key": config.api_key,
        "api_endpoint": config.api_endpoint,
        "engine": {
            "model": config.engine.model,
            "max_tokens": config.engine.max_tokens,
            "temperature": config.engine.temperature,
            "max_conversation_turns": config.engine.max_conversation_turns,
        },
    }

    with open(config_path, "w") as f:
        toml.dump(data, f)
```

## 15.4 初始化设置

```python
# pyclaude/setup.py
import asyncio
from pathlib import Path
import shutil

CLAUDE_DIR = Path.home() / ".claude"
HISTORY_FILE = CLAUDE_DIR / "history.jsonl"
SETTINGS_FILE = CLAUDE_DIR / "settings.toml"


class Setup:
    """初始化设置"""

    async def check_version(self) -> None:
        """检查版本"""
        # 实现版本检查逻辑
        pass

    async def ensure_directories(self) -> None:
        """确保必要目录存在"""
        CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    async def setup_uds_server(self) -> None:
        """设置 UDS 服务器"""
        # 实现 UDS 服务器设置
        pass

    async def create_worktree(self, name: str) -> None:
        """创建 Worktree"""
        # 实现 worktree 创建
        pass

    async def initialize(self) -> None:
        """完整初始化"""
        await self.ensure_directories()
        await self.check_version()
        await self.setup_uds_server()
```

## 15.5 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `main.tsx` | `main.py` | `pyclaude/main.py` |
| `setup.ts` | `setup.py` | `pyclaude/setup.py` |
| `Config` | `@dataclass Config` | `pyclaude/config.py` |