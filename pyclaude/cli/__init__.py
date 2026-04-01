"""
CLI module - handles console output, structured I/O, and transports.
"""

from .print import print, println, print_error, print_warning, print_success
from .structured_io import StructuredIO, create_structured_io
from .transports import (
    Transport,
    WebSocketTransport,
    SSETransport,
    HybridTransport,
    SerialBatchEventUploader,
    WorkerStateUploader,
)

__all__ = [
    'print',
    'println',
    'print_error',
    'print_warning',
    'print_success',
    'StructuredIO',
    'create_structured_io',
    'Transport',
    'WebSocketTransport',
    'SSETransport',
    'HybridTransport',
    'SerialBatchEventUploader',
    'WorkerStateUploader',
]