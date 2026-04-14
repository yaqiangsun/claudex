# 02 - 核心引擎模块

本模块实现 Claude Code 的核心引擎系统，包括 QueryEngine、Task 定义、Tool 抽象基类。

## 2.1 Task 定义

对应 TypeScript: `src/Task.ts`

### 功能
- 定义任务类型枚举
- 定义任务相关的数据结构

### Python 实现

```python
# pyclaude/core/task.py
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class TaskType(str, Enum):
    """任务类型枚举"""
    LOCAL_BASH = "local_bash"           # 本地 Bash 命令
    LOCAL_AGENT = "local_agent"         # 本地 Agent
    REMOTE_AGENT = "remote_agent"       # 远程 Agent
    TOOL_USE = "tool_use"               # 工具使用
    TOOL_RESULT = "tool_result"         # 工具结果
    TEXT = "text"                       # 文本消息
    SYSTEM = "system"                   # 系统消息
    ENTRY = "entry"                     # 入口点


class Task(BaseModel):
    """任务模型"""
    task_type: TaskType
    message: str = ""
    tool_name: Optional[str] = None
    tool_input: dict[str, Any] = Field(default_factory=dict)
    tool_id: Optional[str] = None
    parent_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskResult(BaseModel):
    """任务结果"""
    task_id: str
    task_type: TaskType
    result: Any
    error: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
```

## 2.2 Tool 抽象基类

对应 TypeScript: `src/Tool.ts`

### 功能
- 定义工具接口协议
- 工具能力定义（并发安全、只读、破坏性）
- 权限检查
- 工具注册与发现

### Python 实现

```python
# pyclaude/tools/base.py
from abc import ABC, abstractmethod
from enum import Flag, auto
from typing import Any, Optional
from pydantic import BaseModel, Field


class ToolCapability(Flag):
    """工具能力标志"""
    NONE = 0
    CONCURRENT_SAFE = auto()     # 并发安全
    READ_ONLY = auto()           # 只读操作
    DESTRUCTIVE = auto()         # 破坏性操作
    HIDDEN = auto()              # 隐藏工具（不显示给用户）


class PermissionResult(BaseModel):
    """权限检查结果"""
    allowed: bool
    reason: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolDefinition(BaseModel):
    """工具定义"""
    name: str
    description: str
    input_schema: dict[str, Any]
    capability: ToolCapability = ToolCapability.NONE
    visible: bool = True


class BaseTool(ABC):
    """工具基类"""

    @abstractmethod
    def get_definition(self) -> ToolDefinition:
        """获取工具定义"""
        pass

    @abstractmethod
    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """执行工具"""
        pass

    async def validate_input(self, tool_input: dict[str, Any]) -> bool:
        """验证输入"""
        return True

    async def check_permission(self, tool_input: dict[str, Any]) -> PermissionResult:
        """权限检查（默认允许）"""
        return PermissionResult(allowed=True)
```

## 2.3 QueryEngine

对应 TypeScript: `src/QueryEngine.ts`

### 功能
- 管理对话生命周期
- 消息历史管理
- 工具执行上下文
- 上下文压缩
- 会话管理

### Python 实现

```python
# pyclaude/engine.py
from typing import Optional, AsyncIterator
from dataclasses import dataclass, field

from pyclaude.core.task import Task, TaskType, TaskResult
from pyclaude.core.query import QueryLoop
from pyclaude.tools.registry import ToolRegistry
from pyclaude.commands.registry import CommandRegistry
from pyclaude.state.store import Store
from pyclaude.core.history import MessageHistory
from pyclaude.services.api import APIClient


@dataclass
class QueryEngineConfig:
    """QueryEngine 配置"""
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 8192
    system_prompt: Optional[str] = None
    max_conversation_turns: int = 100
    context_window: int = 200000


class QueryEngine:
    """核心查询引擎"""

    def __init__(
        self,
        api_client: APIClient,
        tool_registry: ToolRegistry,
        command_registry: CommandRegistry,
        store: Store,
        config: Optional[QueryEngineConfig] = None,
    ):
        self.api_client = api_client
        self.tool_registry = tool_registry
        self.command_registry = command_registry
        self.store = store
        self.config = config or QueryEngineConfig()
        self.query_loop = QueryLoop(api_client, tool_registry, self.config)
        self.history = MessageHistory(max_turns=self.config.max_conversation_turns)

    async def query(
        self,
        user_message: str,
        session_id: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """执行查询，返回流式响应"""
        # 1. 解析命令
        command_result = await self.command_registry.parse(user_message)
        if command_result:
            yield command_result
            return

        # 2. 添加用户消息到历史
        self.history.add_message("user", user_message)

        # 3. 构建上下文
        context = await self._build_context()

        # 4. 执行查询循环
        async for chunk in self.query_loop.execute(
            messages=context,
            tools=self.tool_registry.get_tool_definitions(),
            session_id=session_id,
        ):
            # 5. 处理工具调用
            if chunk.get("type") == "tool_use":
                await self._handle_tool_use(chunk)
            elif chunk.get("type") == "content_block":
                self.history.add_message("assistant", chunk.get("text", ""))

            yield chunk

    async def _build_context(self) -> list[dict]:
        """构建对话上下文"""
        messages = []

        # 添加系统提示
        if self.config.system_prompt:
            messages.append({
                "role": "system",
                "content": self.config.system_prompt
            })

        # 添加历史消息
        messages.extend(self.history.get_messages())

        return messages

    async def _handle_tool_use(self, chunk: dict) -> dict:
        """处理工具调用"""
        tool_name = chunk.get("name")
        tool_input = chunk.get("input", {})
        tool_id = chunk.get("id")

        # 获取工具
        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            return {
                "type": "tool_result",
                "tool_id": tool_id,
                "content": f"Tool not found: {tool_name}",
                "is_error": True,
            }

        # 权限检查
        permission = await tool.check_permission(tool_input)
        if not permission.allowed:
            return {
                "type": "tool_result",
                "tool_id": tool_id,
                "content": permission.reason or "Permission denied",
                "is_error": True,
            }

        # 执行工具
        try:
            result = await tool.execute(tool_input)
            self.history.add_message(
                "user",
                f"[Tool: {tool_name}] {result}",
                tool_result=True,
            )
            return {
                "type": "tool_result",
                "tool_id": tool_id,
                "content": result,
                "is_error": False,
            }
        except Exception as e:
            return {
                "type": "tool_result",
                "tool_id": tool_id,
                "content": str(e),
                "is_error": True,
            }

    async def reset_session(self) -> None:
        """重置会话"""
        self.history.clear()

    async def compress_context(self) -> None:
        """压缩上下文"""
        # 调用上下文压缩服务
        compressed = await self._compress_messages(self.history.get_messages())
        self.history.replace_all(compressed)

    async def _compress_messages(self, messages: list[dict]) -> list[dict]:
        """压缩消息（调用 AI）"""
        # 实现上下文压缩逻辑
        pass
```

## 2.4 消息历史管理

对应 TypeScript: `src/history.ts`

### 功能
- 用户输入历史记录
- JSONL 格式持久化
- 历史搜索

### Python 实现

```python
# pyclaude/core/history.py
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Message:
    """消息"""
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    tool_name: Optional[str] = None
    tool_result: bool = False


class MessageHistory:
    """消息历史管理器"""

    def __init__(self, history_file: Optional[Path] = None, max_turns: int = 100):
        self.history_file = history_file or Path.home() / ".claude" / "history.jsonl"
        self.max_turns = max_turns
        self.messages: list[dict] = []
        self._load_history()

    def add_message(
        self,
        role: str,
        content: str,
        tool_name: Optional[str] = None,
        tool_result: bool = False,
    ) -> None:
        """添加消息"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }
        if tool_name:
            message["tool_name"] = tool_name
        if tool_result:
            message["tool_result"] = tool_result

        self.messages.append(message)
        self._save_message(message)

        # 限制历史长度
        if len(self.messages) > self.max_turns * 2:
            self.messages = self.messages[-self.max_turns * 2:]

    def get_messages(self) -> list[dict]:
        """获取消息列表"""
        return self.messages.copy()

    def clear(self) -> None:
        """清空历史"""
        self.messages.clear()

    def replace_all(self, messages: list[dict]) -> None:
        """替换所有消息（用于压缩后）"""
        self.messages = messages

    def _load_history(self) -> None:
        """加载历史记录"""
        if not self.history_file.exists():
            return

        try:
            with open(self.history_file, "r") as f:
                self.messages = [json.loads(line) for line in f]
        except Exception:
            pass

    def _save_message(self, message: dict) -> None:
        """保存单条消息"""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_file, "a") as f:
            f.write(json.dumps(message) + "\n")

    def search(self, query: str) -> list[dict]:
        """搜索历史"""
        return [
            msg for msg in self.messages
            if query.lower() in msg.get("content", "").lower()
        ]
```

## 2.5 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `QueryEngine` | `class QueryEngine` | `pyclaude/engine.py` |
| `TaskType` | `enum TaskType` | `pyclaude/core/task.py` |
| `Task` | `class Task(BaseModel)` | `pyclaude/core/task.py` |
| `BaseTool` | `class BaseTool(ABC)` | `pyclaude/tools/base.py` |
| `ToolDefinition` | `class ToolDefinition(BaseModel)` | `pyclaude/tools/base.py` |
| `PermissionResult` | `class PermissionResult(BaseModel)` | `pyclaude/tools/base.py` |
| `ToolCapability` | `enum ToolCapability(Flag)` | `pyclaude/tools/base.py` |
| `MessageHistory` | `class MessageHistory` | `pyclaude/core/history.py` |