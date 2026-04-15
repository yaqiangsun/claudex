# 16 - 内存系统 (Memdir) 与其他模块

对应 TypeScript: `src/memdir/`, `src/buddy/`, `src/coordinator/`, `src/remote/`

---

## 16.1 内存系统 (Memdir) 详解

### 16.1.1 内存类型分类

```python
# pyclaude/memdir/types.py
from enum import Enum


class MemoryType(str, Enum):
    """内存类型 - 四类分类"""
    USER = "user"       # 用户信息：角色、目标、偏好
    FEEDBACK = "feedback"  # 用户反馈：纠正、确认
    PROJECT = "project"    # 项目信息：目标、bug、initiate
    REFERENCE = "reference"  # 引用：外部系统指针


@dataclass
class MemoryEntry:
    """记忆条目"""
    entry_id: str
    name: str           # 用于索引的标题
    description: str    # 一行描述（用于判断相关性）
    memory_type: MemoryType

    file_path: Path
    content: str
    created_at: datetime
    updated_at: datetime
    mtime: datetime     # 文件修改时间
```

### 16.1.2 内存路径管理

```python
# pyclaude/memdir/paths.py
from pathlib import Path
import os


class MemoryPathManager:
    """内存路径管理器"""

    DEFAULT_MEMORY_BASE = Path.home() / ".claude"
    REMOTE_MEMORY_BASE = os.environ.get("CLAUDE_CODE_REMOTE_MEMORY_DIR")

    @classmethod
    def get_memory_base(cls) -> Path:
        """获取内存基础目录"""
        if cls.REMOTE_MEMORY_BASE:
            return Path(cls.REMOTE_MEMORY_BASE)
        return cls.DEFAULT_MEMORY_BASE

    @classmethod
    def get_auto_mem_path(cls, project_root: str = None) -> Path:
        """获取自动记忆目录"""
        base = cls.get_memory_base()

        if project_root:
            # 清理项目路径作为目录名
            safe_name = cls._sanitize_path(project_root)
            return base / "projects" / safe_name / "memory"

        return base / "memory"

    @classmethod
    def is_auto_mem_path(cls, path: Path) -> bool:
        """检查路径是否在自动记忆目录"""
        auto_mem = cls.get_auto_mem_path()
        try:
            path.resolve().relative_to(auto_mem.resolve())
            return True
        except ValueError:
            return False

    @classmethod
    def is_auto_memory_enabled(cls) -> bool:
        """检查自动记忆是否启用"""
        # 检查环境变量和设置
        return os.environ.get("CLAUDE_CODE_AUTO_MEMORY", "1") == "1"
```

### 16.1.3 内存扫描与加载

```python
# pyclaude/memdir/scanner.py
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from pyclaude.memdir.types import MemoryEntry, MemoryType


@dataclass
class ScannedMemory:
    """扫描到的内存"""
    file_path: Path
    mtime: datetime
    name: str
    description: str
    memory_type: MemoryType


class MemoryScanner:
    """内存扫描器"""

    async def scan_memory_files(
        self,
        memory_dir: Path,
    ) -> list[ScannedMemory]:
        """扫描内存目录下的所有 .md 文件"""
        if not memory_dir.exists():
            return []

        memories = []
        for md_file in memory_dir.rglob("*.md"):
            # 跳过非内存文件（如索引文件）
            if md_file.name == "MEMORY.md" and md_file.parent == memory_dir:
                continue

            scanned = await self._scan_file(md_file)
            if scanned:
                memories.append(scanned)

        # 按修改时间排序（最新优先）
        return sorted(memories, key=lambda m: m.mtime, reverse=True)

    async def _scan_file(self, file_path: Path) -> Optional[ScannedMemory]:
        """扫描单个文件"""
        import yaml

        content = file_path.read_text()

        # 解析 frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                description = frontmatter.get("description", "")
                name = frontmatter.get("name", file_path.stem)
                memory_type = MemoryType(frontmatter.get("type", "general"))
            else:
                name = file_path.stem
                description = ""
                memory_type = MemoryType.GENERAL
        else:
            name = file_path.stem
            description = ""
            memory_type = MemoryType.GENERAL

        stat = file_path.stat()

        return ScannedMemory(
            file_path=file_path,
            mtime=datetime.fromtimestamp(stat.st_mtime),
            name=name,
            description=description,
            memory_type=memory_type,
        )
```

### 16.1.4 记忆检索与相关性

```python
# pyclaude/memdir/retrieval.py
from pathlib import Path
from typing import Optional
import httpx

from pyclaude.services.api import APIClient


class MemoryRetrieval:
    """记忆检索 - 查询时选择相关记忆"""

    MAX_MEMORY_BYTES = 4 * 1024   # 每个记忆最大 4KB
    MAX_MEMORIES = 5              # 每次最多 5 个记忆

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def find_relevant_memories(
        self,
        query: str,
        memory_dir: Path,
        exclude_paths: list[Path] = None,
    ) -> list[tuple[Path, datetime]]:
        """使用 AI 查找相关记忆"""
        # 1. 扫描所有记忆
        from pyclaude.memdir.scanner import MemoryScanner
        scanner = MemoryScanner()
        all_memories = await scanner.scan_memory_files(memory_dir)

        # 2. 过滤已排除的记忆
        exclude_paths = exclude_paths or []
        candidates = [
            m for m in all_memories
            if m.file_path not in exclude_paths
        ]

        if not candidates:
            return []

        # 3. 使用轻量模型选择相关记忆
        prompt = self._build_selection_prompt(query, candidates)

        response = await self.api_client.create_completion({
            "model": "claude-haiku-4-5-20251001",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
        })

        # 4. 解析响应获取选中的记忆
        selected = self._parse_selection(response, candidates)

        # 5. 返回路径和修改时间
        return [(m.file_path, m.mtime) for m in selected[:self.MAX_MEMORIES]]

    def _build_selection_prompt(
        self,
        query: str,
        candidates: list["ScannedMemory"],
    ) -> str:
        """构建选择提示词"""
        memory_list = "\n".join([
            f"- {m.name}: {m.description} (type: {m.memory_type.value})"
            for m in candidates
        ])

        return f"""Given the user query: "{query}"

Select up to {self.MAX_MEMORIES} most relevant memories from this list:

{memory_list}

Return only the names of selected memories, one per line:"""

    def _parse_selection(
        self,
        response: dict,
        candidates: list["ScannedMemory"],
    ) -> list["ScannedMemory"]:
        """解析选择结果"""
        # 简单实现：返回响应中提到的记忆
        # 实际需要更复杂的解析
        content = response.get("content", "")
        selected = []

        for line in content.split("\n"):
            line = line.strip()
            if not line:
                continue

            for candidate in candidates:
                if candidate.name.lower() in line.lower():
                    selected.append(candidate)
                    break

        return selected
```

### 16.1.5 记忆提取 (自动写入)

```python
# pyclaude/memdir/extractor.py
"""
记忆提取服务 - 每次查询结束时自动提取记忆
"""


class MemoryExtractor:
    """记忆提取器"""

    def __init__(self, api_client, memory_path_manager):
        self.api_client = api_client
        self.memory_path = memory_path_manager.get_auto_mem_path()
        self.feature_gate = "tengu_bramble_lintel"  # 提取节流

    async def extract_memories(
        self,
        conversation: list[dict],
        session_id: str,
    ) -> None:
        """从对话中提取记忆"""
        # 1. 检查是否应该提取 (节流)
        if not self._should_extract():
            return

        # 2. 使用子代理提取
        prompt = self._build_extraction_prompt(conversation)

        result = await self._run_forked_agent(prompt)

        # 3. 写入记忆文件
        if result:
            await self._write_memories(result, session_id)

    async def _run_forked_agent(self, prompt: str) -> Optional[dict]:
        """在子代理中运行提取"""
        # 实现 fork 子代理逻辑
        pass

    async def _write_memories(self, memories: dict, session_id: str) -> None:
        """写入记忆文件"""
        import yaml
        from datetime import datetime

        for memory_type, entries in memories.items():
            if not entries:
                continue

            # 每个类型一个文件
            file_path = self.memory_path / f"{memory_type}.md"

            # 构建文件内容
            content = f"---\ntype: {memory_type}\n---\n\n"
            content += f"# {memory_type.capitalize()} Memories\n\n"

            for entry in entries:
                content += f"## {entry['name']}\n\n"
                content += f"{entry['content']}\n\n"
                content += f"_Extracted: {datetime.now().isoformat()}_\n\n"

            file_path.write_text(content)
```

### 16.1.6 团队记忆

```python
# pyclaude/memdir/team.py
from pathlib import Path


class TeamMemory:
    """团队记忆 - 共享内存"""

    @classmethod
    def get_team_mem_path(cls, auto_mem_path: Path) -> Path:
        """获取团队记忆目录"""
        return auto_mem_path / "team"

    @classmethod
    def is_team_memory_enabled(cls) -> bool:
        """检查团队记忆是否启用"""
        import os
        return os.environ.get("CLAUDE_CODE_TEAM_MEMORY", "0") == "1"

    @classmethod
    def validate_write_path(cls, path: Path) -> bool:
        """验证写入路径（防止路径遍历）"""
        try:
            resolved = path.resolve()
            team_path = cls.get_team_mem_path(
                path.parent.parent  # 假设 path 是 team/xxx/xxx.md
            ).resolve()

            # 确保解析后的路径在团队目录内
            resolved.relative_to(team_path)
            return True
        except ValueError:
            return False
```

---

## 16.2 会话记忆

```python
# pyclaude/memdir/session.py
"""
会话记忆 - 当前会话的对话笔记
用于上下文压缩
"""


class SessionMemory:
    """会话记忆"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.memory_dir = Path.home() / ".claude" / "session-memory"
        self.file_path = self.memory_dir / f"{session_id}.md"

    async def update(
        self,
        token_count: int,
        tool_call_count: int,
        transcript: list[dict],
    ) -> None:
        """更新会话记忆"""
        # 基于 token 数量和工具调用次数阈值决定是否更新
        # 使用子代理生成总结
        pass

    async def get_for_context(self) -> str:
        """获取用于上下文的记忆"""
        if not self.file_path.exists():
            return ""
        return self.file_path.read_text()
```

---

## 16.3 Agent 内存

```python
# pyclaude/memdir/agent.py
"""
Agent 内存 - Agent 特定的内存作用域
"""


class AgentMemoryScope(str, Enum):
    """Agent 内存作用域"""
    USER = "user"       # 用户级别
    PROJECT = "project" # 项目级别
    LOCAL = "local"     # 本地级别


class AgentMemory:
    """Agent 内存管理器"""

    @classmethod
    def get_agent_memory_dir(
        cls,
        agent_type: str,
        scope: AgentMemoryScope,
    ) -> Path:
        """获取 Agent 内存目录"""
        if scope == AgentMemoryScope.USER:
            return Path.home() / ".claude" / "agent-memory" / agent_type
        elif scope == AgentMemoryScope.PROJECT:
            return Path.cwd() / ".claude" / "agent-memory" / agent_type
        else:  # LOCAL
            return Path.cwd() / ".agent-memory" / agent_type

    @classmethod
    def is_agent_memory_path(cls, path: Path) -> bool:
        """检查路径是否为 Agent 内存路径"""
        agent_memory_patterns = [
            ".claude/agent-memory",
            ".agent-memory",
        ]
        path_str = str(path)
        return any(p in path_str for p in agent_memory_patterns)
```

---

## 16.4 嵌套记忆 (CLAUDE.md)

```python
# pyclaude/memdir/nested.py
"""
嵌套记忆 - 目录层级中的 CLAUDE.md 文件
"""


class NestedMemory:
    """嵌套记忆管理器"""

    @classmethod
    def find_claude_md_files(cls, cwd: Path) -> list[tuple[Path, str]]:
        """查找从根目录到 CWD 的所有 CLAUDE.md"""
        claude_files = []

        # 从根目录向下扫描
        current = cwd
        while True:
            claude_md = current / "CLAUDE.md"
            if claude_md.exists():
                claude_files.append((claude_md, str(current)))

            # 到达文件系统根
            if current.parent == current:
                break
            current = current.parent

        # 反转顺序（从根到当前目录）
        return list(reversed(claude_files))

    @classmethod
    def find_conditional_rules(
        cls,
        cwd: Path,
    ) -> list[tuple[Path, list[str]]]:
        """查找条件规则 (.claude/rules/)"""
        rules_dir = cwd / ".claude" / "rules"
        if not rules_dir.exists():
            return []

        rules = []
        for rule_file in rules_dir.glob("*.md"):
            # 解析 frontmatter 中的 glob 模式
            content = rule_file.read_text()
            # 提取 patterns
            patterns = cls._extract_glob_patterns(content)
            rules.append((rule_file, patterns))

        return rules
```

---

## 16.5 Buddy 模块

### 16.5.1 伙伴精灵系统

Buddy 是一个同伴精灵功能，在 UI 中显示辅助交互角色。

```python
# pyclaude/buddy/sprite.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SpriteType(Enum):
    """精灵类型"""
    DEFAULT = "default"     # 默认静态显示
    ANIMATED = "animated"   # 动画显示
    MINIMAL = "minimal"     # 极简显示


@dataclass
class Sprite:
    """精灵定义"""
    name: str               # 名称
    emoji: str              # 表情符号
    sprite_type: SpriteType = SpriteType.DEFAULT
    description: str = ""   # 描述


class BuddyEngine:
    """Buddy 引擎 - 管理同伴精灵"""

    def __init__(self):
        self.current_sprite: Optional[Sprite] = None
        self.sprites: dict[str, Sprite] = {}
        self._load_default_sprites()

    def _load_default_sprites(self) -> None:
        """加载默认精灵"""
        # 默认精灵
        self.current_sprite = Sprite(
            name="Claude",
            emoji="🧠",
            sprite_type=SpriteType.DEFAULT,
            description="AI programming assistant",
        )
        self.sprites["default"] = self.current_sprite

    def set_sprite(self, sprite: Sprite) -> None:
        """设置当前精灵"""
        self.current_sprite = sprite

    def set_sprite_by_name(self, name: str) -> bool:
        """通过名称设置精灵"""
        if name in self.sprites:
            self.current_sprite = self.sprites[name]
            return True
        return False

    def get_greeting(self) -> str:
        """获取问候语"""
        if self.current_sprite:
            return f"{self.current_sprite.emoji} {self.current_sprite.name} is ready to help!"
        return "Ready to help!"

    def get_status_message(self, status: str) -> str:
        """获取状态消息"""
        if not self.current_sprite:
            return ""

        messages = {
            "thinking": f"{self.current_sprite.emoji} Thinking...",
            "working": f"{self.current_sprite.emoji} Working on it...",
            "done": f"{self.current_sprite.emoji} Done!",
            "error": f"{self.current_sprite.emoji} Something went wrong",
        }
        return messages.get(status, "")
```

---

## 16.6 Coordinator 模块

### 16.6.1 任务协调系统

Coordinator 负责任务协调和管理。

```python
# pyclaude/coordinator/task.py
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"     # 待处理
    RUNNING = "running"     # 运行中
    COMPLETED = "completed" # 已完成
    FAILED = "failed"       # 失败
    CANCELLED = "cancelled" # 已取消


@dataclass
class CoordinatedTask:
    """协调任务"""
    task_id: str
    name: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING

    # 时间信息
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # 结果
    result: Optional[dict] = None
    error: Optional[str] = None

    # 依赖
    depends_on: list[str] = field(default_factory=list)

    # 元数据
    metadata: dict = field(default_factory=dict)


class TaskCoordinator:
    """任务协调器"""

    def __init__(self):
        self.tasks: dict[str, CoordinatedTask] = {}
        self._running: list[str] = []
        self._completed: list[str] = []

    def create_task(
        self,
        name: str,
        description: str = "",
        depends_on: list[str] = None,
    ) -> str:
        """创建任务"""
        task_id = str(uuid.uuid4())

        # 检查依赖
        if depends_on:
            for dep_id in depends_on:
                if dep_id not in self.tasks:
                    raise ValueError(f"Dependency task not found: {dep_id}")

        task = CoordinatedTask(
            task_id=task_id,
            name=name,
            description=description,
            depends_on=depends_on or [],
        )
        self.tasks[task_id] = task
        return task_id

    def start_task(self, task_id: str) -> bool:
        """开始任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False

        # 检查依赖是否完成
        for dep_id in task.depends_on:
            dep_task = self.tasks.get(dep_id)
            if dep_task and dep_task.status != TaskStatus.COMPLETED:
                return False  # 依赖未完成

        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        self._running.append(task_id)
        return True

    def complete_task(self, task_id: str, result: dict = None) -> bool:
        """完成任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False

        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.result = result or {}

        if task_id in self._running:
            self._running.remove(task_id)
        self._completed.append(task_id)

        return True

    def fail_task(self, task_id: str, error: str) -> bool:
        """任务失败"""
        task = self.tasks.get(task_id)
        if not task:
            return False

        task.status = TaskStatus.FAILED
        task.completed_at = datetime.now()
        task.error = error

        if task_id in self._running:
            self._running.remove(task_id)

        return True

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False

        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now()

        if task_id in self._running:
            self._running.remove(task_id)

        return True

    def get_task(self, task_id: str) -> Optional[CoordinatedTask]:
        """获取任务"""
        return self.tasks.get(task_id)

    def get_ready_tasks(self) -> list[str]:
        """获取就绪的任务（依赖已满足）"""
        ready = []
        for task_id, task in self.tasks.items():
            if task.status != TaskStatus.PENDING:
                continue

            # 检查依赖
            all_deps_done = True
            for dep_id in task.depends_on:
                dep_task = self.tasks.get(dep_id)
                if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                    all_deps_done = False
                    break

            if all_deps_done:
                ready.append(task_id)

        return ready

    def list_tasks(self, status: TaskStatus = None) -> list[CoordinatedTask]:
        """列出任务"""
        if status:
            return [t for t in self.tasks.values() if t.status == status]
        return list(self.tasks.values())

    def get_statistics(self) -> dict:
        """获取统计信息"""
        stats = {
            "total": len(self.tasks),
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0,
        }
        for task in self.tasks.values():
            stats[task.status.value] += 1
        return stats
```

---

## 16.7 Remote 模块

### 16.7.1 远程会话管理

Remote 模块处理远程会话。

```python
# pyclaude/remote/session.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


class RemoteSessionState(str, Enum):
    """远程会话状态"""
    ACTIVE = "active"
    IDLE = "idle"
    CLOSED = "closed"
    ERROR = "error"


@dataclass
class RemoteSession:
    """远程会话"""
    session_id: str
    state: RemoteSessionState = RemoteSessionState.ACTIVE

    # 时间信息
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)

    # 连接信息
    remote_address: Optional[str] = None
    transport_type: str = "websocket"

    # 元数据
    metadata: dict = field(default_factory=dict)

    @staticmethod
    def create() -> "RemoteSession":
        """创建新远程会话"""
        now = datetime.now()
        return RemoteSession(
            session_id=str(uuid.uuid4()),
            created_at=now,
            last_activity=now,
        )

    def update_activity(self) -> None:
        """更新最后活动时间"""
        self.last_activity = datetime.now()

    def close(self) -> None:
        """关闭会话"""
        self.state = RemoteSessionState.CLOSED


class RemoteManager:
    """远程会话管理器"""

    def __init__(self):
        self.sessions: dict[str, RemoteSession] = {}

    def create_session(self) -> RemoteSession:
        """创建会话"""
        session = RemoteSession.create()
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[RemoteSession]:
        """获取会话"""
        return self.sessions.get(session_id)

    def close_session(self, session_id: str) -> None:
        """关闭会话"""
        if session_id in self.sessions:
            self.sessions[session_id].close()

    def list_active_sessions(self) -> list[RemoteSession]:
        """列出活动会话"""
        return [
            s for s in self.sessions.values()
            if s.state == RemoteSessionState.ACTIVE
        ]
```

---

## 16.8 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `MemoryType` | `enum MemoryType` | `pyclaude/memdir/types.py` |
| `MemoryEntry` | `class MemoryEntry` | `pyclaude/memdir/types.py` |
| `MemoryPathManager` | `class MemoryPathManager` | `pyclaude/memdir/paths.py` |
| `MemoryScanner` | `class MemoryScanner` | `pyclaude/memdir/scanner.py` |
| `MemoryRetrieval` | `class MemoryRetrieval` | `pyclaude/memdir/retrieval.py` |
| `MemoryExtractor` | `class MemoryExtractor` | `pyclaude/memdir/extractor.py` |
| `TeamMemory` | `class TeamMemory` | `pyclaude/memdir/team.py` |
| `SessionMemory` | `class SessionMemory` | `pyclaude/memdir/session.py` |
| `AgentMemory` | `class AgentMemory` | `pyclaude/memdir/agent.py` |
| `NestedMemory` | `class NestedMemory` | `pyclaude/memdir/nested.py` |
| `Sprite` | `@dataclass Sprite` | `pyclaude/buddy/sprite.py` |
| `BuddyEngine` | `class BuddyEngine` | `pyclaude/buddy/engine.py` |
| `CoordinatedTask` | `@dataclass CoordinatedTask` | `pyclaude/coordinator/task.py` |
| `TaskCoordinator` | `class TaskCoordinator` | `pyclaude/coordinator/task.py` |
| `RemoteSession` | `@dataclass RemoteSession` | `pyclaude/remote/session.py` |
| `RemoteManager` | `class RemoteManager` | `pyclaude/remote/manager.py` |