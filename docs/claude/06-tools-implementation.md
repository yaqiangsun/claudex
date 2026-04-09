# 内置工具实现分析

本文档详细分析 Claude Code 的内置工具实现系统。

---

## 一、tools 目录结构

### 1.1 工具分类

```
src/tools/
├── AgentTool/                 # Agent 工具 - 创建和管理子 Agent
├── AskUserQuestionTool/       # 用户问答工具
├── BashTool/                  # Bash 命令执行工具 ⭐
├── BriefTool/                 # 摘要工具
├── ConfigTool/                # 配置工具
├── EnterPlanModeTool/         # 进入计划模式工具
├── EnterWorktreeTool/         # 进入 worktree 工具
├── ExitPlanModeTool/          # 退出计划模式工具
├── ExitWorktreeTool/          # 退出 worktree 工具
├── FileEditTool/              # 文件编辑工具
├── FileReadTool/              # 文件读取工具 ⭐
├── FileWriteTool/             # 文件写入工具
├── GlobTool/                  # 文件匹配工具
├── GrepTool/                  # 文本搜索工具
├── LSPTool/                   # LSP 语言服务器工具
├── ListMcpResourcesTool/      # 列出 MCP 资源工具
├── MCPTool/                   # MCP 工具
├── McpAuthTool/               # MCP 认证工具
├── NotebookEditTool/          # Jupyter 笔记本编辑工具
├── PowerShellTool/            # PowerShell 工具
├── REPLTool/                  # REPL 工具
├── ReadMcpResourceTool/       # 读取 MCP 资源工具
├── RemoteTriggerTool/         # 远程触发工具
├── ScheduleCronTool/          # 定时任务工具
├── SendMessageTool/           # 发送消息工具
├── SkillTool/                 # 技能工具
├── SleepTool/                 # 睡眠工具
├── SyntheticOutputTool/       # 合成输出工具
├── TaskCreateTool/            # 创建任务工具
├── TaskGetTool/               # 获取任务工具
├── TaskListTool/              # 列出任务工具
├── TaskOutputTool/            # 任务输出工具
├── TaskStopTool/              # 停止任务工具
├── TaskUpdateTool/            # 更新任务工具
├── TeamCreateTool/            # 创建团队工具
├── TeamDeleteTool/            # 删除团队工具
├── TodoWriteTool/             # Todo 列表工具
├── ToolSearchTool/            # 工具搜索工具
├── WebFetchTool/              # Web 获取工具
├── WebSearchTool/             # Web 搜索工具
├── shared/                    # 共享工具函数
└── utils.ts                   # 工具辅助函数
```

### 1.2 工具数量统计

| 类别 | 数量 |
|------|------|
| 文件操作 | 5 (Read, Write, Edit, Glob, Grep) |
| 命令执行 | 2 (Bash, PowerShell) |
| Agent 管理 | 1 (AgentTool) |
| 任务管理 | 7 (Create, Get, List, Output, Stop, Update, Task) |
| Web 功能 | 2 (WebFetch, WebSearch) |
| 配置管理 | 1 (ConfigTool) |
| 其他 | 25+ |

---

## 二、工具构建模式

### 2.1 使用 buildTool 构建

所有内置工具都使用 `Tool.ts` 中的 `buildTool()` 函数构建：

```typescript
import { buildTool, type ToolDef } from '../../Tool.js'

export const BashTool = buildTool({
  name: 'bash',
  searchHint: 'execute shell commands',
  maxResultSizeChars: 30_000,
  strict: true,

  // 描述
  async description({ description }) {
    return description || 'Run shell command'
  },

  // Prompt
  async prompt() {
    return getSimplePrompt()
  },

  // 能力定义
  isConcurrencySafe(input) {
    return this.isReadOnly?.(input) ?? false
  },

  isReadOnly(input) {
    const result = checkReadOnlyConstraints(input)
    return result.behavior === 'allow'
  },

  toAutoClassifierInput(input) {
    return input.command
  },

  // 权限检查
  async preparePermissionMatcher({ command }) {
    // 配置权限匹配器
  },

  async checkPermissions(input, context) {
    return bashToolHasPermission(input)
  },

  // 输入 Schema
  inputSchema: z.object({
    command: z.string().describe('...'),
    // ...
  }),

  // 执行方法
  async call(args, context, canUseTool, parentMessage, onProgress) {
    // 执行逻辑
    return { content: [...] }
  },

  // 渲染方法
  renderToolUseMessage(input, options) {
    return <BashToolUseMessage ... />
  },

  renderToolResultMessage(content, progressMessages, options) {
    return <BashToolResultMessage ... />
  },
})
```

### 2.2 工具目录标准结构

每个工具通常包含以下文件：

```
ToolName/
├── ToolName.tsx         # 主工具实现 (buildTool)
├── prompt.ts            # 工具使用提示
├── constants.ts         # 常量定义
├── types.ts             # 类型定义
├── utils.ts             # 辅助函数
└── UI.tsx               # React 渲染组件 (可选)
```

---

## 三、核心工具详解

### 3.1 BashTool - Shell 命令执行

**文件**: `src/tools/BashTool/BashTool.tsx`

#### 主要功能
- 执行 shell 命令
- 支持管道和复合命令
- 后台任务管理
- 图像输出处理

#### 输入 Schema
```typescript
const InputSchema = z.object({
  command: z.string().describe('Shell command to execute'),
  description: z.string().optional().describe('Command description'),
  timeout: z.number().optional().describe('Timeout in milliseconds'),
  background: z.boolean().optional().describe('Run in background'),
})
```

#### 关键方法
```typescript
// 判断是否为只读命令
isReadOnly(input) {
  const result = checkReadOnlyConstraints(input)
  return result.behavior === 'allow'
}

// 判断是否为搜索/读取命令
isSearchOrReadCommand(input) {
  return isSearchOrReadBashCommand(input.command)
}

// 权限检查
async checkPermissions(input, context) {
  return bashToolHasPermission(input)
}

// 命令执行
async call(args, context, canUseTool, parentMessage, onProgress) {
  // 1. 权限检查
  // 2. 解析命令
  // 3. 执行命令
  // 4. 处理结果
}
```

#### 安全机制
- **命令验证**: 解析命令，检测危险操作
- **路径验证**: 防止路径遍历攻击
- **只读检测**: 检测是否为只读操作
- **权限检查**: 基于规则的权限系统

#### 子模块
| 文件 | 功能 |
|------|------|
| `bashPermissions.ts` | 权限规则 |
| `bashSecurity.ts` | 安全检查 |
| `commandSemantics.ts` | 命令语义分析 |
| `pathValidation.ts` | 路径验证 |
| `readOnlyValidation.ts` | 只读验证 |
| `sedValidation.ts` | sed 命令验证 |
| `destructiveCommandWarning.ts` | 破坏性命令警告 |

---

### 3.2 FileReadTool - 文件读取

**文件**: `src/tools/FileReadTool/FileReadTool.ts`

#### 主要功能
- 读取文件内容
- 支持图像处理
- 支持 PDF 读取
- 支持 Jupyter Notebook

#### 输入 Schema
```typescript
const InputSchema = z.object({
  file_path: z.string().describe('File path to read'),
  offset: z.number().optional().describe('Line offset'),
  limit: z.number().optional().describe('Line limit'),
  show_line_numbers: z.boolean().optional(),
  partial_mode: z.boolean().optional(),
})
```

#### 特殊处理
- **图像**: 检测图像格式，可能调整大小
- **PDF**: 提取文本，支持分页
- **Notebook**: 解析 Jupyter 格式
- **大文件**: 支持范围读取

#### 子模块
| 文件 | 功能 |
|------|------|
| `imageProcessor.ts` | 图像处理 |
| `limits.ts` | 读取限制 |
| `prompt.ts` | 使用提示 |

---

### 3.3 FileEditTool - 文件编辑

**文件**: `src/tools/FileEditTool/FileEditTool.ts`

#### 主要功能
- 原地编辑文件
- 支持正则表达式替换
- 创建文件

#### 输入 Schema
```typescript
const InputSchema = z.object({
  file_path: z.string(),
  operation: z.enum(['edit', 'insert', 'replace']),
  old_string: z.string().optional(),
  new_string: z.string().optional(),
  insert_at_line: z.number().optional(),
  replace_string: z.string().optional(),
})
```

---

### 3.4 FileWriteTool - 文件写入

**文件**: `src/tools/FileWriteTool/FileWriteTool.ts`

```typescript
const InputSchema = z.object({
  file_path: z.string(),
  content: z.string(),
  create_if_missing: z.boolean().optional(),
})
```

---

### 3.5 AgentTool - Agent 管理

**文件**: `src/tools/AgentTool/AgentTool.tsx`

#### 功能
- 创建子 Agent
- 管理 Agent 生命周期
- Agent 间通信

#### 内置 Agent
```
src/tools/AgentTool/built-in/
├── claudeCodeGuideAgent.ts   # Claude Code 指南
├── exploreAgent.ts           # 代码探索
├── generalPurposeAgent       # 通用 Agent
├── planAgent.ts              # 计划 Agent
├── statuslineSetup.ts        # 状态行设置
└── verificationAgent.ts      # 验证 Agent
```

---

### 3.6 任务工具集

| 工具 | 文件 | 功能 |
|------|------|------|
| TaskCreateTool | `TaskCreateTool.ts` | 创建后台任务 |
| TaskGetTool | `TaskGetTool.ts` | 获取任务状态 |
| TaskListTool | `TaskListTool.ts` | 列出任务 |
| TaskOutputTool | `TaskOutputTool.tsx` | 获取任务输出 |
| TaskStopTool | `TaskStopTool.ts` | 停止任务 |
| TaskUpdateTool | `TaskUpdateTool.ts` | 更新任务 |

---

### 3.7 Web 工具

#### WebFetchTool
```typescript
const InputSchema = z.object({
  url: z.string().url(),
  prompt: z.string().optional(),
})
```

#### WebSearchTool
```typescript
const InputSchema = z.object({
  query: z.string(),
  num_results: z.number().optional().default(10),
})
```

---

### 3.8 其他重要工具

| 工具 | 功能 |
|------|------|
| GlobTool | 文件路径匹配 |
| GrepTool | 文本搜索 |
| LSPTool | 语言服务器协议 |
| MCPTool | MCP 工具调用 |
| ConfigTool | 配置管理 |
| TodoWriteTool | Todo 列表管理 |
| SkillTool | 技能执行 |
| ScheduleCronTool | 定时任务 |

---

## 四、工具能力系统

### 4.1 能力接口

```typescript
// 并发安全
isConcurrencySafe(input): boolean

// 只读操作
isReadOnly(input): boolean

// 破坏性操作
isDestructive?(input): boolean

// 中断行为
interruptBehavior?(): 'cancel' | 'block'

// 搜索/读取命令
isSearchOrReadCommand?(input): { isSearch: boolean; isRead: boolean }

// 开放世界
isOpenWorld?(input): boolean

// 需要用户交互
requiresUserInteraction?(): boolean
```

### 4.2 权限检查

```typescript
async checkPermissions(
  input: Input,
  context: ToolUseContext
): Promise<PermissionResult> {
  return {
    behavior: 'allow' | 'deny' | 'ask',
    decisionReason?: { type: string; reason: string }
  }
}
```

---

## 五、工具渲染系统

### 5.1 渲染接口

```typescript
// 工具使用消息
renderToolUseMessage(input, options): React.ReactNode

// 工具结果消息
renderToolResultMessage(content, progressMessages, options): React.ReactNode

// 工具使用标签
renderToolUseTag(input): React.ReactNode

// 工具使用进度消息
renderToolUseProgressMessage(progressMessages, options): React.ReactNode

// 工具使用排队消息
renderToolUseQueuedMessage(): React.ReactNode

// 工具使用拒绝消息
renderToolUseRejectedMessage(input, options): React.ReactNode

// 工具使用错误消息
renderToolUseErrorMessage(result, options): React.ReactNode
```

### 5.2 渲染示例 (BashTool)

```typescript
// 渲染工具使用消息
renderToolUseMessage(input, options) {
  return (
    <BashToolUseMessage
      command={input.command}
      background={input.background}
      running={isRunning}
    />
  )
}

// 渲染工具结果
renderToolResultMessage(content, progressMessages, options) {
  return (
    <BashToolResultMessage
      result={content}
      showLineNumbers={options.showLineNumbers}
    />
  )
}
```

---

## 六、Python 版本实现建议

### 6.1 工具基类设计

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Generic, TypeVar, Protocol

InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
ProgressT = TypeVar('ProgressT')

@dataclass
class ToolResult(Generic[OutputT]):
    content: OutputT
    is_error: bool = False
    truncated: bool = False

class Tool(ABC, Generic[InputT, OutputT]):
    name: str
    description: str
    input_schema: dict

    @abstractmethod
    async def call(
        self,
        args: InputT,
        context: "ToolUseContext",
        can_use_tool: bool
    ) -> ToolResult[OutputT]:
        pass

    def is_read_only(self, input: InputT) -> bool:
        return False

    def is_concurrency_safe(self, input: InputT) -> bool:
        return False
```

### 6.2 工具注册表

```python
class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def all(self) -> list[Tool]:
        return list(self._tools.values())

# 全局注册表
TOOLS = ToolRegistry()

# 注册工具
TOOLS.register(BashTool())
TOOLS.register(FileReadTool())
TOOLS.register(FileWriteTool())
# ...
```

### 6.3 工具目录结构

```
claudex/tools/
├── __init__.py
├── base.py              # 工具基类和接口
├── registry.py          # 工具注册表
├── bash/
│   ├── __init__.py
│   ├── tool.py          # BashTool 实现
│   ├── permissions.py   # 权限检查
│   └── security.py      # 安全验证
├── file/
│   ├── __init__.py
│   ├── read.py          # FileReadTool
│   ├── write.py         # FileWriteTool
│   └── edit.py          # FileEditTool
├── search/
│   ├── __init__.py
│   ├── glob.py          # GlobTool
│   └── grep.py          # GrepTool
├── web/
│   ├── __init__.py
│   ├── fetch.py         # WebFetchTool
│   └── search.py        # WebSearchTool
├── task/
│   ├── __init__.py
│   ├── create.py
│   ├── stop.py
│   └── list.py
└── utils/
    ├── __init__.py
    └── rendering.py     # 渲染工具
```

---

## 七、关键实现要点

### 7.1 异步执行
- 使用 `async/await` 和异步生成器
- 支持进度回调 `onProgress`
- 支持取消操作

### 7.2 权限系统
- 基于规则的权限匹配
- 支持通配符模式
- 支持权限请求

### 7.3 结果处理
- 支持大结果存储到文件
- 支持截断显示
- 支持图像处理

### 7.4 错误处理
- 统一的错误类型
- 错误渲染接口
- 用户友好的错误消息

---

*文档版本: 1.0*
*分析时间: 2026-04-09*