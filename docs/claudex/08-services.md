# 08 - 服务层

对应 TypeScript: `src/services/` - 50+ 服务

## 8.1 MCP 服务

```python
# pyclaude/services/mcp.py
from typing import Optional, Any
from dataclasses import dataclass
from enum import Enum
import httpx


class MCPServerType(str, Enum):
    """MCP 服务器类型"""
    STDIO = "stdio"
    HTTP = "http"


@dataclass
class MCPServer:
    """MCP 服务器配置"""
    name: str
    server_type: MCPServerType
    command: Optional[str] = None
    args: list[str] = None
    url: Optional[str] = None
    env: dict[str, str] = None


class MCPClient:
    """MCP 客户端"""

    def __init__(self, server: MCPServer):
        self.server = server
        self.tools = []
        self.resources = []

    async def connect(self) -> None:
        """连接 MCP 服务器"""
        if self.server.server_type == MCPServerType.STDIO:
            await self._connect_stdio()
        else:
            await self._connect_http()

    async def _connect_stdio(self) -> None:
        """STDIO 连接"""
        # 实现 STDIO 连接
        pass

    async def _connect_http(self) -> None:
        """HTTP 连接"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.server.url}/initialize",
                json={"protocolVersion": "2024-11-05"},
            )
            data = response.json()
            self.tools = data.get("tools", [])
            self.resources = data.get("resources", [])

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """调用工具"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.server.url}/tools/call",
                json={
                    "name": tool_name,
                    "arguments": arguments,
                },
            )
            return response.json()

    async def list_tools(self) -> list[dict]:
        """列出工具"""
        return self.tools

    async def list_resources(self) -> list[dict]:
        """列出资源"""
        return self.resources


class MCPManager:
    """MCP 管理器"""

    def __init__(self):
        self.servers: dict[str, MCPServer] = {}
        self.clients: dict[str, MCPClient] = {}

    def add_server(self, server: MCPServer) -> None:
        """添加服务器"""
        self.servers[server.name] = server
        self.clients[server.name] = MCPClient(server)

    async def connect_all(self) -> None:
        """连接所有服务器"""
        for client in self.clients.values():
            await client.connect()

    def get_tools(self) -> list[dict]:
        """获取所有工具"""
        tools = []
        for client in self.clients.values():
            tools.extend(client.tools)
        return tools

    def get_resources(self) -> list[dict]:
        """获取所有资源"""
        resources = []
        for client in self.clients.values():
            resources.extend(client.resources)
        return resources

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> dict:
        """调用工具"""
        client = self.clients.get(server_name)
        if not client:
            raise ValueError(f"MCP server not found: {server_name}")
        return await client.call_tool(tool_name, arguments)
```

## 8.2 Analytics 服务

```python
# pyclaude/services/analytics.py
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
import httpx


@dataclass
class Event:
    """分析事件"""
    event_type: str
    timestamp: datetime
    properties: dict


class AnalyticsService:
    """分析服务"""

    def __init__(self, endpoint: Optional[str] = None):
        self.endpoint = endpoint or "https://api.anthropic.com/v1/analytics"
        self.events = []

    async def track(self, event_type: str, properties: dict = None) -> None:
        """追踪事件"""
        event = Event(
            event_type=event_type,
            timestamp=datetime.now(),
            properties=properties or {},
        )
        self.events.append(event)

        # 异步发送
        asyncio.create_task(self._send_event(event))

    async def _send_event(self, event: Event) -> None:
        """发送事件"""
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    self.endpoint,
                    json={
                        "event_type": event.event_type,
                        "timestamp": event.timestamp.isoformat(),
                        "properties": event.properties,
                    },
                )
        except Exception:
            # 静默失败
            pass

    async def flush(self) -> None:
        """刷新所有待发送事件"""
        events = self.events.copy()
        self.events.clear()
        for event in events:
            await self._send_event(event)
```

## 8.3 模型服务

```python
# pyclaude/services/model.py
from typing import Optional
from dataclasses import dataclass
from enum import Enum


class ModelProvider(str, Enum):
    """模型提供商"""
    ANTHROPIC = "anthropic"
    AWS_BEDROCK = "bedrock"
    AZURE = "azure"


@dataclass
class ModelConfig:
    """模型配置"""
    provider: ModelProvider
    model: str
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    region: Optional[str] = None


class ModelService:
    """模型服务 - 支持多种模型提供商"""

    def __init__(self):
        self.config: Optional[ModelConfig] = None

    def configure(self, config: ModelConfig) -> None:
        """配置模型"""
        self.config = config

    def get_client(self):
        """获取 API 客户端"""
        if self.config.provider == ModelProvider.ANTHROPIC:
            from pyclaude.services.api import APIClient
            return APIClient(
                api_key=self.config.api_key,
                base_url=self.config.endpoint or "https://api.anthropic.com",
            )
        elif self.config.provider == ModelProvider.AWS_BEDROCK:
            from pyclaude.services.bedrock import BedrockClient
            return BedrockClient(
                model=self.config.model,
                region=self.config.region,
            )
        elif self.config.provider == ModelProvider.AZURE:
            from pyclaude.services.azure import AzureOpenAIClient
            return AzureOpenAIClient(
                endpoint=self.config.endpoint,
                api_key=self.config.api_key,
            )
        else:
            raise ValueError(f"Unknown provider: {self.config.provider}")
```

## 8.4 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `MCPClient` | `class MCPClient` | `pyclaude/services/mcp.py` |
| `MCPManager` | `class MCPManager` | `pyclaude/services/mcp.py` |
| `AnalyticsService` | `class AnalyticsService` | `pyclaude/services/analytics.py` |
| `ModelService` | `class ModelService` | `pyclaude/services/model.py` |
| `APIClient` | `class APIClient` | `pyclaude/services/api.py` |
| `BedrockClient` | `class BedrockClient` | `pyclaude/services/bedrock.py` |
| `AzureOpenAIClient` | `class AzureOpenAIClient` | `pyclaude/services/azure.py` |