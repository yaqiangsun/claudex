"""Remote Permission Bridge."""
from typing import Any


class RemotePermissionBridge:
    """Bridge for remote permission requests."""

    def __init__(self):
        self.pending_requests: dict[str, Any] = {}

    def request_permission(self, request: dict) -> str:
        """Request permission from remote."""
        request_id = request.get('request_id', '')
        self.pending_requests[request_id] = request
        return request_id

    def cancel_permission(self, request_id: str) -> None:
        """Cancel a pending permission request."""
        if request_id in self.pending_requests:
            del self.pending_requests[request_id]

    def get_pending_request(self, request_id: str) -> dict | None:
        """Get a pending request by ID."""
        return self.pending_requests.get(request_id)


__all__ = ['RemotePermissionBridge']