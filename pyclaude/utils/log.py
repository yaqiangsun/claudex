"""
Log utility.
"""
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pyclaude')

def log(message: str, level: str = 'info') -> None:
    getattr(logger, level)(message)

def log_error(error: Any) -> None:
    logger.error(str(error))

__all__ = ['log', 'log_error', 'logger']