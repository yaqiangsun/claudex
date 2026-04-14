# 01 - 总览与架构设计

## 1.1 项目目标

Claude Code Python 版本旨在完整复现 TypeScript 版本的核心功能，提供一个功能等价但使用 Python 实现的 AI 编程助手 CLI 工具。

**核心目标**：
- 完整的 AI 对话界面，支持工具执行
- 远程桥接支持（通过 claude.ai 网页控制）
- 技能系统（Skills）
- 100+ 命令支持
- 45+ 内置工具
- 高度可定制化

**可选目标**（降低优先级）：
- 完整的 React 组件库（使用 Python UI 框架替代）
- Ink 终端 UI（使用 prompt_toolkit 或 Textual 替代）

## 1.2 技术选型

### 核心依赖

| 类别 | 库 | 用途 |
|------|-----|------|
| AI SDK | `anthropic` | Claude API 交互 |
| 异步 | `asyncio` / `aiohttp` | 异步 IO、HTTP 请求 |
| CLI UI | `prompt_toolkit` 或 `Textual` | 终端 UI 框架 |
| 配置 | `toml` / `pydantic` | 配置管理 |
| 状态管理 | 自实现或 `pydantic` | 状态存储 |
| 日志 | `loguru` | 日志记录 |
| HTTP | `httpx` | HTTP 客户端 |
| WebSocket | `websockets` | WebSocket 支持 |
| SSE | `sse-starlette` | Server-Sent Events |

### 项目结构

```
pyclaude/
├── pyclaude/
│   ├── __init__.py
│   ├── __main__.py          # 入口点
│   ├── main.py              # 主程序
│   ├── engine.py            # QueryEngine
│   ├── core/
│   │   ├── __init__.py
│   │   ├── task.py          # Task 定义
│   │   ├── query.py         # 查询循环
│   │   ├── history.py       # 历史记录
│   │   └── context.py       # 上下文管理
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py          # Tool 基类/Protocol
│   │   ├── registry.py      # 工具注册表
│   │   ├── bash.py          # BashTool
│   │   ├── file.py          # 文件操作工具
│   │   └── ...              # 其他工具
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── registry.py      # 命令注册表
│   │   ├── commit.py        # commit 命令
│   │   ├── config.py        # config 命令
│   │   └── ...              # 其他命令
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── loader.py        # 技能加载器
│   │   ├── registry.py      # 技能注册表
│   │   └── builtin/         # 内置技能
│   ├── bridge/
│   │   ├── __init__.py
│   │   ├── client.py        # Bridge 客户端
│   │   ├── session.py       # 会话管理
│   │   └── transport/       # 传输层
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── app.py           # CLI 应用
│   │   ├── input.py         # 输入处理
│   │   ├── output.py        # 输出处理
│   │   └── transport/       # 传输层实现
│   ├── services/
│   │   ├── __init__.py
│   │   ├── api.py           # API 客户端
│   │   ├── mcp.py           # MCP 支持
│   │   ├── analytics.py     # 分析服务
│   │   └── compact.py       # 上下文压缩
│   ├── state/
│   │   ├── __init__.py
│   │   ├── store.py         # 状态存储
│   │   └── selectors.py     # 选择器
│   ├── hooks/               # 钩子系统
│   ├── utils/               # 工具函数
│   ├── constants/           # 常量定义
│   ├── types/               # 类型定义
│   └── config.py            # 配置管理
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

## 1.3 整体架构

### 分层架构

```
┌─────────────────────────────────────────┐
│           用户交互层                     │
│   CLI 输入 │ UI │ Bridge 远程控制        │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│           命令系统层                     │
│   命令注册 │ 100+ 命令实现               │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│           核心处理层                     │
│   QueryEngine │ Query 循环 │ Tool 系统  │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│            服务层                        │
│   API 客户端 │ MCP │ Analytics          │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│           状态管理层                      │
│   自定义 Store │ 状态选择器              │
└─────────────────────────────────────────┘
```

### 数据流

```
用户输入 → 命令解析 → QueryEngine
              ↓
         API 请求 → Claude API
              ↓
         工具执行 → Tool Registry
              ↓
         结果返回 → UI 输出
              ↓
         状态更新 → Store
```

### 核心模块依赖关系

```
main.py
  ├── setup.py (初始化)
  ├── cli/app.py (UI)
  │     ├── cli/input.py
  │     └── cli/output.py
  ├── engine.py
  │     ├── core/query.py
  │     ├── core/history.py
  │     ├── tools/registry.py
  │     ├── commands/registry.py
  │     └── state/store.py
  ├── bridge/client.py
  │     └── bridge/transport/
  ├── services/api.py
  └── services/mcp.py
```

## 1.4 设计原则

1. **功能等价**：优先完整实现核心功能，UI 层可简化
2. **接口稳定**：核心接口与 TypeScript 版本保持一致
3. **异步优先**：使用 asyncio 实现高性能并发
4. **类型安全**：使用 Pydantic 进行类型验证
5. **可扩展**：支持 MCP 协议、插件系统、技能系统
6. **配置驱动**：通过配置文件定制行为