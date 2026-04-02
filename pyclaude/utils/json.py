"""
JSON utility.
"""
import json
from typing import Any, Optional

def parse_json(text: str) -> Optional[Any]:
    try:
        return json.loads(text)
    except Exception:
        return None

def to_json(obj: Any, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(obj, indent=2)
    return json.dumps(obj)

__all__ = ['parse_json', 'to_json']