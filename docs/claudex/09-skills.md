# 09 - 技能系统

对应 TypeScript: `src/skills/` - 15+ 内置技能

## 9.1 技能系统概述

技能(Skills)是一种可扩展的命令系统，用户可以自定义技能或使用内置技能。

## 9.2 技能注册表

```python
# pyclaude/skills/registry.py
from typing import Optional, Callable, Awaitable
from dataclasses import dataclass
from pathlib import Path
import importlib.util


@dataclass
class Skill:
    """技能定义"""
    name: str
    description: str
    aliases: list[str]
    handler: Callable[..., Awaitable[str]]
    parser: Optional[Callable[[str], dict]] = None


class SkillRegistry:
    """技能注册表"""

    def __init__(self):
        self.skills: dict[str, Skill] = {}
        self._load_builtin_skills()

    def register(self, skill: Skill) -> None:
        """注册技能"""
        self.skills[skill.name] = skill
        for alias in skill.aliases:
            self.skills[alias] = skill

    def get(self, name: str) -> Optional[Skill]:
        """获取技能"""
        return self.skills.get(name)

    def list_skills(self) -> list[Skill]:
        """列出所有技能"""
        return list(set(self.skills.values()))

    async def execute(self, name: str, args: dict) -> str:
        """执行技能"""
        skill = self.get(name)
        if not skill:
            raise ValueError(f"Skill not found: {name}")
        return await skill.handler(**args)

    def load_from_directory(self, directory: Path) -> None:
        """从目录加载技能"""
        if not directory.exists():
            return

        for file in directory.glob("*.py"):
            if file.stem.startswith("_"):
                continue
            self._load_skill_file(file)

    def _load_skill_file(self, file: Path) -> None:
        """加载技能文件"""
        spec = importlib.util.spec_from_file_location(file.stem, file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # 查找 register_skill 函数
            if hasattr(module, "register_skill"):
                skill = module.register_skill()
                self.register(skill)

    def _load_builtin_skills(self) -> None:
        """加载内置技能"""
        from pyclaude.skills import builtin
        builtin_dir = Path(builtin.__file__).parent
        self.load_from_directory(builtin_dir)
```

## 9.3 内置技能

### 9.3.1 Simplify Skill

```python
# pyclaude/skills/builtin/simplify.py
from pyclaude.skills.registry import Skill


def register_skill() -> Skill:
    """注册 Simplify 技能"""
    async def execute(input: str = "", **kwargs) -> str:
        # 实现代码简化逻辑
        return "Code simplified successfully"

    return Skill(
        name="simplify",
        description="Review changed code for reuse, quality, and efficiency",
        aliases=["simp"],
        handler=execute,
    )
```

### 9.3.2 Debug Skill

```python
# pyclaude/skills/builtin/debug.py
from pyclaude.skills.registry import Skill


def register_skill() -> Skill:
    """注册 Debug 技能"""
    async def execute(input: str = "", **kwargs) -> str:
        # 实现调试逻辑
        return "Debug session started"

    return Skill(
        name="debug",
        description="Start a debugging session for the current code",
        aliases=["dbg"],
        handler=execute,
    )
```

### 9.3.3 Verify Skill

```python
# pyclaude/skills/builtin/verify.py
from pyclaude.skills.registry import Skill


def register_skill() -> Skill:
    """注册 Verify 技能"""
    async def execute(input: str = "", **kwargs) -> str:
        # 实现验证逻辑
        return "Verification complete"

    return Skill(
        name="verify",
        description="Verify code changes and test results",
        aliases=["vfy"],
        handler=execute,
    )
```

### 9.3.4 Loop Skill

```python
# pyclaude/skills/builtin/loop.py
from pyclaude.skills.registry import Skill
from pyclaude.core.task import TaskType


def register_skill() -> Skill:
    """注册 Loop 技能"""
    async def execute(input: str = "", interval: str = "10m", **kwargs) -> str:
        # 实现循环任务逻辑
        return f"Loop task scheduled: {interval}"

    return Skill(
        name="loop",
        description="Run a prompt or command on a recurring interval",
        aliases=[],
        handler=execute,
    )
```

## 9.4 技能类型

| 技能名 | 描述 | 别名 |
|--------|------|------|
| `simplify` | 代码审查与优化 | `simp` |
| `debug` | 调试会话 | `dbg` |
| `verify` | 验证更改 | `vfy` |
| `loop` | 循环任务 | - |
| `review` | 代码审查 | `rvw` |
| `test` | 测试生成 | `t` |
| `commit` | 提交创建 | `c` |
| `mcp` | MCP 命令 | - |
| `claude-api` | Claude API | - |

## 9.5 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `SkillRegistry` | `class SkillRegistry` | `pyclaude/skills/registry.py` |
| `Skill` | `class Skill` | `pyclaude/skills/registry.py` |
| `SkillLoader` | `class SkillLoader` | `pyclaude/skills/loader.py` |
| 内置技能 | `builtin/*.py` | `pyclaude/skills/builtin/` |