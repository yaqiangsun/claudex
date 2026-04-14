# 剩余模块分析

本文档分析之前未覆盖的剩余模块。

---

## 一、bootstrap 目录 - 引导状态

### 1.1 目录结构

```
src/bootstrap/
└── state.ts    # 全局引导状态
```

### 1.2 功能

```typescript
// bootstrap/state.ts
type State = {
  originalCwd: string       // 原始工作目录
  projectRoot: string       // 项目根目录
  sessionId: string         // 会话 ID
  channelEntries: ChannelEntry[]  // 渠道配置
  // ...
}

// 渠道类型
type ChannelEntry =
  | { kind: 'plugin'; name: string; marketplace: string; dev?: boolean }
  | { kind: 'server'; name: string; dev?: boolean }
```

---

## 二、entrypoints 目录 - 入口点

### 2.1 目录结构

```
src/entrypoints/
├── cli.tsx            # CLI 入口
├── init.ts            # 初始化入口
├── mcp.ts             # MCP 入口
├── sandboxTypes.ts    # 沙箱类型
├── agentSdkTypes.ts   # Agent SDK 类型
└── sdk/               # SDK 类型定义
    ├── coreTypes.ts   # 核心类型
    ├── coreSchemas.ts # 核心 Schema
    └── controlSchemas.ts  # 控制 Schema
```

### 2.2 Agent SDK 类型

```typescript
// agentSdkTypes.ts
// 用于外部 SDK 集成的类型定义

interface AgentSdkConfig {
  apiKey: string
  model: string
  maxTokens?: number
  // ...
}
```

---

## 三、memdir 目录 - 记忆系统

### 3.1 目录结构

```
src/memdir/
├── memdir.ts              # 记忆目录管理
├── memoryTypes.ts         # 记忆类型
├── memoryAge.ts           # 记忆时长
├── memoryScan.ts          # 记忆扫描
├── paths.ts               # 路径管理
├── findRelevantMemories.ts # 查找相关记忆
├── teamMemPaths.ts        # 团队记忆路径
└── teamMemPrompts.ts      # 团队记忆提示
```

### 3.2 功能概述

```typescript
// 记忆系统 - 自动保存重要信息

interface Memory {
  id: string
  content: string
  createdAt: number
  accessedAt: number
  relevance: number  // 相关性评分
}

// 记忆类型
type MemoryType = 'code' | 'docs' | 'conversation' | 'context'

// 记忆扫描
async function scanForMemories(dir: string): Promise<Memory[]>
async function findRelevantMemories(query: string): Promise<Memory[]>
```

---

## 四、remote 目录 - 远程会话

### 4.1 目录结构

```
src/remote/
├── RemoteSessionManager.ts    # 远程会话管理
├── SessionsWebSocket.ts       # WebSocket 会话
├── remotePermissionBridge.ts # 权限桥接
└── sdkMessageAdapter.ts       # SDK 消息适配器
```

### 4.2 功能

```typescript
// 远程会话管理
interface RemoteSessionManager {
  createSession(config: RemoteConfig): SessionInfo
  attachSession(sessionId: string): Connection
  sendMessage(sessionId: string, message: SDKMessage): void
  disconnect(sessionId: string): void
}

// WebSocket 会话
class SessionsWebSocket {
  connect(url: string): Promise<void>
  send(message: SDKMessage): void
  onMessage(handler: (msg: SDKMessage) => void): void
}
```

---

## 五、types 目录 - 类型定义

### 5.1 目录结构

```
src/types/
├── command.ts       # 命令类型
├── message.ts       # 消息类型
├── hooks.ts         # Hooks 类型
├── ids.ts           # ID 类型
├── logs.ts          # 日志类型
├── permissions.ts   # 权限类型
├── plugin.ts        # 插件类型
└── textInputTypes.ts  # 文本输入类型
```

### 5.2 命令类型

```typescript
// types/command.ts
export type LocalCommandResult =
  | { type: 'text'; value: string }
  | { type: 'compact'; compactionResult: CompactionResult }
  | { type: 'skip' }

export type PromptCommand = {
  type: 'prompt'
  progressMessage: string
  contentLength: number
  argNames?: string[]
  allowedTools?: string[]
  model?: string
  source: SettingSource | 'builtin' | 'mcp' | 'plugin' | 'bundled'
  // ...
}

export type LocalCommand = {
  type: 'local' | 'local-jsx'
  name: string
  command: string
  description?: string
  // ...
}
```

---

## 六、native-ts 目录 - 原生模块

### 6.1 目录结构

```
src/native-ts/
├── color-diff/      # 颜色差异计算
├── file-index/      # 文件索引
└── yoga-layout/     # Yoga 布局引擎
```

### 6.2 功能

- **color-diff**: 计算两个颜色之间的差异
- **file-index**: 快速文件索引
- **yoga-layout**: 跨平台布局引擎 (Facebook Yoga)

---

## 七、schemas 目录 - Schema 定义

### 7.1 目录结构

```
src/schemas/
└── hooks.ts   # Hooks JSON Schema
```

### 7.2 功能

```typescript
// Hooks 配置的 JSON Schema 验证
// 用于配置文件验证
```

---

## 八、upstreamproxy 目录 - 上游代理

### 8.1 目录结构

```
src/upstreamproxy/
├── upstreamproxy.ts  # 上游代理
└── relay.ts          # 转发
```

### 8.2 功能

```typescript
// 上游代理 - 转发请求到其他服务
interface UpstreamProxy {
  forward(request: Request): Promise<Response>
  relay(message: Message): void
}
```

---

## 九、outputStyles 目录 - 输出样式

### 9.1 目录结构

```
src/outputStyles/
└── loadOutputStylesDir.ts  # 加载输出样式目录
```

### 9.2 功能

```typescript
// 加载自定义输出样式
interface OutputStyle {
  name: string
  colors: ColorScheme
  fonts: string[]
}
```

---

## 十、Python 版本实现建议

### 10.1 记忆系统

```python
# claudex/memory/__init__.py
from dataclasses import dataclass
from typing import Literal
import time

MemoryType = Literal["code", "docs", "conversation", "context"]

@dataclass
class Memory:
    id: str
    content: str
    created_at: float
    accessed_at: float
    memory_type: MemoryType
    relevance: float = 0.0

class MemoryManager:
    def __init__(self, memdir: str):
        self.memdir = memdir
        self._memories: dict[str, Memory] = {}

    async def save(self, memory: Memory):
        self._memories[memory.id] = memory
        # 持久化到磁盘

    async def find_relevant(self, query: str) -> list[Memory]:
        # 搜索相关记忆
        # 返回相关性排序结果
        pass

    async def cleanup(self, max_age_days: int = 30):
        # 清理过期记忆
        pass
```

### 10.2 远程会话

```python
# claudex/remote/__init__.py
from dataclasses import dataclass
from enum import Enum
import asyncio

class SessionState(Enum):
    STARTING = "starting"
    RUNNING = "running"
    DETACHED = "detached"
    STOPPING = "stopping"
    STOPPED = "stopped"

@dataclass
class RemoteSession:
    session_id: str
    state: SessionState
    created_at: float
    work_dir: str

class RemoteSessionManager:
    def __init__(self):
        self._sessions: dict[str, RemoteSession] = {}

    async def create(self, work_dir: str) -> RemoteSession:
        session = RemoteSession(
            session_id=generate_id(),
            state=SessionState.STARTING,
            created_at=time.time(),
            work_dir=work_dir
        )
        self._sessions[session.session_id] = session
        return session

    async def attach(self, session_id: str) -> asyncio.Queue:
        # 附加到会话
        pass
```

### 10.3 目录结构

```
claudex/
├── memory/
│   ├── __init__.py
│   ├── manager.py      # MemoryManager
│   ├── types.py        # Memory 类型
│   └── scanner.py      # 记忆扫描

├── remote/
│   ├── __init__.py
│   ├── session.py      # RemoteSession
│   ├── manager.py      # RemoteSessionManager
│   └── websocket.py    # WebSocket 连接

├── bootstrap/
│   ├── __init__.py
│   └── state.py        # 引导状态

└── types/
    ├── __init__.py
    ├── command.py      # 命令类型
    ├── message.py      # 消息类型
    └── hooks.py        # Hooks 类型
```

---

## 十一、模块汇总

| 目录 | 文件数 | 功能 | 复杂度 |
|------|--------|------|--------|
| **utils/** | 329 | 工具函数库 | 已覆盖 |
| **commands/** | 101 | 命令定义 | 已覆盖 |
| **components/** | 144 | React 组件 | 已覆盖 |
| **hooks/** | 85 | React Hooks | 已覆盖 |
| **services/** | 36 | 服务模块 | 已覆盖 |
| **bridge/** | 31 | 桥接模块 | 已覆盖 |
| **tools/** | 43 | 工具实现 | 已覆盖 |
| **ink/** | 48 | CLI 框架 | 已覆盖 |
| **keybindings/** | 14 | 快捷键 | 已覆盖 |
| **memdir/** | 8 | 记忆系统 | 本文档 |
| **tasks/** | 9 | 任务系统 | 已覆盖 |
| **state/** | 6 | 状态管理 | 已覆盖 |
| **buddy/** | 6 | 队友模式 | 已覆盖 |
| **remote/** | 4 | 远程会话 | 本文档 |
| **query/** | 4 | 查询核心 | 已覆盖 |
| **context/** | 9 | Context | 已覆盖 |
| **bootstrap/** | 1 | 引导状态 | 本文档 |
| **entrypoints/** | 6 | 入口点 | 本文档 |
| **types/** | 8 | 类型定义 | 本文档 |
| **schemas/** | 1 | Schema | 本文档 |
| **native-ts/** | 3 | 原生模块 | 本文档 |
| **upstreamproxy/** | 2 | 上游代理 | 本文档 |
| **outputStyles/** | 1 | 输出样式 | 本文档 |

---

## 十二、完整文档清单

| # | 文档 | 内容 |
|---|------|------|
| 01 | architecture-overview.md | 整体架构 |
| 02 | core-modules.md | 核心模块 |
| 03 | bridge-module.md | Bridge 模块 |
| 04 | cli-commands.md | CLI 和命令 |
| 05 | hooks-services.md | Hooks/Services |
| 06 | tools-implementation.md | 工具实现 |
| 07 | utils-library.md | 工具函数 |
| 08 | constants.md | 常量定义 |
| 09 | startup-flow.md | 启动流程 |
| 10 | skills-system.md | 技能系统 |
| 11 | components.md | React 组件 |
| 12 | context-state.md | Context/State |
| 13 | additional-modules.md | Ink/Buddy/Coordinator |
| 14 | input-system.md | Keybindings/Vim/Server |
| 15 | remaining-modules.md | Bootstrap/Memdir/Remote/Types |

---

*文档版本: 1.0*
*分析时间: 2026-04-14*