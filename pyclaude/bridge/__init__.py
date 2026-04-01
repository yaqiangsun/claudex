"""
Bridge module - Remote control/session management.
"""

from .bridge_main import BridgeMain, BridgeConfig
from .repl_bridge import REPLBridge, REPLBridgeConfig
from .session import Session, SessionManager
from .types import BridgeMessage, BridgeEvent, BridgeState

__all__ = [
    'BridgeMain',
    'BridgeConfig',
    'REPLBridge',
    'REPLBridgeConfig',
    'Session',
    'SessionManager',
    'BridgeMessage',
    'BridgeEvent',
    'BridgeState',
]