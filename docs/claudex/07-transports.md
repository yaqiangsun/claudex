# 07 - 传输层

对应 TypeScript: `src/cli/transports/` - 本地 CLI 传输层

## 7.1 传输层概述

传输层负责 CLI 应用与后端服务之间的通信，支持三种模式：
- **WebSocket**: 双向实时通信
- **SSE**: Server-Sent Events 单向通信
- **Hybrid**: 混合模式

## 7.2 WebSocket 传输

```python
# pyclaude/cli/transport/websocket.py
import asyncio
import json
from typing import AsyncIterator
import websockets
from pyclaude.cli.transport.base import Transport, TransportConfig


class WebSocketTransport(Transport):
    """WebSocket 传输"""

    def __init__(self, config: TransportConfig):
        super().__init__(config)
        self.ws = None
        self.receive_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self) -> None:
        """建立 WebSocket 连接"""
        self.ws = await websockets.connect(
            self.config.url,
            extra_headers=self.config.headers,
        )
        self.connected = True
        # 启动接收循环
        asyncio.create_task(self._receive_loop())

    async def disconnect(self) -> None:
        """断开连接"""
        if self.ws:
            await self.ws.close()
        self.connected = False

    async def send(self, message: dict) -> None:
        """发送消息"""
        if not self.ws:
            raise RuntimeError("Not connected")
        await self.ws.send(json.dumps(message))

    async def receive(self) -> AsyncIterator[dict]:
        """接收消息"""
        while self.connected:
            message = await self.receive_queue.get()
            yield message

    async def _receive_loop(self) -> None:
        """接收循环"""
        try:
            async for message in self.ws:
                data = json.loads(message)
                await self.receive_queue.put(data)
        except Exception:
            self.connected = False

    async def is_connected(self) -> bool:
        return self.connected
```

## 7.3 SSE 传输

```python
# pyclaude/cli/transport/sse.py
import asyncio
import json
from typing import AsyncIterator
import sse_starlette
from pyclaude.cli.transport.base import Transport, TransportConfig


class SSETransport(Transport):
    """SSE (Server-Sent Events) 传输"""

    def __init__(self, config: TransportConfig):
        super().__init__(config)
        self.event_source = None
        self.receive_queue: asyncio.Queue = asyncio.Queue()

    async def connect(self) -> None:
        """建立 SSE 连接"""
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "GET",
                self.config.url,
                headers=self.config.headers,
            ) as response:
                self.connected = True
                asyncio.create_task(self._receive_loop(response))

    async def disconnect(self) -> None:
        """断开连接"""
        self.connected = False

    async def send(self, message: dict) -> None:
        """发送消息 (通过 HTTP POST)"""
        async with httpx.AsyncClient() as client:
            await client.post(
                self.config.url,
                json=message,
                headers={**self.config.headers, "Content-Type": "application/json"},
            )

    async def receive(self) -> AsyncIterator[dict]:
        """接收消息"""
        while self.connected:
            message = await self.receive_queue.get()
            yield message

    async def _receive_loop(self, response) -> None:
        """接收循环"""
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                data = line[6:]
                if data:
                    await self.receive_queue.put(json.loads(data))

    async def is_connected(self) -> bool:
        return self.connected
```

## 7.4 Hybrid 传输

```python
# pyclaude/cli/transport/hybrid.py
import asyncio
from typing import AsyncIterator
from pyclaude.cli.transport.websocket import WebSocketTransport
from pyclaude.cli.transport.sse import SSETransport
from pyclaude.cli.transport.base import Transport, TransportConfig


class HybridTransport(Transport):
    """混合传输 - 同时使用 WebSocket 和 SSE"""

    def __init__(self, config: TransportConfig):
        super().__init__(config)
        self.ws_transport = WebSocketTransport(config)
        self.sse_transport = SSETransport(config)
        self._use_ws = True

    async def connect(self) -> None:
        """建立混合连接"""
        # 优先使用 WebSocket，失败则回退到 SSE
        try:
            await self.ws_transport.connect()
            self._use_ws = True
        except Exception:
            await self.sse_transport.connect()
            self._use_ws = False

        self.connected = True

    async def disconnect(self) -> None:
        """断开连接"""
        if self._use_ws:
            await self.ws_transport.disconnect()
        else:
            await self.sse_transport.disconnect()
        self.connected = False

    async def send(self, message: dict) -> None:
        """发送消息"""
        if self._use_ws:
            await self.ws_transport.send(message)
        else:
            await self.sse_transport.send(message)

    async def receive(self) -> AsyncIterator[dict]:
        """接收消息"""
        if self._use_ws:
            async for msg in self.ws_transport.receive():
                yield msg
        else:
            async for msg in self.sse_transport.receive():
                yield msg

    async def is_connected(self) -> bool:
        return self.connected
```

## 7.5 传输配置

```python
# pyclaude/cli/transport/config.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class TransportConfig:
    """传输配置"""
    url: str
    headers: dict = None
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0

    def __post_init__(self):
        if self.headers is None:
            self.headers = {}
```

## 7.6 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `WebSocketTransport` | `class WebSocketTransport` | `pyclaude/cli/transport/websocket.py` |
| `SSETransport` | `class SSETransport` | `pyclaude/cli/transport/sse.py` |
| `HybridTransport` | `class HybridTransport` | `pyclaude/cli/transport/hybrid.py` |
| `TransportConfig` | `class TransportConfig` | `pyclaude/cli/transport/config.py` |