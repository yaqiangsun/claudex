"""Assistant module - session history management and assistant context."""

import uuid
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

# Use requests instead of axios for HTTP calls
try:
    import requests
except ImportError:
    requests = None

from pyclaude.pyclaude.py_types.ids import SessionId

HISTORY_PAGE_SIZE = 100


@dataclass
class AssistantMessage:
    """A message in the conversation."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: str = 'user'
    content: str = ''
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HistoryPage:
    """Chronological order within the page."""
    events: List[Any] = field(default_factory=list)
    """Oldest event ID in this page - before_id cursor for next-older page."""
    first_id: Optional[str] = None
    """True = older events exist."""
    has_more: bool = False


@dataclass
class HistoryAuthCtx:
    """Authentication context for history requests."""
    base_url: str
    headers: Dict[str, str]


@dataclass
class SessionEventsResponse:
    """Response from session events API."""
    data: List[Any] = field(default_factory=list)
    has_more: bool = False
    first_id: Optional[str] = None
    last_id: Optional[str] = None


class SessionHistory:
    """Manages conversation history for a session."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.messages: List[AssistantMessage] = []
        self.created_at = datetime.now().timestamp()
        self.last_active = self.created_at

    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None) -> AssistantMessage:
        """Add a message to history."""
        msg = AssistantMessage(
            role=role,
            content=content,
            metadata=metadata or {},
        )
        self.messages.append(msg)
        self.last_active = datetime.now().timestamp()
        return msg

    def add_user_message(self, content: str) -> AssistantMessage:
        """Add a user message."""
        return self.add_message('user', content)

    def add_assistant_message(self, content: str, metadata: Optional[Dict] = None) -> AssistantMessage:
        """Add an assistant message."""
        return self.add_message('assistant', content, metadata)

    def add_system_message(self, content: str) -> AssistantMessage:
        """Add a system message."""
        return self.add_message('system', content)

    def get_messages(self) -> List[AssistantMessage]:
        """Get all messages."""
        return list(self.messages)

    def get_message_count(self) -> int:
        """Get the number of messages."""
        return len(self.messages)

    def clear(self) -> None:
        """Clear all messages."""
        self.messages.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'session_id': self.session_id,
            'messages': [
                {
                    'id': m.id,
                    'role': m.role,
                    'content': m.content,
                    'timestamp': m.timestamp,
                    'metadata': m.metadata,
                }
                for m in self.messages
            ],
            'created_at': self.created_at,
            'last_active': self.last_active,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionHistory':
        """Create from dictionary."""
        history = cls(session_id=data.get('session_id'))
        history.messages = [
            AssistantMessage(
                id=m['id'],
                role=m['role'],
                content=m['content'],
                timestamp=m['timestamp'],
                metadata=m.get('metadata', {}),
            )
            for m in data.get('messages', [])
        ]
        history.created_at = data.get('created_at', history.created_at)
        history.last_active = data.get('last_active', history.last_active)
        return history


# Placeholder for OAuth config - will be injected from parent module
_oauth_config: Optional[Dict[str, Any]] = None


def _get_oauth_config() -> Dict[str, Any]:
    """Get OAuth configuration."""
    global _oauth_config
    if _oauth_config is None:
        # Default config - actual implementation should set this
        _oauth_config = {'BASE_API_URL': 'https://api.anthropic.com'}
    return _oauth_config


def set_oauth_config(config: Dict[str, Any]) -> None:
    """Set OAuth configuration from external source."""
    global _oauth_config
    _oauth_config = config


# Placeholder for API request preparation - will be injected
_prepare_api_request: Optional[callable] = None


def set_prepare_api_request(func: callable) -> None:
    """Set the function to prepare API requests."""
    global _prepare_api_request
    _prepare_api_request = func


def _get_oauth_headers(access_token: str) -> Dict[str, str]:
    """Get OAuth headers."""
    return {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }


async def create_history_auth_ctx(session_id: str) -> HistoryAuthCtx:
    """Prepare auth + headers + base URL once, reuse across pages."""
    global _prepare_api_request

    if _prepare_api_request:
        result = await _prepare_api_request()
        access_token = result.get('accessToken')
        org_uuid = result.get('orgUUID')
    else:
        # Default placeholder values
        access_token = ''
        org_uuid = ''

    base_url = f"{_get_oauth_config()['BASE_API_URL']}/v1/sessions/{session_id}/events"
    headers = {
        **_get_oauth_headers(access_token),
        'anthropic-beta': 'ccr-byoc-2025-07-29',
        'x-organization-uuid': org_uuid,
    }
    return HistoryAuthCtx(base_url=base_url, headers=headers)


async def _fetch_page(
    ctx: HistoryAuthCtx,
    params: Dict[str, Union[str, int, bool]],
    label: str,
) -> Optional[HistoryPage]:
    """Fetch a page of session events."""
    if requests is None:
        raise RuntimeError("requests library is required for HTTP calls")

    try:
        resp = requests.get(
            ctx.base_url,
            headers=ctx.headers,
            params=params,
            timeout=15,
        )
    except Exception:
        resp = None

    if resp is None or resp.status_code != 200:
        # Log for debugging
        print(f"[{label}] HTTP {resp.status_code if resp else 'error'}")
        return None

    data = resp.json() if resp.status_code == 200 else {}
    return HistoryPage(
        events=data.get('data', []) if isinstance(data.get('data'), list) else [],
        first_id=data.get('first_id'),
        has_more=data.get('has_more', False),
    )


async def fetch_latest_events(
    ctx: HistoryAuthCtx,
    limit: int = HISTORY_PAGE_SIZE,
) -> Optional[HistoryPage]:
    """
    Newest page: last `limit` events, chronological, via anchor_to_latest.
    has_more=True means older events exist.
    """
    return await _fetch_page(ctx, {'limit': limit, 'anchor_to_latest': True}, 'fetch_latest_events')


async def fetch_older_events(
    ctx: HistoryAuthCtx,
    before_id: str,
    limit: int = HISTORY_PAGE_SIZE,
) -> Optional[HistoryPage]:
    """Older page: events immediately before `before_id` cursor."""
    return await _fetch_page(ctx, {'limit': limit, 'before_id': before_id}, 'fetch_older_events')


# Global session history
_session_history: Optional[SessionHistory] = None


def get_session_history() -> SessionHistory:
    """Get the global session history."""
    global _session_history
    if _session_history is None:
        _session_history = SessionHistory()
    return _session_history


def set_session_history(history: SessionHistory) -> None:
    """Set the global session history."""
    global _session_history
    _session_history = history


__all__ = [
    'HISTORY_PAGE_SIZE',
    'AssistantMessage',
    'SessionHistory',
    'HistoryPage',
    'HistoryAuthCtx',
    'create_history_auth_ctx',
    'fetch_latest_events',
    'fetch_older_events',
    'set_oauth_config',
    'set_prepare_api_request',
    'get_session_history',
    'set_session_history',
]