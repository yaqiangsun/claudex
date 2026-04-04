"""Tests for bridge module."""
import pytest
from pyclaude.bridge.types import (
    BridgeState,
    BridgeEventType,
    BridgeMessage,
    BridgeEvent,
    BridgeConfig,
    get_bridge_status,
)


class TestBridgeState:
    """Test BridgeState enum."""

    def test_states_exist(self):
        """All expected states exist."""
        assert BridgeState.DISABLED == 'disabled'
        assert BridgeState.ENABLED == 'enabled'
        assert BridgeState.CONNECTING == 'connecting'
        assert BridgeState.CONNECTED == 'connected'
        assert BridgeState.RECONNECTING == 'reconnecting'
        assert BridgeState.ERROR == 'error'


class TestBridgeEventType:
    """Test BridgeEventType enum."""

    def test_event_types_exist(self):
        """All expected event types exist."""
        assert BridgeEventType.SESSION_START == 'session_start'
        assert BridgeEventType.SESSION_END == 'session_end'
        assert BridgeEventType.MESSAGE == 'message'
        assert BridgeEventType.TOOL_USE == 'tool_use'
        assert BridgeEventType.TOOL_RESULT == 'tool_result'


class TestBridgeMessage:
    """Test BridgeMessage class."""

    def test_message_creation(self):
        """BridgeMessage can be created."""
        msg = BridgeMessage(id="msg-1", type="user_message", payload={"content": "Hello"})
        assert msg.id == "msg-1"
        assert msg.type == "user_message"
        assert msg.timestamp > 0


class TestBridgeConfig:
    """Test BridgeConfig class."""

    def test_default_config(self):
        """Default config has expected values."""
        config = BridgeConfig()
        assert config.enabled is False
        assert config.reconnect is True
        assert config.reconnect_delay == 1.0


class TestGetBridgeStatus:
    """Test get_bridge_status function."""

    def test_connected_status(self):
        """Connected state returns correct status."""
        status = get_bridge_status(BridgeState.CONNECTED)
        assert status['is_connected'] is True
        assert status['state'] == 'connected'

    def test_connecting_status(self):
        """Connecting state returns correct status."""
        status = get_bridge_status(BridgeState.CONNECTING)
        assert status['is_connecting'] is True