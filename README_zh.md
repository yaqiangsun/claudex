# PyClaude

Claude Code 的 Python 实现 - 一个 AI 编程助手。

## 概述

PyClaude 是类Claude Code 的 Python 版本，主要目的是还原原始 TypeScript 项目的架构和功能。

## 特性

- **核心查询引擎** - 支持多轮对话和工具调用
- **命令系统** - 完整的命令注册和执行框架
- **Bridge 远程控制** - 支持远程会话控制
- **多种传输协议** - WebSocket、SSE、Hybrid 传输支持
- **REPL 交互模式** - 交互式命令行界面

## 架构

```
pyclaude/
├── __init__.py              # 包入口
├── __main__.py              # CLI 入口
├── cli_main.py              # CLI 主程序
├── bootstrap/               # 初始化模块
│   └── __init__.py
├── bridge/                  # 远程控制模块
│   ├── __init__.py
│   ├── bridge_main.py       # Bridge 主控制器
│   ├── repl_bridge.py       # REPL Bridge 实现
│   ├── session.py           # 会话管理
│   └── types.py             # 类型定义
├── cli/                     # CLI 模块
│   ├── __init__.py
│   ├── print.py             # 终端输出
│   ├── structured_io.py     # 结构化 I/O
│   └── transports/          # 传输层
│       ├── __init__.py
│       ├── transport.py     # 基础传输
│       ├── websocket.py     # WebSocket
│       ├── sse.py           # SSE
│       └── hybrid.py        # Hybrid
├── commands.py              # 命令系统
├── py_types/                # 类型定义
│   ├── __init__.py
│   └── ids.py               # ID 类型
├── query_engine.py          # 查询引擎
├── query.py                 # 查询实现
├── state/                   # 状态管理
│   └── __init__.py
├── task.py                  # 任务定义
├── tool.py                  # 工具定义
└── utils/                   # 工具函数
    ├── __init__.py
    ├── model/               # 模型配置
    │   └── model.py
    └── thinking.py          # 思考配置
```

## 安装

```bash
# 克隆项目
git clone https://github.com/anthropics/claude-code.git
cd claude-code/pyclaude

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
python -m pyclaude --help

# 执行单次查询
python -m pyclaude "帮我写一个 hello world 程序"

# 指定模型
python -m pyclaude -m claude-opus-4-20250501 "你的问题"

# 详细输出
python -m pyclaude -v "你的问题"

# 最大轮数限制
python -m pyclaude -n 5 "你的问题"
```

### REPL 交互模式

```bash
python -m pyclaude --repl
```

### 编程使用

```python
import asyncio
from pyclaude import QueryEngine, QueryEngineConfig
from pyclaude.tool import Tool

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
| 命令系统 | ✅ | ✅ |
| Bridge | ✅ | ✅ |
| 传输层 | ✅ | ✅ |
| REPL | ✅ | ✅ |
| MCP 集成 | ✅ | 规划中 |
| 完整工具集 | ✅ | 规划中 |
| UI 组件 | React/Ink | textual (规划中) |

## 许可证

MIT License - 与原版 Claude Code 相同

## 参考

- [Claude Code 官方仓库](https://github.com/anthropics/claude-code)
- [Anthropic API 文档](https://docs.anthropic.com)