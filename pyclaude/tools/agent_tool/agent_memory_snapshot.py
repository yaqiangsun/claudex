"""Agent memory snapshot matching src/tools/AgentTool/agentMemorySnapshot.ts"""
from typing import Dict, Any, Optional
import json
from datetime import datetime
from .agent_memory import AgentMemory


class AgentMemorySnapshot:
    """Creates and manages snapshots of agent memory."""

    @staticmethod
    def create_snapshot(memory: AgentMemory, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a snapshot of the current agent memory."""
        return {
            "agent_id": memory.agent_id,
            "timestamp": datetime.now().isoformat(),
            "entries": [
                {
                    "timestamp": entry.timestamp.isoformat(),
                    "content": entry.content,
                    "type": entry.type,
                }
                for entry in memory.entries
            ],
            "context": memory.context,
            "metadata": metadata or {},
        }

    @staticmethod
    def save_snapshot(snapshot: Dict[str, Any], path: str) -> None:
        """Save snapshot to a file."""
        with open(path, 'w') as f:
            json.dump(snapshot, f, indent=2)

    @staticmethod
    def load_snapshot(path: str) -> Dict[str, Any]:
        """Load snapshot from a file."""
        with open(path, 'r') as f:
            return json.load(f)

    @staticmethod
    def restore_memory(snapshot: Dict[str, Any]) -> AgentMemory:
        """Restore agent memory from a snapshot."""
        memory = AgentMemory(snapshot["agent_id"])
        for entry in snapshot.get("entries", []):
            memory.add_entry(entry["content"], entry["type"])
        memory.context = snapshot.get("context", {})
        return memory


__all__ = ["AgentMemorySnapshot"]