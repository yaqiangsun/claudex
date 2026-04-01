"""
Utility modules.
"""

from .model.model import (
    get_main_loop_model,
    parse_user_specified_model,
    get_model_pricing,
    calculate_cost,
    DEFAULT_MODEL,
    ModelSetting,
)
from .thinking import (
    ThinkingConfig,
    should_enable_thinking_by_default,
    get_thinking_config,
)
from .array import intersperse, count, uniq
from .crypto import random_uuid
from .errors import (
    ClaudeError,
    MalformedCommandError,
    AbortError,
    is_abort_error,
    ConfigParseError,
)
from .cwd import (
    pwd,
    get_cwd,
    set_cwd_state,
    get_cwd_state,
    get_original_cwd,
    set_original_cwd,
    run_with_cwd_override,
)
from .env import (
    get_platform,
    is_darwin,
    is_linux,
    is_win32,
    get_home_dir,
    is_env_truthy,
)

__all__ = [
    # model
    'get_main_loop_model',
    'parse_user_specified_model',
    'get_model_pricing',
    'calculate_cost',
    'DEFAULT_MODEL',
    'ModelSetting',
    # thinking
    'ThinkingConfig',
    'should_enable_thinking_by_default',
    'get_thinking_config',
    # array
    'intersperse',
    'count',
    'uniq',
    # crypto
    'random_uuid',
    # errors
    'ClaudeError',
    'MalformedCommandError',
    'AbortError',
    'is_abort_error',
    'ConfigParseError',
    # cwd
    'pwd',
    'get_cwd',
    'set_cwd_state',
    'get_cwd_state',
    'get_original_cwd',
    'set_original_cwd',
    'run_with_cwd_override',
    # env
    'get_platform',
    'is_darwin',
    'is_linux',
    'is_win32',
    'get_home_dir',
    'is_env_truthy',
]