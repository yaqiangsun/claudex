# 06 - Bridge 远程桥接

对应 TypeScript: `src/bridge/` - claude.ai 远程控制

## 6.1 Bridge 概述

Bridge 模块实现与 claude.ai 网页的远程控制连接，支持两种模式：
- **v1**: 基于 Environments API
- **v2**: 基于 Session Ingress（无环境依赖）

## 6.2 Bridge 客户端

```python
# pyclaude/bridge/client.py
from typing import Optional, AsyncIterator
from dataclasses import dataclass
from enum import Enum


class BridgeMode(str, Enum):
    """Bridge 模式"""
    V1 = "v1"  # Environments API
    V2 = "v2"  # Session Ingress


@dataclass
class BridgeConfig:
    """Bridge 配置"""
    mode: BridgeMode = BridgeMode.V2
    session_id: Optional[str] = None
    access_token: Optional[str] = None
    endpoint: str = "https://api.anthropic.com"
    transport: str = "websocket"  # websocket, sse, hybrid


class BridgeClient:
    """Bridge 客户端 - 远程控制连接"""

    def __init__(self, config: BridgeConfig):
        self.config = config
        self.session_id = config.session_id
        self.connected = False
        self.transport = None

    async def connect(self) -> None:
        """建立连接"""
        if self.config.transport == "websocket":
            from pyclaude.bridge.transport.websocket import WebSocketTransport
            self.transport = WebSocketTransport(self.config)
        elif self.config.transport == "sse":
            from pyclaude.bridge.transport.sse import SSETransport
            self.transport = SSETransport(self.config)
        else:
            from pyclaude.bridge.transport.hybrid import HybridTransport
            self.transport = HybridTransport(self.config)

        await self.transport.connect()
        self.connected = True

    async def disconnect(self) -> None:
        """断开连接"""
        if self.transport:
            await self.transport.disconnect()
        self.connected = False

    async def send_message(self, message: dict) -> None:
        """发送消息"""
        if not self.connected:
            raise RuntimeError("Not connected")
        await self.transport.send(message)

    async def receive_message(self) -> AsyncIterator[dict]:
        """接收消息"""
        if not self.connected:
            raise RuntimeError("Not connected")
        async for message in self.transport.receive():
            yield message

    async def create_session(self) -> str:
        """创建新会话"""
        if self.config.mode == BridgeMode.V1:
            return await self._create_v1_session()
        else:
            return await self._create_v2_session()

    async def _create_v1_session(self) -> str:
        """创建 v1 会话"""
        # 实现 v1 会话创建
        pass

    async def _create_v2_session(self) -> str:
        """创建 v2 会话"""
        # 实现 v2 会话创建
        pass
```

## 6.3 会话管理

```python
# pyclaude/bridge/session.py
from typing import Optional, AsyncIterator
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Session:
    """会话"""
    session_id: str
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)
    state: str = "active"


class SessionManager:
    """会话管理器"""

    def __init__(self):
        self.sessions: dict[str, Session] = {}
        self.active_session: Optional[Session] = None

    def create_session(self) -> Session:
        """创建新会话"""
        session_id = str(uuid.uuid4())
        session = Session(session_id=session_id)
        self.sessions[session_id] = session
        self.active_session = session
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话"""
        return self.sessions.get(session_id)

    def set_active_session(self, session_id: str) -> bool:
        """设置活动会话"""
        session = self.get_session(session_id)
        if session:
            self.active_session = session
            return True
        return False

    def close_session(self, session_id: str) -> None:
        """关闭会话"""
        if session_id in self.sessions:
            self.sessions[session_id].state = "closed"
            if self.active_session and self.active_session.session_id == session_id:
                self.active_session = None

    def list_sessions(self) -> list[Session]:
        """列出所有会话"""
        return list(self.sessions.values())
```

## 6.4 传输层抽象

```python
# pyclaude/bridge/transport/base.py
from abc import ABC, abstractmethod
from typing import AsyncIterator
from pyclaude.bridge.client import BridgeConfig


class Transport(ABC):
    """传输层基类"""

    def __init__(self, config: BridgeConfig):
        self.config = config
        self.connected = False

    @abstractmethod
    async def connect(self) -> None:
        """建立连接"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """断开连接"""
        pass

    @abstractmethod
    async def send(self, message: dict) -> None:
        """发送消息"""
        pass

    @abstractmethod
    async def receive(self) -> AsyncIterator[dict]:
        """接收消息"""
        pass

    @abstractmethod
    async def is_connected(self) -> bool:
        """检查连接状态"""
        pass
```

## 6.5 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `BridgeApiClient` | `class BridgeClient` | `pyclaude/bridge/client.py` |
| `Session` | `class Session` | `pyclaude/bridge/session.py` |
| `SessionManager` | `class SessionManager` | `pyclaude/bridge/session.py` |
| `Transport` | `class Transport(ABC)` | `pyclaude/bridge/transport/base.py` |
| `WebSocketTransport` | `class WebSocketTransport` | `pyclaude/bridge/transport/websocket.py` |
| `SSETransport` | `class SSETransport` | `pyclaude/bridge/transport/sse.py` |
| `HybridTransport` | `class HybridTransport` | `pyclaude/bridge/transport/hybrid.py` |