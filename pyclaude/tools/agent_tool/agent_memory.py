"""Agent memory matching src/tools/AgentTool/agentMemory.ts"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentMemoryEntry:
    """A single memory entry."""
    timestamp: datetime
    content: str
    type: str = "info"  # info, action, result, error


class AgentMemory:
    """Stores agent conversation history and context."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.entries: List[AgentMemoryEntry] = []
        self.context: Dict[str, Any] = {}

    def add_entry(self, content: str, entry_type: str = "info") -> None:
        """Add a memory entry."""
        entry = AgentMemoryEntry(
            timestamp=datetime.now(),
            content=content,
            type=entry_type,
        )
        self.entries.append(entry)

    def get_history(self, limit: Optional[int] = None) -> List[AgentMemoryEntry]:
        """Get conversation history."""
        if limit:
            return self.entries[-limit:]
        return self.entries

    def set_context(self, key: str, value: Any) -> None:
        """Set context value."""
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get context value."""
        return self.context.get(key, default)

    def clear(self) -> None:
        """Clear all memory."""
        self.entries.clear()
        self.context.clear()


__all__ = ["AgentMemory", "AgentMemoryEntry"]