"""Bash tool utilities matching src/tools/BashTool/utils.ts"""
import os
import subprocess
from typing import Dict, Any, Optional, List
import shlex


def run_command(
    command: str,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """Run a bash command and return result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd or os.getcwd(),
            env=env or os.environ.copy(),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": "Command timed out",
        }
    except Exception as e:
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
        }


def parse_command_args(command: str) -> List[str]:
    """Parse command string into arguments."""
    try:
        return shlex.split(command)
    except Exception:
        return command.split()


def get_working_directory() -> str:
    """Get current working directory."""
    return os.getcwd()


__all__ = ["run_command", "parse_command_args", "get_working_directory"]