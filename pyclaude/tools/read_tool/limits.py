"""Limits for FileReadTool matching src/tools/FileReadTool/limits.ts"""

# Default limits
DEFAULT_MAX_LINES = 1000
DEFAULT_MAX_CHARS = 100000
DEFAULT_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Image processing limits
MAX_IMAGE_WIDTH = 4096
MAX_IMAGE_HEIGHT = 4096
IMAGE_QUALITY = 85


__all__ = [
    "DEFAULT_MAX_LINES",
    "DEFAULT_MAX_CHARS",
    "DEFAULT_MAX_FILE_SIZE",
    "MAX_IMAGE_WIDTH",
    "MAX_IMAGE_HEIGHT",
    "IMAGE_QUALITY",
]