"""Error IDs for tracking and debugging."""

# Error categories
ERROR_AUTH = "auth_error"
ERROR_API = "api_error"
ERROR_NETWORK = "network_error"
ERROR_TOOL = "tool_error"
ERROR_INTERNAL = "internal_error"

# Specific error IDs
ERROR_INVALID_API_KEY = "invalid_api_key"
ERROR_RATE_LIMITED = "rate_limited"
ERROR_TIMEOUT = "timeout"
ERROR_FILE_NOT_FOUND = "file_not_found"
ERROR_PERMISSION_DENIED = "permission_denied"


ERROR_MESSAGES = {
    ERROR_INVALID_API_KEY: "Invalid API key",
    ERROR_RATE_LIMITED: "Rate limit exceeded",
    ERROR_TIMEOUT: "Request timed out",
    ERROR_FILE_NOT_FOUND: "File not found",
    ERROR_PERMISSION_DENIED: "Permission denied",
}


__all__ = [
    'ERROR_AUTH',
    'ERROR_API',
    'ERROR_NETWORK',
    'ERROR_TOOL',
    'ERROR_INTERNAL',
    'ERROR_INVALID_API_KEY',
    'ERROR_RATE_LIMITED',
    'ERROR_TIMEOUT',
    'ERROR_FILE_NOT_FOUND',
    'ERROR_PERMISSION_DENIED',
    'ERROR_MESSAGES',
]