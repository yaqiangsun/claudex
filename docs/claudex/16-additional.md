# 16 - 其他模块

对应 TypeScript: `src/buddy/`, `src/coordinator/`, `src/memdir/`, `src/remote/`

## 16.1 Buddy 模块

Buddy 是一个同伴精灵功能，提供辅助交互。

```python
# pyclaude/buddy/__init__.py
from pyclaude.buddy.engine import BuddyEngine
from pyclaude.buddy.sprite import Sprite

__all__ = ["BuddyEngine", "Sprite"]
```

```python
# pyclaude/buddy/sprite.py
from dataclasses import dataclass
from enum import Enum


class SpriteType(Enum):
    """精灵类型"""
    DEFAULT = "default"
    ANIMATED = "animated"
    MINIMAL = "minimal"


@dataclass
class Sprite:
    """精灵定义"""
    name: str
    emoji: str
    sprite_type: SpriteType = SpriteType.DEFAULT
    description: str = ""
```

```python
# pyclaude/buddy/engine.py
from typing import Optional
from pyclaude.buddy.sprite import Sprite, SpriteType


class BuddyEngine:
    """Buddy 引擎"""

    def __init__(self):
        self.current_sprite: Optional[Sprite] = None
        self._load_default_sprites()

    def _load_default_sprites(self) -> None:
        """加载默认精灵"""
        self.current_sprite = Sprite(
            name="Claude",
            emoji="🧠",
            sprite_type=SpriteType.DEFAULT,
            description="AI programming assistant",
        )

    def set_sprite(self, sprite: Sprite) -> None:
        """设置当前精灵"""
        self.current_sprite = sprite

    def get_greeting(self) -> str:
        """获取问候语"""
        if self.current_sprite:
            return f"{self.current_sprite.emoji} {self.current_sprite.name} is ready to help!"
        return "Ready to help!"
```

## 16.2 Coordinator 模块

Coordinator 负责任务协调。

```python
# pyclaude/coordinator/__init__.py
from pyclaude.coordinator.task_coordinator import TaskCoordinator

__all__ = ["TaskCoordinator"]
```

```python
# pyclaude/coordinator/task_coordinator.py
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class CoordinatedTask:
    """协调任务"""
    task_id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[dict] = None
    error: Optional[str] = None


class TaskCoordinator:
    """任务协调器"""

    def __init__(self):
        self.tasks: dict[str, CoordinatedTask] = {}
        self._running: list[str] = []

    def create_task(self, name: str) -> str:
        """创建任务"""
        task_id = str(uuid.uuid4())
        task = CoordinatedTask(task_id=task_id, name=name)
        self.tasks[task_id] = task
        return task_id

    def start_task(self, task_id: str) -> bool:
        """开始任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        task.status = TaskStatus.RUNNING
        self._running.append(task_id)
        return True

    def complete_task(self, task_id: str, result: dict) -> bool:
        """完成任务"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        task.status = TaskStatus.COMPLETED
        task.result = result
        task.completed_at = datetime.now()
        if task_id in self._running:
            self._running.remove(task_id)
        return True

    def fail_task(self, task_id: str, error: str) -> bool:
        """任务失败"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        task.status = TaskStatus.FAILED
        task.error = error
        task.completed_at = datetime.now()
        if task_id in self._running:
            self._running.remove(task_id)
        return True

    def get_task(self, task_id: str) -> Optional[CoordinatedTask]:
        """获取任务"""
        return self.tasks.get(task_id)

    def list_tasks(self) -> list[CoordinatedTask]:
        """列出所有任务"""
        return list(self.tasks.values())
```

## 16.3 Memdir 模块

Memdir 提供基于目录的内存系统。

```python
# pyclaude/memdir/__init__.py
from pyclaude.memdir.memory import MemoryStore
from pyclaude.memdir.entries import MemoryEntry

__all__ = ["MemoryStore", "MemoryEntry"]
```

```python
# pyclaude/memdir/entries.py
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
import uuid


@dataclass
class MemoryEntry:
    """记忆条目"""
    entry_id: str
    content: str
    created_at: datetime
    updated_at: datetime
    tags: list[str]
    metadata: dict[str, Any]
    memory_type: str = "general"

    @staticmethod
    def create(content: str, tags: list[str] = None, metadata: dict = None) -> "MemoryEntry":
        """创建新记忆"""
        now = datetime.now()
        return MemoryEntry(
            entry_id=str(uuid.uuid4()),
            content=content,
            created_at=now,
            updated_at=now,
            tags=tags or [],
            metadata=metadata or {},
        )
```

```python
# pyclaude/memdir/memory.py
from pathlib import Path
from typing import Optional
from pyclaude.memdir.entries import MemoryEntry
import json


class MemoryStore:
    """记忆存储"""

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.home() / ".claude" / "memory"
        self.base_path.mkdir(parents=True, exist_ok=True)

    def add(self, entry: MemoryEntry) -> None:
        """添加记忆"""
        file_path = self.base_path / f"{entry.entry_id}.json"
        with open(file_path, "w") as f:
            json.dump({
                "entry_id": entry.entry_id,
                "content": entry.content,
                "created_at": entry.created_at.isoformat(),
                "updated_at": entry.updated_at.isoformat(),
                "tags": entry.tags,
                "metadata": entry.metadata,
                "memory_type": entry.memory_type,
            }, f)

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        """获取记忆"""
        file_path = self.base_path / f"{entry_id}.json"
        if not file_path.exists():
            return None

        with open(file_path) as f:
            data = json.load(f)

        return MemoryEntry(
            entry_id=data["entry_id"],
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            tags=data["tags"],
            metadata=data["metadata"],
            memory_type=data["memory_type"],
        )

    def search(self, query: str) -> list[MemoryEntry]:
        """搜索记忆"""
        results = []
        for file_path in self.base_path.glob("*.json"):
            with open(file_path) as f:
                data = json.load(f)
            if query.lower() in data["content"].lower():
                results.append(self.get(data["entry_id"]))
        return results
```

## 16.4 Remote 模块

Remote 模块处理远程会话。

```python
# pyclaude/remote/__init__.py
from pyclaude.remote.session import RemoteSession
from pyclaude.remote.manager import RemoteManager

__all__ = ["RemoteSession", "RemoteManager"]
```

```python
# pyclaude/remote/session.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class RemoteSession:
    """远程会话"""
    session_id: str
    created_at: datetime
    last_activity: datetime
    status: str
    remote_address: Optional[str] = None
    metadata: dict = None

    @staticmethod
    def create() -> "RemoteSession":
        """创建新远程会话"""
        now = datetime.now()
        return RemoteSession(
            session_id=str(uuid.uuid4()),
            created_at=now,
            last_activity=now,
            status="active",
        )
```

```python
# pyclaude/remote/manager.py
from typing import Optional
from pyclaude.remote.session import RemoteSession


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
            self.sessions[session_id].status = "closed"
```

## 16.5 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `BuddyEngine` | `class BuddyEngine` | `pyclaude/buddy/engine.py` |
| `Sprite` | `@dataclass Sprite` | `pyclaude/buddy/sprite.py` |
| `TaskCoordinator` | `class TaskCoordinator` | `pyclaude/coordinator/task_coordinator.py` |
| `CoordinatedTask` | `@dataclass CoordinatedTask` | `pyclaude/coordinator/task_coordinator.py` |
| `MemoryStore` | `class MemoryStore` | `pyclaude/memdir/memory.py` |
| `MemoryEntry` | `@dataclass MemoryEntry` | `pyclaude/memdir/entries.py` |
| `RemoteSession` | `@dataclass RemoteSession` | `pyclaude/remote/session.py` |
| `RemoteManager` | `class RemoteManager` | `pyclaude/remote/manager.py` |