"""
AppState - Central application state management.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class TaskStatus(str, Enum):
    """Task status values."""
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    KILLED = 'killed'


class CompletionBoundaryType(str, Enum):
    """Types of completion boundaries."""
    COMPLETE = 'complete'
    BASH = 'bash'
    EDIT = 'edit'
    DENIED_TOOL = 'denied_tool'


@dataclass
class CompletionBoundary:
    """Completion boundary information."""
    type: CompletionBoundaryType
    completed_at: int
    output_tokens: int = 0
    command: str = ''
    tool_name: str = ''
    file_path: str = ''
    detail: str = ''


@dataclass
class SpeculationState:
    """State for AI prediction/speculation."""
    status: str = 'idle'  # 'idle' or 'active'
    id: str = ''
    start_time: int = 0
    suggestion_length: int = 0
    tool_use_count: int = 0
    is_pipelined: bool = False


class FooterItem(str, Enum):
    """Footer pill items."""
    TASKS = 'tasks'
    TMUX = 'tmux'
    BAGEL = 'bagel'
    TEAMS = 'teams'
    BRIDGE = 'bridge'
    COMPANION = 'companion'


class ViewSelectionMode(str, Enum):
    """View selection mode."""
    NONE = 'none'
    SELECTING_AGENT = 'selecting-agent'
    VIEWING_AGENT = 'viewing-agent'


class ExpandedView(str, Enum):
    """Expanded view state."""
    NONE = 'none'
    TASKS = 'tasks'
    TEAMMATES = 'teammates'


class RemoteConnectionStatus(str, Enum):
    """Remote connection status."""
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    RECONNECTING = 'reconnecting'
    DISCONNECTED = 'disconnected'


# Simplified AppState - full version has many more fields
@dataclass
class AppState:
    """Central application state."""
    # Settings
    settings: dict[str, Any] = field(default_factory=dict)
    verbose: bool = False
    main_loop_model: str = ''
    main_loop_model_for_session: str = ''
    status_line_text: Optional[str] = None
    expanded_view: ExpandedView = ExpandedView.NONE
    is_brief_only: bool = False

    # Coordinator
    coordinator_task_index: int = 0
    view_selection_mode: ViewSelectionMode = ViewSelectionMode.NONE
    footer_selection: Optional[FooterItem] = None

    # Spinner
    spinner_tip: Optional[str] = None

    # Agent
    agent: Optional[str] = None

    # Kairos (Assistant mode)
    kairos_enabled: bool = False

    # Remote session
    remote_session_url: Optional[str] = None
    remote_connection_status: RemoteConnectionStatus = RemoteConnectionStatus.DISCONNECTED
    remote_background_task_count: int = 0

    # Bridge (Always-on remote control)
    repl_bridge_enabled: bool = False
    repl_bridge_explicit: bool = False
    repl_bridge_outbound_only: bool = False
    repl_bridge_connected: bool = False
    repl_bridge_session_active: bool = False
    repl_bridge_reconnecting: bool = False
    repl_bridge_connect_url: Optional[str] = None
    repl_bridge_session_url: Optional[str] = None
    repl_bridge_environment_id: Optional[str] = None
    repl_bridge_session_id: Optional[str] = None
    repl_bridge_error: Optional[str] = None
    repl_bridge_initial_name: Optional[str] = None
    show_remote_callout: bool = False

    # Tasks
    tasks: dict[str, Any] = field(default_factory=dict)

    # Agent name registry
    agent_name_registry: dict[str, str] = field(default_factory=dict)

    # Foregrounded task
    foregrounded_task_id: Optional[str] = None
    viewing_agent_task_id: Optional[str] = None

    # Companion
    companion_reaction: Optional[str] = None
    companion_pet_at: Optional[int] = None

    # MCP
    mcp: dict[str, Any] = field(default_factory=lambda: {
        'clients': [],
        'tools': [],
        'commands': [],
        'resources': {},
        'plugin_reconnect_key': 0,
    })

    # Plugins
    plugins: dict[str, Any] = field(default_factory=lambda: {
        'enabled': [],
        'disabled': [],
        'commands': [],
        'errors': [],
        'installation_status': {
            'marketplaces': [],
            'plugins': [],
        },
        'needs_refresh': False,
    })

    # Agent definitions
    agent_definitions: dict[str, Any] = field(default_factory=dict)

    # File history
    file_history: dict[str, Any] = field(default_factory=dict)

    # Attribution
    attribution: dict[str, Any] = field(default_factory=dict)

    # Todos
    todos: dict[str, Any] = field(default_factory=dict)

    # Remote agent suggestions
    remote_agent_task_suggestions: list[dict[str, str]] = field(default_factory=list)

    # Notifications
    notifications: dict[str, Any] = field(default_factory=lambda: {
        'current': None,
        'queue': [],
    })

    # Elicitation
    elicitation: dict[str, list] = field(default_factory=lambda: {'queue': []})

    # Thinking
    thinking_enabled: Optional[bool] = None
    prompt_suggestion_enabled: bool = False

    # Session hooks
    session_hooks: dict[str, Any] = field(default_factory=dict)

    # Tungsten (tmux capture)
    tungsten_active_session: Optional[dict[str, Any]] = None
    tungsten_last_captured_time: Optional[int] = None
    tungsten_last_command: Optional[dict[str, Any]] = None
    tungsten_panel_visible: Optional[bool] = None
    tungsten_panel_auto_hidden: Optional[bool] = None

    # Bagel (WebBrowser)
    bagel_active: Optional[bool] = None
    bagel_url: Optional[str] = None
    bagel_panel_visible: Optional[bool] = None

    # REPL context
    repl_context: Optional[dict[str, Any]] = None

    # Team context
    team_context: Optional[dict[str, Any]] = None

    # Standalone agent
    standalone_agent_context: Optional[dict[str, Any]] = None


# Global state instance
_app_state: AppState = AppState()


def get_app_state() -> AppState:
    """Get the global app state instance."""
    return _app_state


def set_app_state(state: AppState) -> None:
    """Set the global app state instance."""
    global _app_state
    _app_state = state


def update_app_state(updater: callable) -> None:
    """Update app state with a function."""
    global _app_state
    _app_state = updater(_app_state)