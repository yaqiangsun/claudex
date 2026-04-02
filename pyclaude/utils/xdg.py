"""
XDG Base Directory utilities.

Python adaptation.
"""

import os
from typing import Dict, Optional
from pathlib import Path


def _resolve_options(
    env: Optional[Dict[str, str]] = None,
    homedir: Optional[str] = None,
) -> Dict[str, str]:
    """Resolve options with defaults."""
    return {
        "env": env or dict(os.environ),
        "home": homedir or os.environ.get("HOME") or str(Path.home()),
    }


def get_xdg_state_home(
    env: Optional[Dict[str, str]] = None,
    homedir: Optional[str] = None,
) -> str:
    """Get XDG state home directory.

    Default: ~/.local/state
    """
    options = _resolve_options(env, homedir)
    return options["env"].get("XDG_STATE_HOME") or os.path.join(
        options["home"], ".local", "state"
    )


def get_xdg_cache_home(
    env: Optional[Dict[str, str]] = None,
    homedir: Optional[str] = None,
) -> str:
    """Get XDG cache home directory.

    Default: ~/.cache
    """
    options = _resolve_options(env, homedir)
    return options["env"].get("XDG_CACHE_HOME") or os.path.join(
        options["home"], ".cache"
    )


def get_xdg_data_home(
    env: Optional[Dict[str, str]] = None,
    homedir: Optional[str] = None,
) -> str:
    """Get XDG data home directory.

    Default: ~/.local/share
    """
    options = _resolve_options(env, homedir)
    return options["env"].get("XDG_DATA_HOME") or os.path.join(
        options["home"], ".local", "share"
    )


def get_user_bin_dir(homedir: Optional[str] = None) -> str:
    """Get user bin directory.

    Default: ~/.local/bin
    """
    home = homedir or os.environ.get("HOME") or str(Path.home())
    return os.path.join(home, ".local", "bin")


__all__ = [
    "get_xdg_state_home",
    "get_xdg_cache_home",
    "get_xdg_data_home",
    "get_user_bin_dir",
]