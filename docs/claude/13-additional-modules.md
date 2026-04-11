# 其他重要模块分析

本文档分析之前未覆盖的重要模块：Buddy、Coordinator、Ink、Screens、Voice、Assistant。

---

## 一、buddy 目录 - 队友模式

### 1.1 目录结构

```
src/buddy/
├── companion.ts         # 队友核心逻辑
├── types.ts            # 类型定义
├── sprites.ts          # 角色精灵图
├── prompt.ts           # 队友提示词
├── useBuddyNotification.tsx  # 通知 Hook
└── CompanionSprite.tsx # 角色组件
```

### 1.2 功能概述

```typescript
// buddy 类型
interface Buddy {
  id: string
  name: string
  sprite: Sprite  // 视觉表现
  personality: string

  // 交互
  onMessage: (msg: string) => Promise<string>
  onAction: (action: Action) => void
}

// 队友通知
function useBuddyNotification() {
  // 监听事件，推送队友消息
}
```

---

## 二、coordinator 目录 - 协调者模式

### 2.1 目录结构

```
src/coordinator/
└── coordinatorMode.ts   # 协调者模式逻辑
```

### 2.2 功能概述

```typescript
// 协调者模式 - 管理多个子 Agent
interface CoordinatorMode {
  agents: Agent[]

  // 任务分配
  assignTask(agent: Agent, task: Task): void

  // 结果汇总
  aggregateResults(results: Result[]): Result

  // 协调策略
  strategy: 'parallel' | 'sequential' | 'hierarchical'
}
```

---

## 三、ink 目录 - Ink CLI 框架

### 3.1 统计信息

- **文件数量**: 50+ 个
- **框架**: Ink (React for CLI)

### 3.2 核心模块

```
src/ink/
├── ink.tsx              # 主入口
├── screen.ts            # 屏幕管理
├── renderer.ts          # 渲染器
├── components/          # Ink 基础组件
│   ├── Box.tsx
│   ├── Text.tsx
│   └── ...
├── hooks/               # Ink Hooks
│   ├── useInput.ts
│   ├── useApp.ts
│   └── ...
├── events/              # 事件处理
├── layout/              # 布局系统
├── terminal.ts          # 终端交互
├── dom.ts               # DOM 模拟
└── styles.ts            # 样式系统
```

### 3.3 核心类型

```typescript
// 屏幕/渲染
interface Screen {
  width: number
  height: number
  rows: Row[]

  render(): void
  clear(): void
}

// 组件
interface InkComponent {
  props: Props
  mount(): void
  unmount(): void
  render(): void
}

// 样式
interface TextStyle {
  bold?: boolean
  dim?: boolean
  italic?: boolean
  underline?: boolean
  inverse?: boolean
  strikethrough?: boolean
  color?: string
  backgroundColor?: string
}
```

### 3.4 Ink 使用示例

```typescript
// 使用 Ink 创建 CLI 应用
import { render, Box, Text } from 'ink'

const App = () => (
  <Box flexDirection="column">
    <Text bold>Hello World</Text>
    <Text color="green">Success!</Text>
  </Box>
)

render(<App />)
```

---

## 四、screens 目录 - 屏幕组件

### 4.1 目录结构

```
src/screens/
├── Doctor.tsx           # 健康检查屏幕
├── REPL.tsx             # REPL 主屏幕
└── ResumeConversation.tsx  # 恢复会话屏幕
```

### 4.2 屏幕组件示例

```typescript
// Doctor.tsx - 健康检查屏幕
export function Doctor({ onComplete }) {
  // 运行诊断检查
  // 显示结果
  // 提供修复建议
}

// REPL.tsx - 主交互屏幕
export function REPL({ tools, commands, messages }) {
  return (
    <Box flexDirection="column">
      <Messages messages={messages} />
      <PromptInput />
    </Box>
  )
}
```

---

## 五、voice 目录 - 语音模式

### 5.1 目录结构

```
src/voice/
├── sessionHistory.ts    # 会话历史
└── voiceModeEnabled.ts  # 语音模式状态
```

### 5.2 功能概述

```typescript
// 语音模式配置
interface VoiceConfig {
  enabled: boolean
  wakeWord: string
  language: string

  // 音频处理
  inputDevice: string
  outputDevice: string

  // TTS/STT
  ttsEngine: 'default' | 'custom'
  sttEngine: 'default' | 'custom'
}
```

---

## 六、assistant 目录 - 助手相关

### 6.1 目录结构

```
src/assistant/
└── sessionHistory.ts    # 会话历史管理
```

### 6.2 功能概述

```typescript
// 会话历史
interface SessionHistory {
  sessionId: string
  messages: Message[]

  // 操作
  add(message: Message): void
  getMessages(): Message[]
  clear(): void
  export(): string
}
```

---

## 七、Python 版本实现建议

### 7.1 Ink 渲染系统

```python
# claudex/ui/ink/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Literal

T = TypeVar('T')

# 样式
@dataclass
class Style:
    bold: bool = False
    dim: bool = False
    italic: bool = False
    underline: bool = False
    color: str | None = None
    background_color: str | None = None

# 组件基类
class InkComponent(ABC):
    @abstractmethod
    def render(self, width: int, height: int) -> list[str]:
        pass

# Box 组件
class Box(InkComponent):
    def __init__(
        self,
        children: list[InkComponent] | None = None,
        flex_direction: Literal["row", "column"] = "row",
        justify_content: str = "flex-start",
        align_items: str = "stretch",
        width: int | None = None,
        height: int | None = None,
        style: Style | None = None,
    ):
        self.children = children or []
        self.flex_direction = flex_direction
        # ...

    def render(self, width: int, height: int) -> list[str]:
        # 布局计算
        # 子组件渲染
        # 返回行列表
        pass

# Text 组件
class Text(InkComponent):
    def __init__(self, content: str, style: Style | None = None):
        self.content = content
        self.style = style or Style()

    def render(self, width: int, height: int) -> list[str]:
        # 文本着色
        # 换行处理
        return [self._apply_style(self.content)]
```

### 7.2 屏幕管理

```python
# claudex/ui/ink/screen.py
import shutil
from typing import Callable

class Screen:
    def __init__(self):
        self.width, self.height = shutil.get_terminal_size()
        self.rows: list[str] = []
        self.cursor_x = 0
        self.cursor_y = 0

    def clear(self):
        """清屏"""
        print("\033[2J\033[H", end="")

    def render(self, component: InkComponent):
        """渲染组件到屏幕"""
        self.rows = component.render(self.width, self.height)
        self._draw()

    def _draw(self):
        self.clear()
        for row in self.rows:
            print(row)

    def move_cursor(self, x: int, y: int):
        self.cursor_x = x
        self.cursor_y = y
        print(f"\033[{y};{x}H", end="")
```

### 7.3 目录结构

```
claudex/ui/ink/
├── __init__.py
├── base.py              # InkComponent, Style, Box, Text
├── screen.py            # Screen 管理
├── renderer.py          # 渲染器
├── hooks.py             # Input hooks
├── events.py            # 事件处理
└── styles.py            # 样式系统
```

---

## 八、模块分类汇总

| 目录 | 功能 | 复杂度 |
|------|------|--------|
| **ink/** | CLI React 框架 (50+ 文件) | 高 |
| **components/** | React UI 组件 (144 文件) | 高 |
| **buddy/** | 队友模式 | 中 |
| **coordinator/** | 协调者模式 | 中 |
| **screens/** | 屏幕组件 (3 个) | 低 |
| **voice/** | 语音模式 | 低 |
| **assistant/** | 会话历史 | 低 |
| **context/** | Context Providers | 低 |
| **plugins/** | 插件系统 | 低 |

---

## 九、已分析模块总结

| 文档 | 覆盖内容 |
|------|----------|
| 01 | 整体架构 |
| 02 | 核心模块 (QueryEngine, Task, Tool) |
| 03 | Bridge 模块 |
| 04 | CLI 和命令 |
| 05 | Hooks (90+) 和 Services (50+) |
| 06 | 工具实现 (45 个) |
| 07 | 工具函数 (329 个) |
| 08 | 常量定义 |
| 09 | 启动流程 |
| 10 | 技能系统 (15+ 内置) |
| 11 | React 组件 (144 个) |
| 12 | Context 和 State |
| 13 | 其他模块 (Ink, Buddy, Coordinator) |

---

*文档版本: 1.0*
*分析时间: 2026-04-11*