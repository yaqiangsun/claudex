# 08 - 服务层

对应 TypeScript: `src/services/` - 50+ 服务

## 8.1 MCP (Model Context Protocol) 服务

### 8.1.1 MCP 概述

MCP 是一个标准化协议，用于 Claude Code 与外部服务/工具的连接。支持多种传输方式和认证机制。

### 8.1.2 MCP 服务器配置类型

```python
# pyclaude/services/mcp/types.py
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class MCPServerType(str, Enum):
    """MCP 服务器类型"""
    STDIO = "stdio"           # 本地进程
    SSE = "sse"               # Server-Sent Events
    HTTP = "http"             # Streamable HTTP
    WS = "ws"                 # WebSocket


@dataclass
class OAuthConfig:
    """OAuth 认证配置"""
    client_id: str
    client_secret: str
    token_url: str
    scopes: list[str] = field(default_factory=list)


@dataclass
class MCPServerConfig:
    """MCP 服务器配置"""
    name: str
    server_type: MCPServerType

    # STDIO 配置
    command: Optional[str] = None
    args: list[str] = field(default_factory=list)
    env: Optional[dict[str, str]] = None

    # HTTP/SSE/WS 配置
    url: Optional[str] = None
    headers: Optional[dict[str, str]] = None
    oauth: Optional[OAuthConfig] = None


# 配置作用域
class MCPScope(str, Enum):
    """MCP 配置作用域"""
    LOCAL = "local"      # .mcp.json 当前目录
    USER = "user"        # ~/.claude/mcp.json
    PROJECT = "project"  # 项目级配置
    MANAGED = "managed"  # 企业托管策略
```

### 8.1.3 MCP 客户端

```python
# pyclaude/services/mcp/client.py
from typing import Optional, Any
from dataclasses import dataclass
from enum import Enum

from pyclaude.services.mcp.types import MCPServerConfig, MCPServerType


class MCPToolInputSchema:
    """MCP 工具输入模式"""
    pass


class MCPToolResult:
    """MCP 工具结果"""
    def __init__(
        self,
        content: list[dict],
        is_error: bool = False,
    ):
        self.content = content
        self.is_error = is_error


class MCPConnectionState(str, Enum):
    """连接状态"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class MCPServerConnection:
    """MCP 服务器连接"""
    client: Any  # MCP Client 实例
    state: MCPConnectionState
    capabilities: dict = field(default_factory=dict)
    transport_info: dict = field(default_factory=dict)


class MCPClient:
    """MCP 客户端 - 连接到 MCP 服务器"""

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.connection: Optional[MCPServerConnection] = None
        self._tools = []
        self._resources = []

    async def connect(self) -> MCPServerConnection:
        """连接到 MCP 服务器"""
        if self.config.server_type == MCPServerType.STDIO:
            return await self._connect_stdio()
        elif self.config.server_type == MCPServerType.SSE:
            return await self._connect_sse()
        elif self.config.server_type == MCPServerType.HTTP:
            return await self._connect_http()
        elif self.config.server_type == MCPServerType.WS:
            return await self._connect_ws()
        else:
            raise ValueError(f"Unknown server type: {self.config.server_type}")

    async def _connect_stdio(self) -> MCPServerConnection:
        """STDIO 传输 - 本地进程"""
        # 使用 subprocess 启动进程
        # 通过 stdin/stdout 与 MCP 协议通信
        from pyclaude.services.mcp.transport.stdio import StdioTransport

        transport = StdioTransport(
            command=self.config.command,
            args=self.config.args,
            env=self.config.env,
        )

        # 创建 MCP 客户端并连接
        from mcp import Client
        client = Client(
            name=self.config.name,
            version="1.0.0",
            capabilities={},
        )

        await client.connect(transport)

        # 获取服务器能力
        initialize_result = await client.request_initialize({})
        self._tools = initialize_result.get("tools", [])
        self._resources = initialize_result.get("resources", [])

        return MCPServerConnection(
            client=client,
            state=MCPConnectionState.CONNECTED,
            capabilities=initialize_result.get("capabilities", {}),
            transport_info={"type": "stdio"},
        )

    async def _connect_sse(self) -> MCPServerConnection:
        """SSE 传输 - Server-Sent Events"""
        from pyclaude.services.mcp.transport.sse import SSETransport

        transport = SSETransport(
            url=self.config.url,
            headers=self.config.headers,
            auth_provider=self._create_auth_provider(),
        )

        return await self._create_connection(transport)

    async def _connect_http(self) -> MCPServerConnection:
        """HTTP 传输 - Streamable HTTP"""
        from pyclaude.services.mcp.transport.http import StreamableHTTPTransport

        transport = StreamableHTTPTransport(
            url=self.config.url,
            headers=self.config.headers,
            auth_provider=self._create_auth_provider(),
        )

        return await self._create_connection(transport)

    async def _connect_ws(self) -> MCPServerConnection:
        """WebSocket 传输"""
        from pyclaude.services.mcp.transport.websocket import WebSocketTransport

        transport = WebSocketTransport(
            url=self.config.url,
            headers=self.config.headers,
        )

        return await self._create_connection(transport)

    async def _create_connection(self, transport) -> MCPServerConnection:
        """创建通用连接"""
        from mcp import Client

        client = Client(
            name=self.config.name,
            version="1.0.0",
            capabilities={},
        )

        await client.connect(transport)

        initialize_result = await client.request_initialize({})
        self._tools = initialize_result.get("tools", [])
        self._resources = initialize_result.get("resources", [])

        return MCPServerConnection(
            client=client,
            state=MCPConnectionState.CONNECTED,
            capabilities=initialize_result.get("capabilities", {}),
            transport_info={"type": transport.__class__.__name__},
        )

    def _create_auth_provider(self):
        """创建认证提供者"""
        if self.config.oauth:
            return OAuthProvider(self.config.oauth)
        return None

    async def call_tool(self, name: str, arguments: dict) -> MCPToolResult:
        """调用工具"""
        if not self.connection:
            raise RuntimeError("Not connected")

        result = await self.connection.client.call_tool({
            "name": name,
            "arguments": arguments,
        })

        return MCPToolResult(
            content=result.get("content", []),
            is_error=result.get("isError", False),
        )

    async def list_tools(self) -> list[dict]:
        """列出工具"""
        return self._tools

    async def list_resources(self) -> list[dict]:
        """列出资源"""
        return self._resources

    async def disconnect(self) -> None:
        """断开连接"""
        if self.connection:
            await self.connection.client.close()
            self.connection = None
```

### 8.1.4 MCP 管理器

```python
# pyclaude/services/mcp/manager.py
from pathlib import Path
from typing import Optional
import json

from pyclaude.services.mcp.types import MCPServerConfig, MCPScope
from pyclaude.services.mcp.client import MCPClient


class MCPManager:
    """MCP 管理器"""

    def __init__(self):
        self.servers: dict[str, MCPServerConfig] = {}
        self.clients: dict[str, MCPClient] = {}
        self._load_configs()

    def _load_configs(self) -> None:
        """从配置文件加载"""
        # LOCAL: .mcp.json
        local_config = Path(".mcp.json")
        if local_config.exists():
            self._load_config_file(local_config, MCPScope.LOCAL)

        # USER: ~/.claude/mcp.json
        user_config = Path.home() / ".claude" / "mcp.json"
        if user_config.exists():
            self._load_config_file(user_config, MCPScope.USER)

    def _load_config_file(self, path: Path, scope: MCPScope) -> None:
        """加载配置文件"""
        with open(path) as f:
            data = json.load(f)

        for name, config in data.get("mcpServers", {}).items():
            server_config = MCPServerConfig(
                name=name,
                server_type=MCPServerType(config.get("type", "stdio")),
                command=config.get("command"),
                args=config.get("args", []),
                env=config.get("env"),
                url=config.get("url"),
                headers=config.get("headers"),
            )
            self.add_server(server_config)

    def add_server(self, config: MCPServerConfig) -> None:
        """添加服务器"""
        self.servers[config.name] = config
        self.clients[config.name] = MCPClient(config)

    def remove_server(self, name: str) -> None:
        """移除服务器"""
        if name in self.clients:
            # 断开连接
            import asyncio
            asyncio.create_task(self.clients[name].disconnect())

        del self.servers[name]
        del self.clients[name]

    async def connect_all(self) -> None:
        """连接所有服务器"""
        for client in self.clients.values():
            try:
                await client.connect()
            except Exception as e:
                print(f"Failed to connect: {e}")

    def get_all_tools(self) -> list[dict]:
        """获取所有工具"""
        tools = []
        for client in self.clients.values():
            if client.connection:
                tools.extend(client._tools)
        return tools

    def get_all_resources(self) -> list[dict]:
        """获取所有资源"""
        resources = []
        for client in self.clients.values():
            if client.connection:
                resources.extend(client._resources)
        return resources

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> dict:
        """调用工具"""
        client = self.clients.get(server_name)
        if not client:
            raise ValueError(f"MCP server not found: {server_name}")
        return await client.call_tool(tool_name, arguments)
```

### 8.1.5 MCP CLI 命令

```bash
# MCP CLI 命令设计
claude mcp add <name> <config>     # 添加 MCP 服务器
claude mcp remove <name>           # 移除 MCP 服务器
claude mcp list                    # 列出所有服务器
claude mcp get <name>              # 获取服务器详情
claude mcp serve                   # 作为 MCP 服务器运行
```

### 8.1.6 MCP 服务器模式 (PyClaude 作为服务端)

```python
# pyclaude/services/mcp/server.py
"""
PyClaude 作为 MCP 服务器运行
暴露所有工具给外部客户端
"""
from mcp.server import Server
from mcp.types import Tool, TextContent

from pyclaude.tools.registry import ToolRegistry


class MCPServer:
    """MCP 服务器 - PyClaude 作为服务端"""

    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.server = Server(
            name="pyclaude",
            version="1.0.0",
            capabilities={"tools": {}},
        )
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """设置请求处理器"""

        @self.server.list_tools()
        async def list_tools():
            """列出所有可用工具"""
            tools = []
            for tool in self.tool_registry.get_tool_definitions():
                tools.append(Tool(
                    name=tool.name,
                    description=tool.description,
                    inputSchema=tool.input_schema,
                ))
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            """处理工具调用"""
            tool = self.tool_registry.get(name)
            if not tool:
                return [TextContent(type="text", text=f"Tool not found: {name}")]

            try:
                result = await tool.execute(arguments)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                return [TextContent(type="text", text=str(e), isError=True)]

    async def run(self) -> None:
        """运行 MCP 服务器"""
        from mcp.transport import StdioTransport

        transport = StdioTransport()
        await self.server.connect(transport)
```

### 8.1.7 MCP 传输层

```python
# pyclaude/services/mcp/transport/stdio.py
import asyncio
from typing import Optional


class StdioTransport:
    """STDIO 传输"""

    def __init__(
        self,
        command: str,
        args: list[str],
        env: Optional[dict[str, str]] = None,
    ):
        self.command = command
        self.args = args
        self.env = env
        self.process: Optional[asyncio.subprocess.Process] = None

    async def connect(self) -> None:
        """启动进程并连接"""
        self.process = await asyncio.create_subprocess_exec(
            self.command,
            *self.args,
            env=self.env,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

    async def send(self, message: dict) -> None:
        """发送消息"""
        if not self.process or not self.process.stdin:
            raise RuntimeError("Not connected")

        import json
        self.process.stdin.write(json.dumps(message).encode() + b"\n")
        await self.process.stdin.drain()

    async def receive(self) -> dict:
        """接收消息"""
        if not self.process or not self.process.stdout:
            raise RuntimeError("Not connected")

        line = await self.process.stdout.readline()
        import json
        return json.loads(line.decode())

    async def close(self) -> None:
        """关闭连接"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
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
| `MCPServerConfig` | `class MCPServerConfig` | `pyclaude/services/mcp/types.py` |
| `MCPClient` | `class MCPClient` | `pyclaude/services/mcp/client.py` |
| `MCPManager` | `class MCPManager` | `pyclaude/services/mcp/manager.py` |
| `MCPServer` | `class MCPServer` | `pyclaude/services/mcp/server.py` |
| `StdioTransport` | `class StdioTransport` | `pyclaude/services/mcp/transport/stdio.py` |
| `SSETransport` | `class SSETransport` | `pyclaude/services/mcp/transport/sse.py` |
| `StreamableHTTPTransport` | `class StreamableHTTPTransport` | `pyclaude/services/mcp/transport/http.py` |
| `OAuthProvider` | `class OAuthProvider` | `pyclaude/services/mcp/auth.py` |
| `AnalyticsService` | `class AnalyticsService` | `pyclaude/services/analytics.py` |
| `ModelService` | `class ModelService` | `pyclaude/services/model.py` |