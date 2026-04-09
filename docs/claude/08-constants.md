# 常量定义分析

本文档详细分析 Claude Code 的 constants 目录中的常量定义。

---

## 一、constants 目录概览

### 1.1 文件列表

```
src/constants/
├── apiLimits.ts            # Anthropic API 限制
├── betas.ts                # Beta 功能开关
├── common.ts               # 通用常量
├── cyberRiskInstruction.ts # 网络风险指令
├── errorIds.ts             # 错误 ID
├── figures.ts              # 字符图形
├── files.ts                # 文件相关常量
├── github-app.ts           # GitHub App 配置
├── keys.ts                 # 键盘快捷键
├── messages.ts             # 消息常量
├── oauth.ts                # OAuth 配置
├── outputStyles.ts         # 输出样式
├── product.ts              # 产品信息
├── prompts.ts              # 系统提示词 (54KB)
├── spinnerVerbs.ts         # Spinner 动词
├── system.ts               # 系统常量
├── systemPromptSections.ts # 系统提示 sections
├── toolLimits.ts           # 工具限制
├── tools.ts                # 工具列表
├── turnCompletionVerbs.ts  # 轮次完成动词
└── xml.ts                  # XML 相关
```

---

## 二、核心常量详解

### 2.1 API 限制 (apiLimits.ts)

```typescript
// =============================================================================
// IMAGE LIMITS
// =============================================================================

// API 强制执行的最大 base64 编码图片大小
export const API_IMAGE_MAX_BASE64_SIZE = 5 * 1024 * 1024 // 5 MB

// 编码前的目标原始图片大小 (base64 增加 33%)
export const IMAGE_TARGET_RAW_SIZE = (API_IMAGE_MAX_BASE64_SIZE * 3) / 4 // 3.75 MB

// 客户端最大图片尺寸
export const IMAGE_MAX_WIDTH = 2000
export const IMAGE_MAX_HEIGHT = 2000

// =============================================================================
// PDF LIMITS
// =============================================================================

// PDF 原始文件大小限制
export const PDF_TARGET_RAW_SIZE = 20 * 1024 * 1024 // 20 MB

// API 接受的最大 PDF 页数
export const API_PDF_MAX_PAGES = 100

// PDF 提取阈值 (3MB 以上使用提取)
export const PDF_EXTRACT_SIZE_THRESHOLD = 3 * 1024 * 1024 // 3 MB
export const PDF_MAX_EXTRACT_SIZE = 100 * 1024 * 1024 // 100 MB

// 每次读取最大页数
export const PDF_MAX_PAGES_PER_READ = 20

// @ 提及内联阈值
export const PDF_AT_MENTION_INLINE_THRESHOLD = 10

// =============================================================================
// MEDIA LIMITS
// =============================================================================

// 每请求最大媒体项目数
export const API_MAX_MEDIA_PER_REQUEST = 100
```

---

### 2.2 工具限制 (toolLimits.ts)

```typescript
// 工具结果默认最大字符数
export const DEFAULT_MAX_RESULT_SIZE_CHARS = 50_000

// 工具结果最大 token 数
export const MAX_TOOL_RESULT_TOKENS = 100_000

// 每 token 字节数估算
export const BYTES_PER_TOKEN = 4

// 工具结果最大字节数
export const MAX_TOOL_RESULT_BYTES = MAX_TOOL_RESULT_TOKENS * BYTES_PER_TOKEN

// 每条消息最大工具结果字符数
export const MAX_TOOL_RESULTS_PER_MESSAGE_CHARS = 200_000

// 工具摘要最大长度
export const TOOL_SUMMARY_MAX_LENGTH = 50
```

---

### 2.3 工具列表 (tools.ts)

```typescript
// Agent 禁止使用的工具
export const ALL_AGENT_DISALLOWED_TOOLS = new Set([
  TASK_OUTPUT_TOOL_NAME,
  EXIT_PLAN_MODE_V2_TOOL_NAME,
  ENTER_PLAN_MODE_TOOL_NAME,
  AGENT_TOOL_NAME,  // 除非是 ant 用户
  ASK_USER_QUESTION_TOOL_NAME,
  TASK_STOP_TOOL_NAME,
  WORKFLOW_TOOL_NAME,  // 如果启用
])

// 自定义 Agent 禁止的工具
export const CUSTOM_AGENT_DISALLOWED_TOOLS = new Set([
  ...ALL_AGENT_DISALLOWED_TOOLS,
])

// 异步 Agent 允许的工具
export const ASYNC_AGENT_ALLOWED_TOOLS = new Set([
  FILE_READ_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
  TODO_WRITE_TOOL_NAME,
  GREP_TOOL_NAME,
  WEB_FETCH_TOOL_NAME,
  GLOB_TOOL_NAME,
  ...SHELL_TOOL_NAMES,
  FILE_EDIT_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
  NOTEBOOK_EDIT_TOOL_NAME,
  SKILL_TOOL_NAME,
  SYNTHETIC_OUTPUT_TOOL_NAME,
  TOOL_SEARCH_TOOL_NAME,
  ENTER_WORKTREE_TOOL_NAME,
  EXIT_WORKTREE_TOOL_NAME,
])

// 进程内队友允许的工具
export const IN_PROCESS_TEAMMATE_ALLOWED_TOOLS = new Set([
  TASK_CREATE_TOOL_NAME,
  TASK_GET_TOOL_NAME,
  TASK_LIST_TOOL_NAME,
  TASK_UPDATE_TOOL_NAME,
  SEND_MESSAGE_TOOL_NAME,
  CRON_CREATE_TOOL_NAME,
  CRON_DELETE_TOOL_NAME,
  CRON_LIST_TOOL_NAME,
])

// 协调者模式允许的工具
export const COORDINATOR_MODE_ALLOWED_TOOLS = new Set([
  AGENT_TOOL_NAME,
  TASK_STOP_TOOL_NAME,
  SEND_MESSAGE_TOOL_NAME,
  SYNTHETIC_OUTPUT_TOOL_NAME,
])
```

---

### 2.4 Beta 功能 (betas.ts)

```typescript
// 典型结构
export const BETA_FEATURES = {
  MCP: 'mcp-2024-01',
  SWARM: 'swarm-2024-06',
  VOICE: 'voice-2024-12',
} as const
```

---

### 2.5 系统常量 (system.ts)

```typescript
// 应用信息
export const APP_NAME = 'Claude Code'
export const APP_VERSION = process.env.CLAUDE_CODE_VERSION ?? 'development'

// 默认超时
export const DEFAULT_TIMEOUT_MS = 120_000
export const MAX_TIMEOUT_MS = 600_000

// 路径
export const DEFAULT_CONFIG_DIR = '~/.claude'
export const DEFAULT_DATA_DIR = '~/.claude'
```

---

### 2.6 输出样式 (outputStyles.ts)

```typescript
// 典型的输出样式常量
export const STYLES = {
  SUCCESS: '\x1b[32m',   // 绿色
  ERROR: '\x1b[31m',     // 红色
  WARNING: '\x1b[33m',   // 黄色
  INFO: '\x1b[36m',      // 青色
  DIM: '\x1b[2m',        // 暗淡
  BOLD: '\x1b[1m',       // 粗体
  RESET: '\x1b[0m',      // 重置
} as const
```

---

### 2.7 键盘快捷键 (keys.ts)

```typescript
// 典型快捷键定义
export const KEY_BINDINGS = {
  CtrlC: '\x03',
  CtrlD: '\x04',
  CtrlZ: '\x1a',
  Escape: '\x1b',
  Enter: '\r',
  Tab: '\t',
} as const
```

---

### 2.8 OAuth 配置 (oauth.ts)

```typescript
// OAuth 相关常量
export const OAUTH_CONFIG = {
  AUTHORIZATION_URL: 'https://auth.anthropic.com/oauth/authorize',
  TOKEN_URL: 'https://auth.anthropic.com/oauth/token',
  REDIRECT_URI: 'http://localhost:8080/oauth/callback',
  SCOPES: ['api:read', 'api:write'],
}
```

---

### 2.9 系统提示词 (prompts.ts)

```typescript
// 54KB 的系统提示词文件
// 包含各种系统提示模板
// 例如:
// - 角色定义
// - 行为指南
// - 工具使用说明
// - 风格指南
```

---

## 三、Python 版本实现建议

### 3.1 常量组织

```python
# claudex/constants/__init__.py

# API 限制
API_IMAGE_MAX_BASE64_SIZE = 5 * 1024 * 1024  # 5 MB
IMAGE_TARGET_RAW_SIZE = API_IMAGE_MAX_BASE64_SIZE * 3 // 4
IMAGE_MAX_WIDTH = 2000
IMAGE_MAX_HEIGHT = 2000

PDF_TARGET_RAW_SIZE = 20 * 1024 * 1024  # 20 MB
API_PDF_MAX_PAGES = 100
PDF_MAX_PAGES_PER_READ = 20

API_MAX_MEDIA_PER_REQUEST = 100

# 工具限制
DEFAULT_MAX_RESULT_SIZE_CHARS = 50_000
MAX_TOOL_RESULT_TOKENS = 100_000
BYTES_PER_TOKEN = 4
MAX_TOOL_RESULTS_PER_MESSAGE_CHARS = 200_000
TOOL_SUMMARY_MAX_LENGTH = 50

# 系统
APP_NAME = "Claude Code"
DEFAULT_TIMEOUT_MS = 120_000
MAX_TIMEOUT_MS = 600_000
```

### 3.2 工具集合

```python
# claudex/constants/tools.py

# 工具名称常量
TOOL_NAMES = {
    "file_read": "Read",
    "file_write": "Write",
    "file_edit": "Edit",
    "bash": "Bash",
    "grep": "Grep",
    "glob": "Glob",
    # ...
}

# Agent 允许的工具
ASYNC_AGENT_ALLOWED_TOOLS = frozenset([
    TOOL_NAMES["file_read"],
    TOOL_NAMES["web_search"],
    # ...
])

# Agent 禁止的工具
ALL_AGENT_DISALLOWED_TOOLS = frozenset([
    "TaskOutput",
    "ExitPlanMode",
    "EnterPlanMode",
    # ...
])
```

---

## 四、常量分类汇总

| 类别 | 文件 | 说明 |
|------|------|------|
| **API 限制** | `apiLimits.ts` | 图像、PDF、媒体限制 |
| **工具限制** | `toolLimits.ts` | 工具结果大小限制 |
| **工具配置** | `tools.ts` | 允许/禁止工具列表 |
| **功能开关** | `betas.ts` | Beta 功能标志 |
| **系统** | `system.ts` | 应用信息、超时 |
| **认证** | `oauth.ts` | OAuth 配置 |
| **界面** | `outputStyles.ts`, `figures.ts` | 输出样式 |
| **快捷键** | `keys.ts` | 键盘绑定 |
| **提示词** | `prompts.ts` | 系统提示词模板 |

---

*文档版本: 1.0*
*分析时间: 2026-04-09*