"""Constants for EditTool matching src/tools/FileEditTool/constants.ts"""

# Edit tool name
TOOL_NAME = "Edit"

# Edit types
EDIT_TYPE_REPLACE = "replace"
EDIT_TYPE_INSERT = "insert"
EDIT_TYPE_DELETE = "delete"

# Validation
MAX_EDIT_SIZE = 1000000  # 1MB


__all__ = ["TOOL_NAME", "EDIT_TYPE_REPLACE", "EDIT_TYPE_INSERT", "EDIT_TYPE_DELETE", "MAX_EDIT_SIZE"]