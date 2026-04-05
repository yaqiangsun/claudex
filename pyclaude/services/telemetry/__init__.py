"""Telemetry service - collect usage telemetry."""

import time
import uuid
from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """Telemetry event types."""
    SESSION_START = 'session_start'
    SESSION_END = 'session_end'
    API_CALL = 'api_call'
    TOOL_USE = 'tool_use'
    COMMAND = 'command'
    ERROR = 'error'


@dataclass
class TelemetryEvent:
    """A telemetry event."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: EventType = EventType.SESSION_START
    timestamp: float = field(default_factory=lambda: time.time())
    session_id: str = ''
    data: Dict[str, Any] = field(default_factory=dict)


class TelemetryService:
    """Service for collecting telemetry."""

    def __init__(self):
        self._events: List[TelemetryEvent] = []
        self._enabled = True
        self._session_id = str(uuid.uuid4())

    def set_session_id(self, session_id: str) -> None:
        """Set the current session ID."""
        self._session_id = session_id

    def is_enabled(self) -> bool:
        """Check if telemetry is enabled."""
        return self._enabled

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable telemetry."""
        self._enabled = enabled

    async def track_event(
        self,
        event_type: EventType,
        data: Optional[Dict[str, Any]] = None,
    ) -> TelemetryEvent:
        """Track a telemetry event."""
        if not self._enabled:
            return TelemetryEvent(type=event_type)

        event = TelemetryEvent(
            type=event_type,
            session_id=self._session_id,
            data=data or {},
        )

        self._events.append(event)
        return event

    async def track_session_start(self) -> TelemetryEvent:
        """Track session start."""
        return await self.track_event(EventType.SESSION_START, {
            'start_time': datetime.now().isoformat(),
        })

    async def track_session_end(self) -> TelemetryEvent:
        """Track session end."""
        return await self.track_event(EventType.SESSION_END, {
            'end_time': datetime.now().isoformat(),
            'event_count': len(self._events),
        })

    async def track_api_call(
        self,
        model: str,
        tokens: int,
        duration_ms: float,
        cost: float,
    ) -> TelemetryEvent:
        """Track an API call."""
        return await self.track_event(EventType.API_CALL, {
            'model': model,
            'tokens': tokens,
            'duration_ms': duration_ms,
            'cost': cost,
        })

    async def track_tool_use(
        self,
        tool_name: str,
        success: bool,
        duration_ms: float,
    ) -> TelemetryEvent:
        """Track tool use."""
        return await self.track_event(EventType.TOOL_USE, {
            'tool_name': tool_name,
            'success': success,
            'duration_ms': duration_ms,
        })

    async def track_command(
        self,
        command_name: str,
        args: str,
    ) -> TelemetryEvent:
        """Track command usage."""
        return await self.track_event(EventType.COMMAND, {
            'command': command_name,
            'args': args,
        })

    async def track_error(
        self,
        error_type: str,
        message: str,
    ) -> TelemetryEvent:
        """Track an error."""
        return await self.track_event(EventType.ERROR, {
            'error_type': error_type,
            'message': message,
        })

    def get_events(self) -> List[TelemetryEvent]:
        """Get all tracked events."""
        return list(self._events)

    def get_event_count(self) -> int:
        """Get the number of events."""
        return len(self._events)

    def clear(self) -> None:
        """Clear all events."""
        self._events.clear()


# Global telemetry service
_telemetry = TelemetryService()


def get_telemetry() -> TelemetryService:
    """Get the global telemetry service."""
    return _telemetry


__all__ = [
    'TelemetryService',
    'TelemetryEvent',
    'EventType',
    'get_telemetry',
]