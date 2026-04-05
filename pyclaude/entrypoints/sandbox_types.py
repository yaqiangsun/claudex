"""Sandbox types for isolated execution."""
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class SandboxMode(str, Enum):
    """Sandbox execution modes."""
    DISABLED = "disabled"
    ENABLED = "enabled"
    READ_ONLY = "read_only"


@dataclass
class SandboxConfig:
    """Sandbox configuration."""
    mode: SandboxMode = SandboxMode.DISABLED
    timeout: int = 30
    memory_limit: Optional[int] = None


class Sandbox:
    """Sandbox for isolated code execution."""

    def __init__(self, config: Optional[SandboxConfig] = None):
        self.config = config or SandboxConfig()

    def execute(self, code: str) -> Any:
        """Execute code in sandbox."""
        return {"output": None, "error": None}

    def is_allowed(self, operation: str) -> bool:
        """Check if operation is allowed."""
        if self.config.mode == SandboxMode.DISABLED:
            return True
        return True


__all__ = ['SandboxMode', 'SandboxConfig', 'Sandbox']