# 12 - 状态管理

对应 TypeScript: `src/state/` - 自定义 Store + Hooks

## 12.1 状态存储

```python
# pyclaude/state/store.py
from typing import TypeVar, Generic, Callable, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path


T = TypeVar("T")


@dataclass
class StateChange:
    """状态变化"""
    key: str
    old_value: Any
    new_value: Any
    timestamp: datetime = field(default_factory=datetime.now)


class Store(Generic[T]):
    """轻量级状态存储 - 观察者模式"""

    def __init__(self, initial_state: Optional[T] = None):
        self._state: T = initial_state
        self._observers: dict[str, list[Callable[[StateChange], None]]] = {}
        self._history: list[StateChange] = []

    @property
    def state(self) -> T:
        """获取当前状态"""
        return self._state

    def set_state(self, new_state: T) -> None:
        """设置状态"""
        old_state = self._state
        self._state = new_state

        # 记录变化
        change = StateChange(
            key="root",
            old_value=old_state,
            new_value=new_state,
        )
        self._history.append(change)

        # 通知观察者
        self._notify_observers(change)

    def update(self, key: str, value: Any) -> None:
        """更新指定键的值"""
        if hasattr(self._state, key):
            old_value = getattr(self._state, key)
            setattr(self._state, key, value)

            change = StateChange(
                key=key,
                old_value=old_value,
                new_value=value,
            )
            self._history.append(change)
            self._notify_observers(change)

    def subscribe(self, key: str, callback: Callable[[StateChange], None]) -> None:
        """订阅状态变化"""
        if key not in self._observers:
            self._observers[key] = []
        self._observers[key].append(callback)

    def unsubscribe(self, key: str, callback: Callable[[StateChange], None]) -> None:
        """取消订阅"""
        if key in self._observers:
            self._observers[key].remove(callback)

    def _notify_observers(self, change: StateChange) -> None:
        """通知观察者"""
        # 通知特定键的观察者
        if change.key in self._observers:
            for callback in self._observers[change.key]:
                callback(change)

        # 通知全局观察者
        if "root" in self._observers:
            for callback in self._observers["root"]:
                callback(change)

    def get_history(self) -> list[StateChange]:
        """获取历史变化"""
        return self._history.copy()

    def persist(self, path: Path) -> None:
        """持久化状态"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self._state, f, default=str)

    def load(self, path: Path) -> None:
        """加载状态"""
        if path.exists():
            with open(path, "r") as f:
                self._state = json.load(f)
```

## 12.2 应用状态定义

```python
# pyclaude/state/app_state.py
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class SessionInfo:
    """会话信息"""
    session_id: str
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    message_count: int = 0


@dataclass
class UserSettings:
    """用户设置"""
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 1.0
    max_tokens: int = 8192
    vim_mode: bool = False
    auto_save: bool = True


@dataclass
class AppState:
    """应用状态"""
    current_session: Optional[SessionInfo] = None
    sessions: list[SessionInfo] = field(default_factory=list)
    settings: UserSettings = field(default_factory=UserSettings)
    connected: bool = False
    bridge_mode: str = "local"


# 全局状态存储
app_store: Store[AppState] = Store(AppState())
```

## 12.3 选择器

```python
# pyclaude/state/selectors.py
from pyclaude.state.store import Store
from pyclaude.state.app_state import AppState, SessionInfo, UserSettings


def select_current_session(store: Store[AppState]) -> SessionInfo | None:
    """选择当前会话"""
    return store.state.current_session


def select_sessions(store: Store[AppState]) -> list[SessionInfo]:
    """选择所有会话"""
    return store.state.sessions


def select_settings(store: Store[AppState]) -> UserSettings:
    """选择设置"""
    return store.state.settings


def select_connected(store: Store[AppState]) -> bool:
    """选择连接状态"""
    return store.state.connected


def select_bridge_mode(store: Store[AppState]) -> str:
    """选择桥接模式"""
    return store.state.bridge_mode
```

## 12.4 状态管理钩子

对应 TypeScript: `src/hooks/` - 90+ 钩子

```python
# pyclaude/hooks/use_app_state.py
from typing import Callable, Any
from pyclaude.state.store import Store, StateChange
from pyclaude.state.app_state import AppState


class UseAppState:
    """应用状态钩子"""

    def __init__(self, store: Store[AppState]):
        self.store = store

    def get_state(self) -> AppState:
        """获取状态"""
        return self.store.state

    def subscribe(self, key: str, callback: Callable[[StateChange], None]) -> None:
        """订阅状态变化"""
        self.store.subscribe(key, callback)

    def unsubscribe(self, key: str, callback: Callable[[StateChange], None]) -> None:
        """取消订阅"""
        self.store.unsubscribe(key, callback)

    def update(self, key: str, value: Any) -> None:
        """更新状态"""
        self.store.update(key, value)


# 常用钩子工厂
def create_use_selector(store: Store, selector: Callable) -> Callable:
    """创建选择器钩子"""
    def use_selector() -> Any:
        return selector(store)
    return use_selector
```

## 12.5 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `Store<T>` | `class Store(Generic[T])` | `pyclaude/state/store.py` |
| `StateChange` | `class StateChange` | `pyclaude/state/store.py` |
| `AppState` | `@dataclass AppState` | `pyclaude/state/app_state.py` |
| 选择器 | `select_*` 函数 | `pyclaude/state/selectors.py` |
| `UseAppState` | `class UseAppState` | `pyclaude/hooks/use_app_state.py` |