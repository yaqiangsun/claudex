# 11 - 输入系统

对应 TypeScript: `src/keybindings/` + `src/vim/` + `src/server/`

## 11.1 快捷键系统

```python
# pyclaude/cli/input/keybindings.py
from typing import Callable, Awaitable, Optional
from dataclasses import dataclass
from enum import Enum


class KeyModifier(str, Enum):
    """修饰键"""
    CTRL = "ctrl"
    ALT = "alt"
    SHIFT = "shift"
    META = "meta"


@dataclass
class KeyBinding:
    """快捷键绑定"""
    key: str
    modifiers: list[KeyModifier]
    action: str
    description: str


class KeyBindingManager:
    """快捷键管理器"""

    def __init__(self):
        self.bindings: dict[str, KeyBinding] = {}
        self._load_default_bindings()

    def register(self, binding: KeyBinding) -> None:
        """注册快捷键"""
        key = self._make_key(binding.key, binding.modifiers)
        self.bindings[key] = binding

    def get(self, key: str, modifiers: list[KeyModifier]) -> Optional[KeyBinding]:
        """获取快捷键"""
        k = self._make_key(key, modifiers)
        return self.bindings.get(k)

    def _make_key(self, key: str, modifiers: list[KeyModifier]) -> str:
        """生成快捷键标识"""
        parts = [m.value for m in sorted(modifiers, key=lambda m: m.value)]
        parts.append(key.lower())
        return "+".join(parts)

    def _load_default_bindings(self) -> None:
        """加载默认快捷键"""
        defaults = [
            KeyBinding("c", [KeyModifier.CTRL], "quit", "退出"),
            KeyBinding("l", [KeyModifier.CTRL], "clear", "清除屏幕"),
            KeyBinding("n", [KeyModifier.CTRL], "new_session", "新建会话"),
            KeyBinding("p", [KeyModifier.CTRL], "prev_command", "上一命令"),
            KeyBinding("a", [KeyModifier.CTRL], "beginning_of_line", "行首"),
            KeyBinding("e", [KeyModifier.CTRL], "end_of_line", "行尾"),
            KeyBinding("u", [KeyModifier.CTRL], "clear_line", "清除行"),
            KeyBinding("w", [KeyModifier.CTRL], "delete_word", "删除词"),
        ]
        for binding in defaults:
            self.register(binding)
```

## 11.2 Vim 模式

```python
# pyclaude/cli/input/vim.py
from enum import Enum
from typing import Optional


class VimMode(str, Enum):
    """Vim 模式"""
    NORMAL = "normal"
    INSERT = "insert"
    VISUAL = "visual"
    COMMAND = "command"


class VimEngine:
    """Vim 引擎"""

    def __init__(self):
        self.mode = VimMode.NORMAL
        self.register = '"'
        self.last_command: Optional[str] = None
        self.motion: Optional[str] = None
        self.count: Optional[int] = None

    def set_mode(self, mode: VimMode) -> None:
        """设置模式"""
        self.mode = mode

    def handle_key(self, key: str) -> str:
        """处理按键"""
        if self.mode == VimMode.NORMAL:
            return self._handle_normal(key)
        elif self.mode == VimMode.INSERT:
            return self._handle_insert(key)
        elif self.mode == VimMode.VISUAL:
            return self._handle_visual(key)
        elif self.mode == VimMode.COMMAND:
            return self._handle_command(key)
        return ""

    def _handle_normal(self, key: str) -> str:
        """普通模式处理"""
        # i - 进入插入模式
        if key == "i":
            self.set_mode(VimMode.INSERT)
            return ""
        # : - 进入命令模式
        elif key == ":":
            self.set_mode(VimMode.COMMAND)
            return ""
        # dd - 删除行
        elif key == "d" and self.last_command == "d":
            self.last_command = None
            return "delete_line"
        # yy - 复制行
        elif key == "y" and self.last_command == "y":
            self.last_command = None
            return "yank_line"
        # p - 粘贴
        elif key == "p":
            return "paste"
        # u - 撤销
        elif key == "u":
            return "undo"
        # Ctrl+r - 重做
        elif key == "r":
            return "redo"
        # w/b - 词前进/后退
        elif key in "wb":
            return f"word_{key}"
        # 0/$ - 行首/行尾
        elif key == "0":
            return "beginning_of_line"
        elif key == "$":
            return "end_of_line"
        # gg/G - 文件开头/结尾
        elif key == "g":
            return "file_beginning"
        # 数字 - 设置计数
        elif key.isdigit():
            self.count = int(key)
            return ""

        self.last_command = key
        return ""

    def _handle_insert(self, key: str) -> str:
        """插入模式处理"""
        if key == "\x1b":  # ESC
            self.set_mode(VimMode.NORMAL)
            return ""
        return key  # 直接返回字符

    def _handle_visual(self, key: str) -> str:
        """可视模式处理"""
        if key == "\x1b":
            self.set_mode(VimMode.NORMAL)
            return ""
        return ""

    def _handle_command(self, key: str) -> str:
        """命令模式处理"""
        if key == "\x1b":
            self.set_mode(VimMode.NORMAL)
            return ""
        elif key == "\n":
            self.set_mode(VimMode.NORMAL)
            return f"command:{self.last_command}"
        self.last_command = (self.last_command or "") + key
        return ""
```

## 11.3 本地服务器

```python
# pyclaude/cli/input/server.py
import asyncio
from typing import Callable, Awaitable
from dataclasses import dataclass
import socket
import threading


@dataclass
class ServerConfig:
    """服务器配置"""
    host: str = "127.0.0.1"
    port: int = 18901
    socket_path: Optional[str] = None


class InputServer:
    """输入服务器 - 允许外部应用直接输入"""

    def __init__(self, config: ServerConfig):
        self.config = config
        self.server = None
        self.handler: Callable[[str], Awaitable[None]] = None
        self._running = False

    async def start(self) -> None:
        """启动服务器"""
        self._running = True
        self.server = await asyncio.start_server(
            self._handle_client,
            self.config.host,
            self.config.port,
        )
        async with self.server:
            await self.server.serve_forever()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """处理客户端连接"""
        while self._running:
            try:
                data = await reader.readline()
                if not data:
                    break

                message = data.decode().strip()
                if message:
                    await self.handler(message)

            except Exception:
                break
        writer.close()

    def set_handler(self, handler: Callable[[str], Awaitable[None]]) -> None:
        """设置消息处理器"""
        self.handler = handler

    def stop(self) -> None:
        """停止服务器"""
        self._running = False
        if self.server:
            self.server.close()

    async def send_to_client(self, message: str) -> None:
        """发送消息给客户端"""
        # 实现发送逻辑
        pass
```

## 11.4 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `KeyBindingManager` | `class KeyBindingManager` | `pyclaude/cli/input/keybindings.py` |
| `KeyBinding` | `class KeyBinding` | `pyclaude/cli/input/keybindings.py` |
| `VimEngine` | `class VimEngine` | `pyclaude/cli/input/vim.py` |
| `VimMode` | `enum VimMode` | `pyclaude/cli/input/vim.py` |
| `InputServer` | `class InputServer` | `pyclaude/cli/input/server.py` |