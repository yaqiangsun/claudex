"""Brief tool."""
from typing import Any, Dict

class BriefTool:
    name = "brief"
    description = "Brief tool"

    async def execute(self, params: Dict[str, Any]) -> Any:
        return {"status": "ok"}

__all__ = ['BriefTool']