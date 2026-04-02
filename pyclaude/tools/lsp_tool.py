"""LSP tool."""
from typing import Any, Dict

class LSPTool:
    name = "lsp"
    description = "LSP tool"

    async def execute(self, params: Dict[str, Any]) -> Any:
        return {"status": "ok"}

__all__ = ['LSPTool']