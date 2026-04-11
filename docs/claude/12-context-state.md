# Context 和 State 分析

本文档分析 Claude Code 的 Context Providers 和状态管理系统。

---

## 一、context 目录概览

### 1.1 目录结构

```
src/context/
├── stats.tsx                  # 统计/指标存储 (Reservoir Sampling)
├── fpsMetrics.tsx             # FPS 指标
├── mailbox.tsx                # 消息邮箱
├── notifications.tsx          # 通知系统
├── modalContext.tsx           # 模态框上下文
├── overlayContext.tsx         # 浮层上下文
├── promptOverlayContext.tsx   # 输入框浮层
├── voice.tsx                  # 语音模式
└── QueuedMessageContext.tsx   # 排队消息
```

---

## 二、核心 Context Provider

### 2.1 StatsStore - 统计指标

```typescript
// src/context/stats.tsx
export type StatsStore = {
  increment(name: string, value?: number): void
  set(name: string, value: number): void
  observe(name: string, value: number): void  // Reservoir sampling
  add(name: string, value: string): void
  getAll(): Record<string, number>
}

// 使用 Reservoir Sampling 计算百分位数
function percentile(sorted: number[], p: number): number {
  const index = p / 100 * (sorted.length - 1)
  // 线性插值
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (index - lower)
}
```

### 2.2 FpsMetrics - 帧率监控

```typescript
// src/context/fpsMetrics.tsx
export function useFpsMetrics() {
  // 跟踪 FPS
  // 计算平均帧率、帧时间分布
}
```

### 2.3 Mailbox - 消息队列

```typescript
// src/context/mailbox.tsx
// 跨 Agent/子会话的消息传递
interface Mailbox {
  send(to: string, message: Message): void
  receive(from: string): Message[]
  subscribe(handler: (msg: Message) => void): unsubscribe
}
```

### 2.4 Notifications - 通知系统

```typescript
// src/context/notifications.tsx
type NotificationType =
  | 'info'
  | 'success'
  | 'warning'
  | 'error'
  | 'task_completed'
  | 'tool_result'

interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  timestamp: number
  read: boolean
}
```

---

## 三、plugins 目录

### 3.1 插件系统结构

```
src/plugins/
├── builtinPlugins.ts          # 内置插件
└── bundled/
    └── index.ts               # 插件加载入口
```

### 3.2 插件定义

```typescript
// 插件接口
export interface ClaudePlugin {
  id: string
  name: string
  version: string

  // 插件生命周期
  onLoad?: () => Promise<void>
  onUnload?: () => Promise<void>

  // Hooks
  hooks?: {
    onMessage?: (message: Message) => Message | null
    onToolCall?: (tool: ToolCall) => ToolCall | null
    onStateChange?: (state: AppState) => void
    // ...
  }

  // 提供的工具
  tools?: Tool[]

  // 提供的命令
  commands?: Command[]
}
```

### 3.3 插件加载

```typescript
// bundled/index.ts
export function loadPlugins(): Promise<ClaudePlugin[]> {
  // 加载内置插件
  // 加载用户插件
  // 加载项目插件
  return plugins
}
```

---

## 四、状态管理模式

### 4.1 AppState 结构

```typescript
// src/state/AppState.ts
interface AppState {
  // 会话
  sessionId: string
  messages: Message[]

  // 输入
  inputText: string
  isSubmitting: boolean

  // 工具
  tools: Tool[]
  allowedTools: string[]

  // 任务
  tasks: Task[]

  // 设置
  settings: Settings

  // UI 状态
  isExpanded: boolean
  showDialog: string | null

  // 远程
  isRemote: boolean
  remoteSession: RemoteSession | null
}
```

### 4.2 状态更新模式

```typescript
// 使用 hooks 更新状态
const setAppState = useSetAppState()

// 单一更新
setAppState({ inputText: 'hello' })

// 函数式更新
setAppState(prev => ({
  ...prev,
  messages: [...prev.messages, newMessage]
}))
```

---

## 五、Python 版本实现建议

### 5.1 Context Provider 模拟

```python
# claudex/ui/context.py
from typing import Any, Callable, Generic, TypeVar
from dataclasses import dataclass, field
from collections import defaultdict
import time

T = TypeVar('T')

class ContextProvider(Generic[T]):
    """Base context provider"""

    def __init__(self, default_value: T):
        self._value = default_value
        self._subscribers: list[Callable[[T], None]] = []

    def get(self) -> T:
        return self._value

    def set(self, value: T):
        self._value = value
        for callback in self._subscribers:
            callback(value)

    def subscribe(self, callback: Callable[[T], None]):
        self._subscribers.append(callback)
        return lambda: self._subscribers.remove(callback)
```

### 5.2 统计指标实现

```python
# claudex/ui/stats.py
from dataclasses import dataclass, field
from collections import deque
import statistics

RESERVOIR_SIZE = 1024

@dataclass
class Histogram:
    reservoir: deque = field(default_factory=lambda: deque(maxlen=RESERVOIR_SIZE))
    count: int = 0
    sum: float = 0.0
    min: float = float('inf')
    max: float = float('-inf')

class StatsStore:
    def __init__(self):
        self._metrics: dict[str, float] = {}
        self._histograms: dict[str, Histogram] = {}
        self._sets: dict[str, set[str]] = defaultdict(set)

    def increment(self, name: str, value: float = 1):
        self._metrics[name] = self._metrics.get(name, 0) + value

    def observe(self, name: str, value: float):
        if name not in self._histograms:
            self._histograms[name] = Histogram()
        h = self._histograms[name]
        h.reservoir.append(value)
        h.count += 1
        h.sum += value
        h.min = min(h.min, value)
        h.max = max(h.max, value)

    def percentile(self, name: str, p: float) -> float:
        h = self._histograms.get(name)
        if not h or not h.reservoir:
            return 0.0
        sorted_values = sorted(h.reservoir)
        index = p / 100 * (len(sorted_values) - 1)
        lower = int(index)
        upper = min(lower + 1, len(sorted_values) - 1)
        if lower == upper:
            return sorted_values[lower]
        # 线性插值
        return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * (index - lower)

    def get_all(self) -> dict[str, float]:
        return dict(self._metrics)
```

### 5.3 通知系统

```python
# claudex/ui/notifications.py
from dataclasses import dataclass
from typing import Literal
from enum import Enum
import time

NotificationType = Literal["info", "success", "warning", "error", "task_completed", "tool_result"]

@dataclass
class Notification:
    id: str
    type: NotificationType
    title: str
    message: str
    timestamp: float
    read: bool = False

class NotificationManager:
    def __init__(self):
        self._notifications: list[Notification] = []
        self._subscribers: list[Callable[[Notification], None]] = []

    def add(self, notification: Notification):
        self._notifications.append(notification)
        for callback in self._subscribers:
            callback(notification)

    def mark_read(self, notification_id: str):
        for n in self._notifications:
            if n.id == notification_id:
                n.read = True
                break

    def subscribe(self, callback):
        self._subscribers.append(callback)
        return lambda: self._subscribers.remove(callback)
```

### 5.4 目录结构

```
claudex/ui/
├── context/
│   ├── __init__.py
│   ├── provider.py      # ContextProvider 基类
│   ├── stats.py         # 统计指标
│   └── notifications.py # 通知系统
├── plugins/
│   ├── __init__.py
│   ├── base.py          # Plugin 接口
│   ├── loader.py        # 插件加载
│   └── builtin.py       # 内置插件
└── state/
    ├── __init__.py
    ├── app_state.py     # AppState 定义
    └── store.py         # 状态存储
```

---

## 六、核心模式总结

| 模式 | 用途 | 关键实现 |
|------|------|----------|
| Provider | 跨组件共享状态 | React Context |
| Reservoir Sampling | 高效百分位数计算 | StatsStore.observe() |
| Observer | 状态变更通知 | Store 模式 |
| Mailbox | 跨会话消息 | 消息队列 |
| Hooks | 状态访问 | useAppState() |

---

*文档版本: 1.0*
*分析时间: 2026-04-11*