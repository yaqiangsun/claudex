"""Agent color manager matching src/tools/AgentTool/agentColorManager.ts"""
from typing import Dict
import hashlib


class AgentColorManager:
    """Manages colors for different agents."""

    COLORS = [
        "#FF6B6B",  # Red
        "#4ECDC4",  # Teal
        "#45B7D1",  # Blue
        "#96CEB4",  # Green
        "#FFEAA7",  # Yellow
        "#DDA0DD",  # Plum
        "#98D8C8",  # Mint
        "#F7DC6F",  # Gold
    ]

    _color_cache: Dict[str, str] = {}

    @classmethod
    def get_color(cls, agent_id: str) -> str:
        """Get a color for an agent based on its ID."""
        if agent_id in cls._color_cache:
            return cls._color_cache[agent_id]

        # Generate a consistent color based on agent_id
        hash_val = int(hashlib.md5(agent_id.encode()).hexdigest(), 16)
        color = cls.COLORS[hash_val % len(cls.COLORS)]
        cls._color_cache[agent_id] = color
        return color

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the color cache."""
        cls._color_cache.clear()


__all__ = ["AgentColorManager"]