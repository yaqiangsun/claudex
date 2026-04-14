# 10 - CLI 界面

对应 TypeScript: `src/ink/` + React 组件 - 使用 Python UI 框架替代

## 10.1 技术选型

TypeScript 版本使用 Ink (React) 实现 CLI UI，Python 版本可选方案：

| 方案 | 优点 | 缺点 |
|------|------|------|
| `prompt_toolkit` | 成熟稳定，跨平台 | 功能有限 |
| `Textual` | 现代，类 CSS，动画好 | 较新 |
| `rich` | 美观，简单 | 交互有限 |
| `urwid` | 功能强大 | API 较老 |

**推荐**: `Textual` - 现代 CLI 框架，支持复杂 UI

## 10.2 CLI 应用主框架

```python
# pyclaude/cli/app.py
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Header, Footer, Button, Input, Static
from textual.binding import Binding

from pyclaude.engine import QueryEngine
from pyclaude.state.store import Store


class ClaudeApp(App):
    """Claude Code CLI 应用"""

    CSS = """
    Screen {
        background: $surface;
    }
    #chat {
        height: 100%;
        padding: 1;
    }
    .message {
        width: 100%;
        padding: 0 1;
    }
    .user-message {
        text-style: bold;
        color: $accent;
    }
    .assistant-message {
        color: $text;
    }
    #input-area {
        dock: bottom;
        height: 3;
    }
    #command-input {
        width: 100%;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True),
        Binding("ctrl+l", "clear", "Clear", show=True),
        Binding("ctrl+n", "new_session", "New Session", show=True),
    ]

    def __init__(self, engine: QueryEngine, store: Store):
        super().__init__()
        self.engine = engine
        self.store = store

    def compose(self) -> ComposeResult:
        """构建 UI"""
        yield Header()
        with Container(id="chat"):
            yield Static("Claude Code Python", id="welcome")
        with Container(id="input-area"):
            yield Input(placeholder="Type your message...", id="command-input")
        yield Footer()

    async def on_mount(self) -> None:
        """挂载时设置"""
        input_widget = self.query_one("#command-input", Input)
        input_widget.focus()

    async def on_input_submit(self, event: Input.Submit) -> None:
        """处理输入提交"""
        message = event.value
        if not message:
            return

        # 显示用户消息
        chat = self.query_one("#chat", Container)
        await chat.mount(Static(f"> {message}", classes="message user-message"))

        # 执行查询
        async for chunk in self.engine.query(message):
            # 显示响应
            await chat.mount(Static(chunk.get("text", ""), classes="message assistant-message"))

        # 清空输入
        event.input.value = ""

    def action_clear(self) -> None:
        """清除屏幕"""
        chat = self.query_one("#chat", Container)
        chat.remove_children()

    def action_new_session(self) -> None:
        """新建会话"""
        import asyncio
        asyncio.create_task(self.engine.reset_session())
        self.action_clear()

    def action_quit(self) -> None:
        """退出"""
        self.exit()
```

## 10.3 消息显示组件

```python
# pyclaude/cli/components/message.py
from textual.widget import Widget
from textual.widgets import Static


class MessageWidget(Widget):
    """消息显示组件"""

    def __init__(self, role: str, content: str):
        super().__init__()
        self.role = role
        self.content = content

    def compose(self):
        prefix = "> " if self.role == "user" else ""
        classes = "user-message" if self.role == "user" else "assistant-message"
        yield Static(f"{prefix}{self.content}", classes=classes)
```

## 10.4 工具结果显示

```python
# pyclaude/cli/components/tool_result.py
from textual.widgets import Static


class ToolResultWidget(Static):
    """工具结果组件"""

    def __init__(self, tool_name: str, result: dict):
        super().__init__()
        self.tool_name = tool_name
        self.result = result

    def render(self):
        success = self.result.get("success", False)
        status = "✓" if success else "✗"
        return f"[Tool: {self.tool_name}] {status}\n{self.result}"
```

## 10.5 进度显示

```python
# pyclaude/cli/components/progress.py
from textual.widgets import ProgressBar, Static


class ProgressWidget(Static):
    """进度显示组件"""

    def __init__(self, description: str = "Processing..."):
        super().__init__()
        self.description = description

    def compose(self):
        yield Static(self.description)
        yield ProgressBar(total=100)
```

## 10.6 提示补全

```python
# pyclaude/cli/completion.py
from prompt_toolkit.completion import Completer, Completion
from pyclaude.commands.registry import CommandRegistry
from pyclaude.skills.registry import SkillRegistry
from pyclaude.tools.registry import ToolRegistry


class ClaudeCompleter(Completer):
    """命令/技能/工具补全器"""

    def __init__(
        self,
        command_registry: CommandRegistry,
        skill_registry: SkillRegistry,
        tool_registry: ToolRegistry,
    ):
        self.command_registry = command_registry
        self.skill_registry = skill_registry
        self.tool_registry = tool_registry

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        # 命令补全
        if text.startswith("/"):
            for cmd in self.command_registry.list_commands():
                if cmd.name.startswith(text[1:]):
                    yield Completion(
                        f"/{cmd.name}",
                        start_position=-len(text) + 1,
                        display=f"{cmd.name} - {cmd.description}",
                    )

        # 技能补全
        if text.startswith("!"):
            for skill in self.skill_registry.list_skills():
                if skill.name.startswith(text[1:]):
                    yield Completion(
                        f"!{skill.name}",
                        start_position=-len(text) + 1,
                        display=f"{skill.name} - {skill.description}",
                    )

        # 工具补全
        for tool in self.tool_registry.get_visible_tools():
            if tool.name.startswith(text):
                yield Completion(
                    tool.name,
                    display=f"{tool.name} - {tool.description}",
                )
```

## 10.7 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `App` | `class ClaudeApp(App)` | `pyclaude/cli/app.py` |
| `MessageWidget` | `class MessageWidget` | `pyclaude/cli/components/message.py` |
| `ToolResultWidget` | `class ToolResultWidget` | `pyclaude/cli/components/tool_result.py` |
| `ProgressWidget` | `class ProgressWidget` | `pyclaude/cli/components/progress.py` |
| `ClaudeCompleter` | `class ClaudeCompleter` | `pyclaude/cli/completion.py` |