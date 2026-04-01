"""
Deterministic Agent ID System.

This module provides helper functions for formatting and parsing deterministic
agent IDs used in the swarm/teammate system.

## ID Formats

**Agent IDs**: `agentName@teamName`
- Example: `team-lead@my-project`, `researcher@my-project`
- The @ symbol acts as a separator between agent name and team name

**Request IDs**: `{requestType}-{timestamp}@{agentId}`
- Example: `shutdown-1702500000000@researcher@my-project`
- Used for shutdown requests, plan approvals, etc.
"""

import time
from typing import Optional, Tuple, Dict


def format_agent_id(agent_name: str, team_name: str) -> str:
    """Format an agent ID in the format `agentName@teamName`."""
    return f"{agent_name}@{team_name}"


def parse_agent_id(agent_id: str) -> Optional[Dict[str, str]]:
    """Parse an agent ID into its components.

    Returns None if the ID doesn't contain the @ separator.
    """
    at_index = agent_id.find("@")
    if at_index == -1:
        return None
    return {
        "agent_name": agent_id[:at_index],
        "team_name": agent_id[at_index + 1:],
    }


def generate_request_id(request_type: str, agent_id: str) -> str:
    """Format a request ID in the format `{requestType}-{timestamp}@{agentId}`."""
    timestamp = int(time.time() * 1000)
    return f"{request_type}-{timestamp}@{agent_id}"


def parse_request_id(request_id: str) -> Optional[Dict[str, any]]:
    """Parse a request ID into its components.

    Returns None if the request ID doesn't match the expected format.
    """
    at_index = request_id.find("@")
    if at_index == -1:
        return None

    prefix = request_id[:at_index]
    agent_id = request_id[at_index + 1:]

    last_dash_index = prefix.rfind("-")
    if last_dash_index == -1:
        return None

    request_type = prefix[:last_dash_index]
    timestamp_str = prefix[last_dash_index + 1:]

    try:
        timestamp = int(timestamp_str)
    except ValueError:
        return None

    return {
        "request_type": request_type,
        "timestamp": timestamp,
        "agent_id": agent_id,
    }


__all__ = [
    "format_agent_id",
    "parse_agent_id",
    "generate_request_id",
    "parse_request_id",
]