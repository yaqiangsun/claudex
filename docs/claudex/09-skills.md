# 09 - 技能系统

对应 TypeScript: `src/skills/` - 15+ 内置技能

## 9.1 技能系统概述

技能(Skills)是一种可扩展的命令系统，提供可复用的提示词模板。核心特点：

- **多源加载**: 内置(bundled)、磁盘加载、 MCP、插件
- **两种执行模式**: Inline(内联) 和 Forked(子代理)
- **动态发现**: 根据文件路径条件激活
- **权限控制**: 受工具权限系统管理

## 9.2 技能来源分类

| 类型 | 来源位置 | 加载机制 |
|------|----------|----------|
| **bundled** | CLI 二进制 | 程序化注册 (`registerBundledSkill`) |
| **skills/** | `~/.claude/skills/`, `.claude/skills/` | 目录加载 (`skill-name/SKILL.md`) |
| **commands/** | `.claude/commands/` | 兼容加载器 |
| **mcp** | MCP 服务器 | MCP 协议加载 |
| **plugin** | 插件 | 插件加载 |

## 9.3 技能 Manifest 格式 (SKILL.md)

```markdown
---
name: Display Name          # 可选显示名称
description: Skill 描述     # 必填
when_to_use: 使用场景提示   # 可选
arguments: [arg1, arg2]    # 参数名列表
argument-hint: hint        # 参数格式提示
allowed-tools: [Read, Grep] # 允许使用的工具
user-invocable: true       # 默认 true，允许用户直接调用
model: claude-sonnet-4-20250514 # 模型覆盖
disable-model-invocation: false # 需要显式调用
paths:                     # 条件激活路径
  - "src/**/*.ts"
hooks:                     # Hook 配置
  on_match: ...
shell: !`echo hello`       # 内联 shell 执行
---

# Skill 提示词内容

实际的提示词模板...

## 变量替换

${CLAUDE_SKILL_DIR} - Skill 目录
${CLAUDE_SESSION_ID} - 会话 ID
$1, $2 - 位置参数
```

## 9.4 技能定义

```python
# pyclaude/skills/types.py
from dataclasses import dataclass, field
from typing import Optional, Callable, Awaitable, Any
from enum import Enum


class SkillContext(str, Enum):
    """Skill 执行上下文"""
    INLINE = "inline"   # 内联展开到对话
    FORK = "fork"       # 子代理执行


@dataclass
class Skill:
    """Skill 定义"""
    name: str                           # Skill 名称 (/name 调用)
    description: str                    # 描述
    aliases: list[str] = field(default_factory=list)  # 别名
    when_to_use: Optional[str] = None  # 使用场景提示
    argument_hint: Optional[str] = None  # 参数提示
    allowed_tools: list[str] = field(default_factory=list)  # 允许工具
    model: Optional[str] = None         # 指定模型
    disable_model_invocation: bool = False  # 需要显式调用
    user_invocable: bool = True         # 允许用户调用
    is_enabled: Optional[Callable[[], bool]] = None  # 动态启用检查
    hooks: Optional[dict] = None        # Hook 配置
    context: SkillContext = SkillContext.INLINE  # 执行模式
    files: Optional[dict[str, str]] = None  # 引用文件
    paths: Optional[list[str]] = None   # 条件激活路径

    # 执行函数
    get_prompt: Callable[[str, "ToolUseContext"], Awaitable[list[dict]]]


@dataclass
class ToolUseContext:
    """工具使用上下文"""
    tool_use_id: str
    agent_id: Optional[str]
    set_app_state: Optional[Callable]
    # ... 其他上下文字段
```

## 9.5 技能注册表

```python
# pyclaude/skills/registry.py
from typing import Optional, Callable, Awaitable
from dataclasses import dataclass, field
from pathlib import Path
import importlib.util
import hashlib

from pyclaude.skills.types import Skill, SkillContext


class SkillRegistry:
    """Skill 注册表"""

    def __init__(self):
        self.skills: dict[str, Skill] = {}
        self.skills_by_file: dict[str, Skill] = {}  # 文件指纹去重
        self._load_builtin_skills()
        self._load_disk_skills()

    def register(self, skill: Skill, file_identity: Optional[str] = None) -> None:
        """注册 Skill"""
        # 文件去重
        if file_identity and file_identity in self.skills_by_file:
            return

        self.skills[skill.name] = skill
        if file_identity:
            self.skills_by_file[file_identity] = skill

        for alias in skill.aliases:
            self.skills[alias] = skill

    def get(self, name: str) -> Optional[Skill]:
        """获取 Skill"""
        return self.skills.get(name)

    def find_by_path(self, file_path: str) -> Optional[Skill]:
        """根据路径查找条件激活的 Skill"""
        for skill in self.skills.values():
            if skill.paths:
                import fnmatch
                for pattern in skill.paths:
                    if fnmatch.fnmatch(file_path, pattern):
                        return skill
        return None

    def list_skills(self) -> list[Skill]:
        """列出所有 Skill"""
        return list(set(self.skills.values()))

    async def execute(
        self,
        name: str,
        args: str,
        context: "ToolUseContext",
    ) -> dict:
        """执行 Skill"""
        skill = self.get(name)
        if not skill:
            raise ValueError(f"Skill not found: {name}")

        # 根据执行模式选择处理方式
        if skill.context == SkillContext.FORK:
            return await self._execute_forked(skill, args, context)
        else:
            return await self._execute_inline(skill, args, context)

    async def _execute_inline(
        self,
        skill: Skill,
        args: str,
        context: "ToolUseContext",
    ) -> dict:
        """内联执行 - 展开提示词到对话"""
        prompt_blocks = await skill.get_prompt(args, context)
        return {
            "type": "skill_prompt",
            "blocks": prompt_blocks,
            "allowed_tools": skill.allowed_tools,
        }

    async def _execute_forked(
        self,
        skill: Skill,
        args: str,
        context: "ToolUseContext",
    ) -> dict:
        """Fork 执行 - 子代理模式"""
        # 在子代理中运行，带独立 token 预算
        pass

    def _load_builtin_skills(self) -> None:
        """加载内置 Skills"""
        from pyclaude.skills import builtin
        builtin_dir = Path(builtin.__file__).parent

        # 注册所有内置 skill
        from pyclaude.skills.bundled import (
            register_simplify_skill,
            register_debug_skill,
            register_verify_skill,
            register_loop_skill,
            register_remember_skill,
            register_stuck_skill,
        )

        for register_fn in [
            register_simplify_skill,
            register_debug_skill,
            register_verify_skill,
            register_loop_skill,
            register_remember_skill,
            register_stuck_skill,
        ]:
            skill = register_fn()
            self.register(skill)

    def _load_disk_skills(self) -> None:
        """从磁盘加载 Skills"""
        # ~/.claude/skills/
        user_skills_dir = Path.home() / ".claude" / "skills"
        self._load_skills_from_directory(user_skills_dir)

        # .claude/skills/
        if Path.cwd() != Path.home():
            project_skills_dir = Path.cwd() / ".claude" / "skills"
            self._load_skills_from_directory(project_skills_dir)

    def _load_skills_from_directory(self, directory: Path) -> None:
        """从目录加载 Skills"""
        if not directory.exists():
            return

        for skill_dir in directory.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue

            # 计算文件指纹用于去重
            file_identity = self._compute_file_identity(skill_file)
            skill = self._load_skill_file(skill_file)
            if skill:
                self.register(skill, file_identity)

    def _load_skill_file(self, file_path: Path) -> Optional[Skill]:
        """加载单个 Skill 文件"""
        import yaml

        content = file_path.read_text()

        # 解析 frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                prompt_content = parts[2].strip()
            else:
                frontmatter = {}
                prompt_content = content
        else:
            frontmatter = {}
            prompt_content = content

        # 创建 Skill 对象
        return Skill(
            name=frontmatter.get("name", file_path.parent.name),
            description=frontmatter.get("description", ""),
            aliases=frontmatter.get("aliases", []),
            when_to_use=frontmatter.get("when_to_use"),
            argument_hint=frontmatter.get("argument_hint"),
            allowed_tools=frontmatter.get("allowed-tools", []),
            user_invocable=frontmatter.get("user-invocable", True),
            model=frontmatter.get("model"),
            disable_model_invocation=frontmatter.get("disable-model-invocation", False),
            paths=frontmatter.get("paths"),
            get_prompt=self._create_prompt_getter(prompt_content, frontmatter),
        )

    def _create_prompt_getter(
        self,
        prompt_content: str,
        frontmatter: dict,
    ) -> Callable[[str, "ToolUseContext"], Awaitable[list[dict]]]:
        """创建提示词获取函数"""
        def get_prompt(args: str, context: "ToolUseContext") -> Awaitable[list[dict]]:
            # 处理参数替换
            processed = prompt_content

            # 位置参数替换
            args_list = args.split()
            for i, arg in enumerate(args_list):
                processed = processed.replace(f"${i+1}", arg)

            # 环境变量替换
            processed = processed.replace("${CLAUDE_SKILL_DIR}", str(context.get("skill_dir", "")))
            processed = processed.replace("${CLAUDE_SESSION_ID}", context.get("session_id", ""))

            return [{"type": "text", "text": processed}]

        return get_prompt

    def _compute_file_identity(self, file_path: Path) -> str:
        """计算文件指纹用于去重"""
        stat = file_path.stat()
        identity = f"{file_path}:{stat.st_mtime}:{stat.st_size}"
        return hashlib.md5(identity.encode()).hexdigest()
```

## 9.6 内置 Skills

### 9.6.1 Simplify Skill

```python
# pyclaude/skills/bundled/simplify.py
from pyclaude.skills.types import Skill


def register_simplify_skill() -> Skill:
    """注册 Simplify Skill"""

    async def get_prompt(args: str, context) -> list[dict]:
        prompt = f"""Review the changed code for reuse, quality, and efficiency.

{args}

Focus on:
1. Code that could be extracted into utilities
2. Duplication that could be refactored
3. Performance inefficiencies
4. Clean code improvements

Report findings and optionally apply fixes."""
        return [{"type": "text", "text": prompt}]

    return Skill(
        name="simplify",
        description="Review changed code for reuse, quality, and efficiency",
        aliases=["simp"],
        get_prompt=get_prompt,
    )
```

### 9.6.2 Debug Skill

```python
# pyclaude/skills/bundled/debug.py
def register_debug_skill() -> Skill:
    """注册 Debug Skill"""
    # 类似实现...
```

### 9.6.3 Verify Skill

```python
# pyclaude/skills/bundled/verify.py
def register_verify_skill() -> Skill:
    """注册 Verify Skill"""
    # 类似实现...
```

### 9.6.4 Loop Skill (功能门控)

```python
# pyclaude/skills/bundled/loop.py
def register_loop_skill() -> Skill:
    """注册 Loop Skill - 循环任务"""
    # 受 feature flag 控制
    return Skill(
        name="loop",
        description="Run a prompt or command on a recurring interval",
        get_prompt=...,
        is_enabled=lambda: is_feature_enabled("KAIROS"),
    )
```

## 9.7 Skill 执行集成

```python
# pyclaude/tools/skill_tool.py
from pyclaude.tools.base import BaseTool, ToolDefinition, ToolCapability


class SkillTool(BaseTool):
    """Skill 工具 - 调用 Skills"""

    def __init__(self, skill_registry: "SkillRegistry"):
        self.skill_registry = skill_registry
        self.definition = ToolDefinition(
            name="Skill",
            description="Invoke a skill to perform specialized tasks",
            input_schema={
                "type": "object",
                "properties": {
                    "skill": {"type": "string", "description": "Skill name"},
                    "args": {"type": "string", "description": "Arguments"},
                },
                "required": ["skill"],
            },
            capability=ToolCapability.CONCURRENT_SAFE,
        )

    async def execute(self, tool_input: dict) -> dict:
        skill_name = tool_input.get("skill")
        args = tool_input.get("args", "")

        result = await self.skill_registry.execute(skill_name, args, context)
        return result
```

## 9.8 动态 Skill 发现

```python
# pyclaude/skills/discovery.py
from pathlib import Path
import fnmatch


class SkillDiscovery:
    """动态 Skill 发现"""

    def __init__(self, registry: "SkillRegistry"):
        self.registry = registry

    def find_relevant_skills(self, file_path: str) -> list["Skill"]:
        """根据文件路径查找相关的条件激活 Skills"""
        return self.registry.find_by_path(file_path)

    def discover_in_directory(self, directory: Path) -> None:
        """在目录中发现 Skills"""
        self.registry._load_skills_from_directory(directory)
```

## 9.9 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `Skill` | `class Skill` | `pyclaude/skills/types.py` |
| `SkillRegistry` | `class SkillRegistry` | `pyclaude/skills/registry.py` |
| `SkillTool` | `class SkillTool` | `pyclaude/tools/skill_tool.py` |
| `SkillDiscovery` | `class SkillDiscovery` | `pyclaude/skills/discovery.py` |
| 内置 Skills | `bundled/*.py` | `pyclaude/skills/bundled/` |
| 磁盘加载 | `_load_disk_skills` | `pyclaude/skills/registry.py` |

## 9.10 全部内置 Skills 列表

| Skill 名 | 描述 | 别名 | 特性门控 |
|----------|------|------|----------|
| `simplify` | 代码审查与优化 | `simp` | - |
| `debug` | 调试会话 | `dbg` | - |
| `verify` | 验证更改 | `vfy` | - |
| `loop` | 循环任务 | - | KAIROS |
| `remember` | 记忆信息 | `rem` | - |
| `stuck` | 处理卡住状态 | - | - |
| `updateConfig` | 更新配置 | - | - |
| `claude-api` | Claude API | - | 需许可 |
| `claudeInChrome` | Chrome 集成 | - | - |
| `batch` | 批量操作 | - | - |
| `keybindings` | 显示快捷键 | `keys` | - |
| `loremIpsum` | 占位文本 | - | - |
| `scheduleRemoteAgents` | 远程调度 | - | - |
| `skillify` | 命令转 Skill | - | - |
| `verifyContent` | 内容验证 | - | - |