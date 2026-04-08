# claudex

Claude Code 的 Python 实现 - 一个 AI 编程助手。

## 概述

claudex 是类Claude Code 的 Python 版本，主要目的是还原原始 TypeScript 项目的架构和功能。

## 特性

- **核心查询引擎** - 支持多轮对话和工具调用
- **命令系统** - 100+ 内置命令 (commit, init, status 等)
- **Bridge 远程控制** - 支持远程会话控制
- **多种传输协议** - WebSocket、SSE、Hybrid 传输支持
- **REPL 交互模式** - 交互式命令行界面
- **工具系统** - 40+ 内置工具 (glob, grep, edit, write 等)
- **Hooks 系统** - 80+ 钩子用于扩展
- **MCP 集成** - Model Context Protocol 支持
- **插件系统** - 插件支持
- **服务** - 分析、LSP 等服务

## 架构

```
claudex/
├── __init__.py              # 包入口
├── __main__.py              # CLI 入口
├── cli_main.py              # CLI 主程序
├── main.py                  # 主入口
├── bootstrap/               # 初始化模块
├── bridge/                  # 远程控制模块
│   ├── bridge_main.py       # Bridge 主控制器
│   ├── repl_bridge.py       # REPL Bridge 实现
│   ├── session.py           # 会话管理
│   └── types.py             # 类型定义
├── cli/                     # CLI 模块
│   ├── print.py             # 终端输出
│   ├── structured_io.py     # 结构化 I/O
│   └── transports/          # 传输层
│       ├── transport.py     # 基础传输
│       ├── websocket.py     # WebSocket
│       ├── sse.py           # SSE
│       └── hybrid.py        # Hybrid
├── commands/                # 命令系统 (100+ 命令)
│   ├── commit.py
│   ├── init.py
│   ├── version.py
│   ├── compact/             # Compact 命令
│   ├── resume/              # Resume 命令
│   ├── status/              # Status 命令
│   ├── btw/                 # BTW 命令
│   └── ...                  # 更多命令
├── commands.py              # 命令系统基础
├── py_types/                # 类型定义
├── query_engine.py          # 查询引擎
├── query_impl.py            # 查询实现
├── services/                # 服务
│   ├── mcp/                 # MCP 集成
│   ├── lsp/                 # LSP 支持
│   ├── plugins/             # 插件系统
│   └── analytics/           # 分析服务
├── state/                   # 状态管理
├── tools/                   # 内置工具 (40+)
│   ├── glob_tool.py
│   ├── grep_tool.py
│   ├── edit_tool.py
│   └── write_tool.py
├── hooks/                   # Hooks 系统 (80+ 钩子)
├── utils/                   # 工具函数
│   ├── model/               # 模型配置
│   └── thinking.py          # 思考配置
├── task.py                  # 任务定义
├── tool.py                  # 工具定义
├── context.py               # 上下文管理
├── coordinator/             # 协调器
├── buddy/                   # Buddy 系统
├── components/              # UI 组件
├── constants/               # 常量
├── entrypoints/             # 入口点
├── keybindings/             # 键盘绑定
├── screens/                 # 屏幕定义
├── server/                  # 服务器模块
└── types/                   # 类型定义
```

## 安装

```bash
# 克隆项目
git clone https://github.com/anthropics/claude-code.git
cd claude-code/claudex

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -e .
```

## 使用

### CLI 模式

```bash
# 查看帮助
python -m claudex --help

# 执行单次查询
python -m claudex "帮我写一个 hello world 程序"

# 指定模型
python -m claudex -m claude-opus-4-20250501 "你的问题"

# 详细输出
python -m claudex -v "你的问题"

# 最大轮数限制
python -m claudex -n 5 "你的问题"
```

### REPL 交互模式

```bash
python -m claudex --repl
```

### 编程使用

```python
import asyncio
from claudex import QueryEngine, QueryEngineConfig
from claudex.tool import Tool

# 创建工具
class HelloTool(Tool):
    def __init__(self):
        super().__init__(
            name="hello",
            description="Say hello",
            input_schema={"type": "object", "properties": {"name": {"type": "string"}}}
        )

    async def execute(self, input_dict, get_app_state, set_app_state, abort_controller=None):
        name = input_dict.get("name", "World")
        return {"content": f"Hello, {name}!"}

# 运行查询
async def main():
    config = QueryEngineConfig(
        cwd="/path/to/project",
        tools=[HelloTool()],
        commands=[],
        mcp_clients=[],
        agents=[],
        can_use_tool=lambda *args: {"behavior": "allow"},
        get_app_state=lambda: {},
        set_app_state=lambda f: None,
    )

    engine = QueryEngine(config)

    async for message in engine.submit_message("Say hello to Alice"):
        print(message)

asyncio.run(main())
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ANTHROPIC_API_KEY` | Anthropic API 密钥 | - |
| `CLAUDE_MODEL` | 默认模型 | claude-sonnet-4-20250514 |
| `CLAUDE_THINKING` | 思考模式 (true/false/disabled) | adaptive |
| `CLAUDE_DISABLE_PERSISTENCE` | 禁用会话持久化 | false |

## 模型支持

- claude-opus-4-20250501
- claude-sonnet-4-20250514
- claude-haiku-4-20250307
- claude-3-5-sonnet-20240620

## 开发

### 运行测试

```bash
pytest
```

### 代码规范

```bash
# 检查代码
ruff check .

# 自动修复
ruff check --fix .
```

## 与原版对比

| 特性 | TypeScript 原版 | Python 版 |
|------|----------------|-----------|
| 核心引擎 | ✅ | ✅ |
| 命令系统 | ✅ | ✅ (100+ 命令) |
| Bridge | ✅ | ✅ |
| 传输层 | ✅ | ✅ |
| REPL | ✅ | ✅ |
| 工具系统 | ✅ | ✅ (40+ 工具) |
| Hooks 系统 | ✅ | ✅ (80+ 钩子) |
| MCP 集成 | ✅ | ✅ |
| 插件系统 | ✅ | ✅ |
| 服务 | ✅ | ✅ |
| UI 组件 | React/Ink | textual (进行中) |

## 许可证

MIT License - 与原版 Claude Code 相同

## 参考

- [Claude Code 官方仓库](https://github.com/anthropics/claude-code)
- [Anthropic API 文档](https://docs.anthropic.com)