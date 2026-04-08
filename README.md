# claudex

Python implementation of Claude Code - an AI programming assistant.

## Overview

claudex is a Python port of Claude Code, aiming to replicate the architecture and functionality of the original TypeScript project.

## Features

- **Core Query Engine** - Multi-turn conversation and tool calling support
- **Command System** - 100+ built-in commands (commit, init, status, etc.)
- **Bridge Remote Control** - Remote session control support
- **Multiple Transport Protocols** - WebSocket, SSE, Hybrid transport support
- **REPL Interactive Mode** - Interactive command-line interface
- **Tool System** - 40+ built-in tools (glob, grep, edit, write, etc.)
- **Hooks System** - 80+ hooks for extensibility
- **MCP Integration** - Model Context Protocol support
- **Plugin System** - Plugin support
- **Services** - Analytics, LSP, and other services

## Architecture

```
claudex/
├── __init__.py              # Package entry
├── __main__.py              # CLI entry
├── cli_main.py              # CLI main program
├── main.py                  # Main entry point
├── bootstrap/               # Initialization module
├── bridge/                  # Remote control module
│   ├── bridge_main.py       # Bridge main controller
│   ├── repl_bridge.py       # REPL Bridge implementation
│   ├── session.py           # Session management
│   └── types.py             # Type definitions
├── cli/                     # CLI module
│   ├── print.py             # Terminal output
│   ├── structured_io.py     # Structured I/O
│   └── transports/          # Transport layer
│       ├── transport.py     # Base transport
│       ├── websocket.py     # WebSocket
│       ├── sse.py           # SSE
│       └── hybrid.py        # Hybrid
├── commands/                # Command system (100+ commands)
│   ├── commit.py
│   ├── init.py
│   ├── version.py
│   ├── compact/             # Compact command
│   ├── resume/              # Resume command
│   ├── status/              # Status command
│   ├── btw/                 # BTW command
│   └── ...                  # Many more commands
├── commands.py              # Command system base
├── py_types/                # Type definitions
├── query_engine.py          # Query engine
├── query_impl.py            # Query implementation
├── services/                # Services
│   ├── mcp/                 # MCP integration
│   ├── lsp/                 # LSP support
│   ├── plugins/             # Plugin system
│   └── analytics/           # Analytics
├── state/                   # State management
├── tools/                   # Built-in tools (40+)
│   ├── glob_tool.py
│   ├── grep_tool.py
│   ├── edit_tool.py
│   └── write_tool.py
├── hooks/                   # Hooks system (80+ hooks)
├── utils/                   # Utility functions
│   ├── model/               # Model configuration
│   └── thinking.py          # Thinking configuration
├── task.py                  # Task definition
├── tool.py                  # Tool definition
├── context.py               # Context management
├── coordinator/             # Coordinator
├── buddy/                   # Buddy system
├── components/              # UI components
├── constants/               # Constants
├── entrypoints/             # Entry points
├── keybindings/             # Key bindings
├── screens/                 # Screen definitions
├── server/                  # Server module
└── types/                   # Type definitions
```

## Installation

```bash
# Clone the project
git clone https://github.com/anthropics/claude-code.git
cd claude-code/claudex

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e .
```

## Usage

### CLI Mode

```bash
# View help
python -m claudex --help

# Execute single query
python -m claudex "Write a hello world program"

# Specify model
python -m claudex -m claude-opus-4-20250501 "Your question"

# Verbose output
python -m claudex -v "Your question"

# Max turns limit
python -m claudex -n 5 "Your question"
```

### REPL Interactive Mode

```bash
python -m claudex --repl
```

### Programmatic Usage

```python
import asyncio
from claudex import QueryEngine, QueryEngineConfig
from claudex.tool import Tool

# Create a tool
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

# Run query
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

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `CLAUDE_MODEL` | Default model | claude-sonnet-4-20250514 |
| `CLAUDE_THINKING` | Thinking mode (true/false/disabled) | adaptive |
| `CLAUDE_DISABLE_PERSISTENCE` | Disable session persistence | false |

## Supported Models

- claude-opus-4-20250501
- claude-sonnet-4-20250514
- claude-haiku-4-20250307
- claude-3-5-sonnet-20240620

## Development

### Run Tests

```bash
pytest
```

### Code Style

```bash
# Lint
ruff check .

# Auto-fix
ruff check --fix .
```

## Comparison with Original

| Feature | TypeScript Original | Python Version |
|---------|---------------------|----------------|
| Core Engine | ✅ | ✅ |
| Command System | ✅ | ✅ (100+ commands) |
| Bridge | ✅ | ✅ |
| Transport Layer | ✅ | ✅ |
| REPL | ✅ | ✅ |
| Tool System | ✅ | ✅ (40+ tools) |
| Hooks System | ✅ | ✅ (80+ hooks) |
| MCP Integration | ✅ | ✅ |
| Plugin System | ✅ | ✅ |
| Services | ✅ | ✅ |
| UI Components | React/Ink | textual (in progress) |

## License

MIT License - Same as original Claude Code

## References

- [Claude Code Official Repository](https://github.com/anthropics/claude-code)
- [Anthropic API Documentation](https://docs.anthropic.com)