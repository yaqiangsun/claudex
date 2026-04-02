"""Remote Session Manager."""
from typing import Any, Callable

# Type aliases
RemoteMessageContent = dict[str, Any]
GetAccessToken = Callable[[], str]


class RemotePermissionResponse:
    """Permission response for remote sessions."""

    def __init__(
        self,
        behavior: str,
        updated_input: dict | None = None,
        message: str | None = None,
    ):
        self.behavior = behavior
        self.updated_input = updated_input
        self.message = message

    def to_dict(self) -> dict:
        if self.behavior == 'allow':
            return {'behavior': 'allow', 'updatedInput': self.updated_input}
        return {'behavior': 'deny', 'message': self.message}


class RemoteSessionConfig:
    """Configuration for remote session."""

    def __init__(
        self,
        session_id: str,
        get_access_token: GetAccessToken,
        org_uuid: str,
        has_initial_prompt: bool = False,
        viewer_only: bool = False,
    ):
        self.session_id = session_id
        self.get_access_token = get_access_token
        self.org_uuid = org_uuid
        self.has_initial_prompt = has_initial_prompt
        self.viewer_only = viewer_only


class RemoteSessionCallbacks:
    """Callbacks for remote session events."""

    def __init__(
        self,
        on_message: Callable[[dict], None],
        on_permission_request: Callable[[dict, str], None],
        on_connected: Callable[[], None] | None = None,
        on_disconnected: Callable[[], None] | None = None,
        on_reconnecting: Callable[[], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
        on_permission_cancelled: Callable[[str, str | None], None] | None = None,
    ):
        self.on_message = on_message
        self.on_permission_request = on_permission_request
        self.on_connected = on_connected
        self.on_disconnected = on_disconnected
        self.on_reconnecting = on_reconnecting
        self.on_error = on_error
        self.on_permission_cancelled = on_permission_cancelled


class RemoteSessionManager:
    """Manages a remote CCR session."""

    def __init__(self, config: RemoteSessionConfig, callbacks: RemoteSessionCallbacks):
        self.config = config
        self.callbacks = callbacks
        self.websocket = None
        self.pending_permission_requests: dict[str, dict] = {}

    def connect(self) -> None:
        """Connect to the remote session via WebSocket."""
        from .sessions_websocket import SessionsWebSocket

        ws_callbacks = {
            'on_message': self._handle_message,
            'on_connected': lambda: self.callbacks.on_connected and self.callbacks.on_connected(),
            'on_close': lambda: self.callbacks.on_disconnected and self.callbacks.on_disconnected(),
            'on_reconnecting': lambda: self.callbacks.on_reconnecting and self.callbacks.on_reconnecting(),
            'on_error': lambda e: self.callbacks.on_error and self.callbacks.on_error(e),
        }

        self.websocket = SessionsWebSocket(
            self.config.session_id,
            self.config.org_uuid,
            self.config.get_access_token,
            ws_callbacks,
        )
        self.websocket.connect()

    def _handle_message(self, message: dict) -> None:
        """Handle messages from WebSocket."""
        msg_type = message.get('type')

        if msg_type == 'control_request':
            self._handle_control_request(message)
            return

        if msg_type == 'control_cancel_request':
            request_id = message.get('request_id')
            if request_id in self.pending_permission_requests:
                pending = self.pending_permission_requests[request_id]
                if self.callbacks.on_permission_cancelled:
                    self.callbacks.on_permission_cancelled(
                        request_id, pending.get('tool_use_id')
                    )
                del self.pending_permission_requests[request_id]
            return

        if msg_type == 'control_response':
            # Handle acknowledgment
            return

        # Forward SDK messages
        if msg_type != 'control_request' and msg_type != 'control_response':
            self.callbacks.on_message(message)

    def _handle_control_request(self, request: dict) -> None:
        """Handle control requests from CCR."""
        request_id = request.get('request_id')
        inner = request.get('request', {})

        if inner.get('subtype') == 'can_use_tool':
            self.pending_permission_requests[request_id] = inner
            self.callbacks.on_permission_request(inner, request_id)
        else:
            # Send error response for unsupported subtypes
            response = {
                'type': 'control_response',
                'response': {
                    'subtype': 'error',
                    'request_id': request_id,
                    'error': f"Unsupported control request subtype: {inner.get('subtype')}",
                },
            }
            if self.websocket:
                self.websocket.send_control_response(response)

    async def send_message(
        self, content: RemoteMessageContent, uuid: str | None = None
    ) -> bool:
        """Send a user message to the remote session."""
        from ..utils.teleport.api import send_event_to_remote_session

        success = await send_event_to_remote_session(
            self.config.session_id, content, uuid
        )
        return success

    def respond_to_permission_request(
        self, request_id: str, result: RemotePermissionResponse
    ) -> None:
        """Respond to a permission request from CCR."""
        if request_id not in self.pending_permission_requests:
            return

        del self.pending_permission_requests[request_id]

        response = {
            'type': 'control_response',
            'response': {
                'subtype': 'success',
                'request_id': request_id,
                'response': {
                    'behavior': result.behavior,
                    **(
                        {'updatedInput': result.updated_input}
                        if result.behavior == 'allow'
                        else {'message': result.message}
                    ),
                },
            },
        }

        if self.websocket:
            self.websocket.send_control_response(response)

    def is_connected(self) -> bool:
        """Check if connected."""
        return self.websocket and self.websocket.is_connected()

    def cancel_session(self) -> None:
        """Send interrupt signal to cancel current request."""
        if self.websocket:
            self.websocket.send_control_request({'subtype': 'interrupt'})

    def get_session_id(self) -> str:
        """Get the session ID."""
        return self.config.session_id

    def disconnect(self) -> None:
        """Disconnect from the remote session."""
        if self.websocket:
            self.websocket.close()
            self.websocket = None
        self.pending_permission_requests.clear()

    def reconnect(self) -> None:
        """Force reconnect the WebSocket."""
        if self.websocket:
            self.websocket.reconnect()


def create_remote_session_config(
    session_id: str,
    get_access_token: GetAccessToken,
    org_uuid: str,
    has_initial_prompt: bool = False,
    viewer_only: bool = False,
) -> RemoteSessionConfig:
    """Create a remote session config from OAuth tokens."""
    return RemoteSessionConfig(
        session_id=session_id,
        get_access_token=get_access_token,
        org_uuid=org_uuid,
        has_initial_prompt=has_initial_prompt,
        viewer_only=viewer_only,
    )


__all__ = [
    'RemoteSessionManager',
    'RemotePermissionResponse',
    'RemoteSessionConfig',
    'RemoteSessionCallbacks',
    'create_remote_session_config',
]