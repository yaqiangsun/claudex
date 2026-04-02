"""
Telemetry attributes utility.
"""
import os
from typing import Dict, Any

def get_telemetry_attributes() -> Dict[str, Any]:
    return {
        'version': os.environ.get('CLAUDE_CODE_VERSION', 'unknown'),
        'platform': os.environ.get('CLAUDE_CODE_PLATFORM', 'unknown'),
    }

__all__ = ['get_telemetry_attributes']