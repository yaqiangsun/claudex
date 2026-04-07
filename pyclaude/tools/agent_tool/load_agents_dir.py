"""Load agents from directory matching src/tools/AgentTool/loadAgentsDir.ts"""
from typing import Dict, Any, List, Optional
import os
import importlib.util
import sys


def discover_agents_in_dir(agents_dir: str) -> List[Dict[str, Any]]:
    """Discover custom agents in a directory."""
    agents = []

    if not os.path.isdir(agents_dir):
        return agents

    for filename in os.listdir(agents_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            agent_path = os.path.join(agents_dir, filename)
            agent_name = filename[:-3]  # Remove .py extension

            try:
                spec = importlib.util.spec_from_file_location(agent_name, agent_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[agent_name] = module
                    spec.loader.exec_module(module)

                    # Look for agent definition
                    if hasattr(module, 'AGENT_CONFIG'):
                        agents.append({
                            "name": agent_name,
                            "config": module.AGENT_CONFIG,
                            "path": agent_path,
                        })
            except Exception as e:
                print(f"Failed to load agent {agent_name}: {e}")

    return agents


def load_custom_agents(config_dir: Optional[str] = None) -> Dict[str, Any]:
    """Load custom agents from config directory."""
    if config_dir is None:
        config_dir = os.path.expanduser("~/.config/pyclaude/agents")

    agents = discover_agents_in_dir(config_dir)
    return {agent["name"]: agent["config"] for agent in agents}


__all__ = ["discover_agents_in_dir", "load_custom_agents"]