# 04 - 工具系统

对应 TypeScript: `src/tools/` 下 45+ 工具

## 4.1 工具注册表

```python
# pyclaude/tools/registry.py
from typing import Optional
from pyclaude.tools.base import BaseTool, ToolDefinition, ToolCapability


class ToolRegistry:
    """工具注册表"""

    def __init__(self):
        self.tools: dict[str, BaseTool] = {}
        self._load_builtin_tools()

    def register(self, tool: BaseTool) -> None:
        """注册工具"""
        definition = tool.get_definition()
        self.tools[definition.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        """获取工具"""
        return self.tools.get(name)

    def get_tool_definitions(self) -> list[ToolDefinition]:
        """获取所有工具定义"""
        return [tool.get_definition() for tool in self.tools.values()]

    def get_visible_tools(self) -> list[ToolDefinition]:
        """获取可见工具（排除隐藏工具）"""
        return [
            tool.get_definition()
            for tool in self.tools.values()
            if tool.get_definition().visible
        ]

    def get_tools_by_capability(self, capability: ToolCapability) -> list[BaseTool]:
        """根据能力获取工具"""
        return [
            tool for tool in self.tools.values()
            if tool.get_definition().capability & capability
        ]

    def _load_builtin_tools(self) -> None:
        """加载内置工具"""
        from pyclaude.tools import (
            BashTool,
            FileReadTool,
            FileEditTool,
            GlobTool,
            GrepTool,
            AgentTool,
            WebFetchTool,
            TaskTool,
        )
        for tool_class in [
            BashTool,
            FileReadTool,
            FileEditTool,
            GlobTool,
            GrepTool,
            AgentTool,
            WebFetchTool,
            TaskTool,
        ]:
            tool = tool_class()
            self.register(tool)
```

## 4.2 核心工具实现

### 4.2.1 BashTool

```python
# pyclaude/tools/bash.py
import asyncio
from typing import Any
from pyclaude.tools.base import BaseTool, ToolDefinition, ToolCapability, PermissionResult


class BashTool(BaseTool):
    """Bash 命令执行工具"""

    def __init__(self):
        self.definition = ToolDefinition(
            name="bash",
            description="Execute bash commands in the terminal",
            input_schema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The bash command to execute"
                    },
                    "description": {
                        "type": "string",
                        "description": "What this command does"
                    }
                },
                "required": ["command"]
            },
            capability=ToolCapability.DESTRUCTIVE | ToolCapability.CONCURRENT_SAFE,
            visible=True,
        )

    def get_definition(self) -> ToolDefinition:
        return self.definition

    async def check_permission(self, tool_input: dict[str, Any]) -> PermissionResult:
        """权限检查"""
        command = tool_input.get("command", "")
        dangerous_patterns = ["rm -rf", "dd if=", ":(){:|:&};:", "mkfs", "> /dev/sda"]
        for pattern in dangerous_patterns:
            if pattern in command:
                return PermissionResult(
                    allowed=False,
                    reason=f"Command contains dangerous pattern: {pattern}"
                )
        return PermissionResult(allowed=True)

    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """执行 Bash 命令"""
        command = tool_input.get("command", "")
        description = tool_input.get("description", "")

        try:
            result = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await result.communicate()

            return {
                "success": result.returncode == 0,
                "stdout": stdout.decode("utf-8"),
                "stderr": stderr.decode("utf-8"),
                "exit_code": result.returncode,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
```

### 4.2.2 FileReadTool

```python
# pyclaude/tools/file.py
from pathlib import Path
from typing import Any
from pyclaude.tools.base import BaseTool, ToolDefinition, ToolCapability, PermissionResult


class FileReadTool(BaseTool):
    """文件读取工具"""

    def __init__(self):
        self.definition = ToolDefinition(
            name="read",
            description="Read the contents of a file",
            input_schema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    },
                    "offset": {
                        "type": "number",
                        "description": "Line number to start reading from"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Number of lines to read"
                    }
                },
                "required": ["file_path"]
            },
            capability=ToolCapability.READ_ONLY,
            visible=True,
        )

    def get_definition(self) -> ToolDefinition:
        return self.definition

    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """读取文件"""
        file_path = Path(tool_input.get("file_path", ""))
        offset = tool_input.get("offset", 0)
        limit = tool_input.get("limit", None)

        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            if offset > 0:
                lines = lines[offset:]

            if limit:
                lines = lines[:limit]

            return {
                "success": True,
                "content": "".join(lines),
                "total_lines": len(lines),
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"File not found: {file_path}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
```

### 4.2.3 FileEditTool

```python
# pyclaude/tools/file_edit.py
from pathlib import Path
from typing import Any
from pyclaude.tools.base import BaseTool, ToolDefinition, ToolCapability


class FileEditTool(BaseTool):
    """文件编辑工具"""

    def __init__(self):
        self.definition = ToolDefinition(
            name="edit",
            description="Edit a file using string replacement",
            input_schema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to edit"
                    },
                    "old_string": {
                        "type": "string",
                        "description": "The exact string to replace"
                    },
                    "new_string": {
                        "type": "string",
                        "description": "The string to replace it with"
                    },
                    "replace_all": {
                        "type": "boolean",
                        "description": "Replace all occurrences",
                        "default": False
                    }
                },
                "required": ["file_path", "old_string", "new_string"]
            },
            capability=ToolCapability.DESTRUCTIVE,
            visible=True,
        )

    def get_definition(self) -> ToolDefinition:
        return self.definition

    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """编辑文件"""
        file_path = Path(tool_input.get("file_path", ""))
        old_string = tool_input.get("old_string", "")
        new_string = tool_input.get("new_string", "")
        replace_all = tool_input.get("replace_all", False)

        try:
            with open(file_path, "r") as f:
                content = f.read()

            if replace_all:
                new_content = content.replace(old_string, new_string)
            else:
                if old_string not in content:
                    return {
                        "success": False,
                        "error": "String not found in file"
                    }
                new_content = content.replace(old_string, new_string, 1)

            with open(file_path, "w") as f:
                f.write(new_content)

            return {
                "success": True,
                "message": "File edited successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
```

### 4.2.4 GlobTool

```python
# pyclaude/tools/glob.py
from pathlib import Path
from typing import Any
from pyclaude.tools.base import BaseTool, ToolDefinition, ToolCapability


class GlobTool(BaseTool):
    """文件模式匹配工具"""

    def __init__(self):
        self.definition = ToolDefinition(
            name="glob",
            description="Find files matching a pattern",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The glob pattern to match"
                    },
                    "path": {
                        "type": "string",
                        "description": "The directory to search in",
                        "default": "."
                    }
                },
                "required": ["pattern"]
            },
            capability=ToolCapability.READ_ONLY,
            visible=True,
        )

    def get_definition(self) -> ToolDefinition:
        return self.definition

    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """执行 glob 匹配"""
        pattern = tool_input.get("pattern", "")
        path = Path(tool_input.get("path", "."))

        try:
            files = list(path.glob(pattern))
            return {
                "success": True,
                "files": [str(f) for f in files],
                "count": len(files),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
```

### 4.2.5 GrepTool

```python
# pyclaude/tools/grep.py
from pathlib import Path
from typing import Any
from pyclaude.tools.base import BaseTool, ToolDefinition, ToolCapability


class GrepTool(BaseTool):
    """内容搜索工具"""

    def __init__(self):
        self.definition = ToolDefinition(
            name="grep",
            description="Search for patterns in files",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The regex pattern to search for"
                    },
                    "path": {
                        "type": "string",
                        "description": "The directory or file to search in",
                        "default": "."
                    },
                    "glob": {
                        "type": "string",
                        "description": "File pattern to filter",
                    },
                    "output_mode": {
                        "type": "string",
                        "description": "files_with_matches, content, count",
                        "default": "content"
                    },
                    "context": {
                        "type": "number",
                        "description": "Lines of context to show",
                        "default": 3
                    }
                },
                "required": ["pattern"]
            },
            capability=ToolCapability.READ_ONLY,
            visible=True,
        )

    def get_definition(self) -> ToolDefinition:
        return self.definition

    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """执行搜索"""
        import re
        pattern = tool_input.get("pattern", "")
        path = Path(tool_input.get("path", "."))
        output_mode = tool_input.get("output_mode", "content")
        context = tool_input.get("context", 3)

        try:
            regex = re.compile(pattern)
            results = []

            # 递归搜索文件
            for file_path in path.rglob("*"):
                if not file_path.is_file():
                    continue

                try:
                    with open(file_path, "r") as f:
                        lines = f.readlines()

                    for i, line in enumerate(lines):
                        if regex.search(line):
                            results.append({
                                "file": str(file_path),
                                "line": i + 1,
                                "content": line.rstrip(),
                            })
                except Exception:
                    continue

            return {
                "success": True,
                "results": results,
                "count": len(results),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
```

### 4.2.6 AgentTool

```python
# pyclaude/tools/agent.py
from typing import Any, Optional
from pyclaude.tools.base import BaseTool, ToolDefinition, ToolCapability
from pyclaude.engine import QueryEngine


class AgentTool(BaseTool):
    """Agent 工具 - 在子会话中执行任务"""

    def __init__(self, engine: Optional[QueryEngine] = None):
        self.engine = engine
        self.definition = ToolDefinition(
            name="Agent",
            description="Ask the agent to use tools to accomplish tasks",
            input_schema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The task description for the agent"
                    },
                    "agent": {
                        "type": "string",
                        "description": "Agent type: default, general-purpose, code-reviewer, etc.",
                        "default": "default"
                    },
                    "max_turns": {
                        "type": "number",
                        "description": "Maximum turns for this agent",
                        "default": 10
                    }
                },
                "required": ["prompt"]
            },
            capability=ToolCapability.CONCURRENT_SAFE,
            visible=True,
        )

    def get_definition(self) -> ToolDefinition:
        return self.definition

    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """执行 Agent 任务"""
        prompt = tool_input.get("prompt", "")
        agent_type = tool_input.get("agent", "default")
        max_turns = tool_input.get("max_turns", 10)

        if not self.engine:
            return {
                "success": False,
                "error": "Engine not available",
            }

        try:
            # 在子会话中执行
            result_chunks = []
            async for chunk in self.engine.query(prompt):
                result_chunks.append(chunk)

            return {
                "success": True,
                "result": "".join(result_chunks),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
```

## 4.3 工具权限系统

```python
# pyclaude/tools/permissions.py
from typing import Any
from pyclaude.tools.base import PermissionResult, ToolCapability


class PermissionChecker:
    """权限检查器"""

    DANGEROUS_PATTERNS = [
        "rm -rf",
        "dd if=",
        ":(){:|:&};:",
        "mkfs",
        "> /dev/sd",
        "chmod 777",
        "chown -R",
    ]

    PROTECTED_PATTERNS = [
        "/etc/passwd",
        "/etc/shadow",
        "~/.ssh/",
        "/.git/objects",
    ]

    @classmethod
    async def check_bash(cls, command: str) -> PermissionResult:
        """检查 Bash 命令权限"""
        for pattern in cls.DANGEROUS_PATTERNS:
            if pattern in command:
                return PermissionResult(
                    allowed=False,
                    reason=f"Command contains dangerous pattern: {pattern}"
                )

        for pattern in cls.PROTECTED_PATTERNS:
            if pattern in command:
                return PermissionResult(
                    allowed=False,
                    reason=f"Command accesses protected path: {pattern}"
                )

        return PermissionResult(allowed=True)

    @classmethod
    async def check_file_write(cls, file_path: str) -> PermissionResult:
        """检查文件写入权限"""
        # 检查是否为项目内部文件
        from pathlib import Path
        path = Path(file_path).resolve()

        # 可配置的黑名单
        protected_dirs = [".git", "node_modules", "__pycache__", ".venv"]
        for protected in protected_dirs:
            if protected in path.parts:
                return PermissionResult(
                    allowed=False,
                    reason=f"Cannot write to protected directory: {protected}"
                )

        return PermissionResult(allowed=True)
```

## 4.4 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `BashTool` | `class BashTool` | `pyclaude/tools/bash.py` |
| `FileReadTool` | `class FileReadTool` | `pyclaude/tools/file.py` |
| `FileEditTool` | `class FileEditTool` | `pyclaude/tools/file_edit.py` |
| `GlobTool` | `class GlobTool` | `pyclaude/tools/glob.py` |
| `GrepTool` | `class GrepTool` | `pyclaude/tools/grep.py` |
| `AgentTool` | `class AgentTool` | `pyclaude/tools/agent.py` |
| `WebFetchTool` | `class WebFetchTool` | `pyclaude/tools/web.py` |
| `ToolRegistry` | `class ToolRegistry` | `pyclaude/tools/registry.py` |
| `PermissionChecker` | `class PermissionChecker` | `pyclaude/tools/permissions.py` |

## 4.5 全部工具列表

| 工具名 | 描述 | 能力 |
|--------|------|------|
| `bash` | 执行 Bash 命令 | DESTRUCTIVE |
| `read` | 读取文件内容 | READ_ONLY |
| `edit` | 编辑文件 | DESTRUCTIVE |
| `glob` | 模式匹配文件 | READ_ONLY |
| `grep` | 搜索文件内容 | READ_ONLY |
| `Agent` | Agent 子任务 | CONCURRENT_SAFE |
| `WebFetch` | 获取网页内容 | READ_ONLY |
| `TodoWrite` | 任务管理 | CONCURRENT_SAFE |
| `ExitPlanMode` | 退出计划模式 | CONCURRENT_SAFE |
| `Write` | 写入文件 | DESTRUCTIVE |
| `NotebookEdit` | 笔记本编辑 | DESTRUCTIVE |