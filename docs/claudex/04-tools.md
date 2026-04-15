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

## 4.2 BashTool 详细实现

### 4.2.1 工具定义

```python
# pyclaude/tools/bash.py
import asyncio
from typing import Any, Optional
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
                    },
                    "run_in_background": {
                        "type": "boolean",
                        "description": "Run in background",
                        "default": False
                    },
                    "dangerouslyDisableSandbox": {
                        "type": "boolean",
                        "description": "Disable sandbox (if available)",
                        "default": False
                    }
                },
                "required": ["command"]
            },
            capability=ToolCapability.DESTRUCTIVE | ToolCapability.CONCURRENT_SAFE,
            visible=True,
        )
        # 权限检查器
        self.permission_checker = BashPermissionChecker()
        # 安全验证器
        self.security_validator = BashSecurityValidator()
        # 沙箱管理器
        self.sandbox_manager = SandboxManager()

    def get_definition(self) -> ToolDefinition:
        return self.definition

    async def check_permission(self, tool_input: dict[str, Any]) -> PermissionResult:
        """权限检查 - 使用 AST 解析"""
        command = tool_input.get("command", "")

        # 1. 权限规则检查 (allow/ask/deny)
        rule_result = await self.permission_checker.check(command)
        if not rule_result.allowed:
            return rule_result

        # 2. 安全验证 (23+ 安全检查)
        security_result = self.security_validator.validate(command)
        if not security_result.allowed:
            return security_result

        # 3. 只读命令自动允许
        if self._is_read_only_command(command):
            return PermissionResult(allowed=True)

        return PermissionResult(allowed=True)

    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        """执行 Bash 命令"""
        command = tool_input.get("command", "")
        description = tool_input.get("description", "")
        run_in_background = tool_input.get("run_in_background", False)
        disable_sandbox = tool_input.get("dangerouslyDisableSandbox", False)

        # 决定是否使用沙箱
        use_sandbox = (
            self.sandbox_manager.is_enabled() and
            not disable_sandbox and
            not self.sandbox_manager.is_excluded_command(command)
        )

        if use_sandbox:
            return await self._execute_sandbox(command, description)
        else:
            return await self._execute_direct(command, description, run_in_background)

    async def _execute_direct(
        self,
        command: str,
        description: str,
        run_in_background: bool,
    ) -> dict[str, Any]:
        """直接执行"""
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        if run_in_background:
            return {"success": True, "pid": process.pid, "background": True}

        stdout, stderr = await process.communicate()
        return {
            "success": process.returncode == 0,
            "stdout": stdout.decode("utf-8"),
            "stderr": stderr.decode("utf-8"),
            "exit_code": process.returncode,
        }

    async def _execute_sandbox(self, command: str, description: str) -> dict[str, Any]:
        """沙箱执行"""
        config = self.sandbox_manager.get_config(command)

        # 使用沙箱运行时执行
        result = await self.sandbox_manager.run(command, config)
        return result

    def _is_read_only_command(self, command: str) -> bool:
        """检测只读命令"""
        # 使用语义分析检测只读命令
        return ReadOnlyDetector.is_read_only(command)
```

## 4.3 权限系统详解

### 4.3.1 权限规则匹配

```python
# pyclaude/tools/permissions/rules.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import fnmatch


class PermissionAction(str, Enum):
    """权限动作"""
    ALLOW = "allow"    # 自动允许
    ASK = "ask"        # 询问用户
    DENY = "deny"      # 拒绝


class MatchType(str, Enum):
    """匹配类型"""
    EXACT = "exact"       # 精确匹配
    PREFIX = "prefix"     # 前缀匹配
    WILDCARD = "wildcard" # 通配符匹配
    CONTENT = "content"   # 内容匹配


@dataclass
class PermissionRule:
    """权限规则"""
    pattern: str           # 匹配模式
    match_type: MatchType  # 匹配类型
    action: PermissionAction  # 动作
    tools: list[str]       # 适用的工具
    reason: Optional[str] = None


class BashPermissionChecker:
    """Bash 权限检查器"""

    def __init__(self):
        self.rules: list[PermissionRule] = []
        self._load_default_rules()

    def _load_default_rules(self) -> None:
        """加载默认规则"""
        # 精确匹配
        self.rules.append(PermissionRule(
            pattern="Bash(rm:*)",
            match_type=MatchType.EXACT,
            action=PermissionAction.ASK,
            tools=["bash"],
        ))

        # 前缀匹配
        self.rules.append(PermissionRule(
            pattern="Bash(npm run:*)",
            match_type=MatchType.PREFIX,
            action=PermissionAction.ALLOW,
            tools=["bash"],
        ))

        # 通配符匹配
        self.rules.append(PermissionRule(
            pattern="Bash(git commit:*)",
            match_type=MatchType.WILDCARD,
            action=PermissionAction.ALLOW,
            tools=["bash"],
        ))

        # 内容匹配
        self.rules.append(PermissionRule(
            pattern="Bash(*git commit*)",
            match_type=MatchType.CONTENT,
            action=PermissionAction.ALLOW,
            tools=["bash"],
        ))

    async def check(self, command: str) -> PermissionResult:
        """检查命令权限"""
        for rule in self.rules:
            if self._matches(rule, command):
                if rule.action == PermissionAction.ALLOW:
                    return PermissionResult(allowed=True, reason=rule.reason)
                elif rule.action == PermissionAction.DENY:
                    return PermissionResult(allowed=False, reason=rule.reason)
                elif rule.action == PermissionAction.ASK:
                    return PermissionResult(
                        allowed=False,
                        reason=f"Requires permission: {rule.reason}",
                        metadata={"requires_prompt": True},
                    )

        # 默认允许
        return PermissionResult(allowed=True)

    def _matches(self, rule: PermissionRule, command: str) -> bool:
        """检查命令是否匹配规则"""
        if "bash" not in rule.tools:
            return False

        if rule.match_type == MatchType.EXACT:
            return command == rule.pattern.replace("Bash(", "").rstrip(")")
        elif rule.match_type == MatchType.PREFIX:
            prefix = rule.pattern.replace("Bash(", "").rstrip(":*") + ":"
            return command.startswith(prefix)
        elif rule.match_type == MatchType.WILDCARD:
            pattern = rule.pattern.replace("Bash(", "").rstrip(")")
            return fnmatch.fnmatch(command, pattern)
        elif rule.match_type == MatchType.CONTENT:
            content_pattern = rule.pattern.replace("Bash(*", "").rstrip("*)")
            return content_pattern in command

        return False
```

### 4.3.2 安全验证 (23+ 检查)

```python
# pyclaude/tools/permissions/security.py
from dataclasses import dataclass
from enum import Enum
import re


class SecurityCheckId(str, Enum):
    """安全检查 ID"""
    INCOMPLETE_COMMANDS = 1
    JQ_SYSTEM_FUNCTION = 2
    JQ_FILE_ARGUMENTS = 3
    OBFUSCATED_FLAGS = 4
    SHELL_METACHARACTERS = 5
    DANGEROUS_VARIABLES = 6
    NEWLINES = 7
    DANGEROUS_PATTERNS_COMMAND_SUBSTITUTION = 8
    DANGEROUS_PATTERNS_INPUT_REDIRECTION = 9
    DANGEROUS_PATTERNS_OUTPUT_REDIRECTION = 10
    IFS_INJECTION = 11
    GIT_COMMIT_SUBSTITUTION = 12
    PROC_ENVIRON_ACCESS = 13
    MALFORMED_TOKEN_INJECTION = 14
    BACKSLASH_ESCAPED_WHITESPACE = 15
    BRACE_EXPANSION = 16
    CONTROL_CHARACTERS = 17
    UNICODE_WHITESPACE = 18
    MID_WORD_HASH = 19
    ZSH_DANGEROUS_COMMANDS = 20
    BACKSLASH_ESCAPED_OPERATORS = 21
    COMMENT_QUOTE_DESYNC = 22
    QUOTED_NEWLINE = 23


@dataclass
class SecurityValidationResult:
    """安全验证结果"""
    allowed: bool
    violations: list[tuple[SecurityCheckId, str]]


class BashSecurityValidator:
    """Bash 安全验证器"""

    # 安全检查模式
    PATTERNS = {
        SecurityCheckId.COMMAND_SUBSTITUTION: r'\$\(.*?\)|`.*?`|\$\{.*?\}|\$\(<\s*\S+',
        SecurityCheckId.PROCESS_SUBSTITUTION: r'<\(\)|>\(\)|=\(',
        SecurityCheckId.ZSH_DANGEROUS: r'(zmodload|emulate|zpty|ztcp|bindkey|compdef|register)',
        SecurityCheckId.GIT_COMMIT_SUBSTITUTION: r'git\s+commit\s+(-m|--message)\s+["\']?\$\(',
        SecurityCheckId.PROC_ENVIRON: r'/proc/\d+/environ',
        SecurityCheckId.IFS_INJECTION: r'IFS=',
        SecurityCheckId.CONTROL_CHARACTERS: r'[\x00-\x1f\x7f]',
    }

    def validate(self, command: str) -> PermissionResult:
        """验证命令安全性"""
        violations = []

        for check_id, pattern in self.PATTERNS.items():
            if re.search(pattern, command, re.IGNORECASE):
                violations.append((check_id, f"Security check {check_id.value} failed"))

        if violations:
            reason = "; ".join([v[1] for v in violations])
            return PermissionResult(allowed=False, reason=reason)

        return PermissionResult(allowed=True)
```

### 4.3.3 沙箱系统

```python
# pyclaude/tools/permissions/sandbox.py
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import platform


class SandboxPlatform(str, Enum):
    """支持的沙箱平台"""
    MACOS = "macos"
    LINUX = "linux"
    WSL = "wsl"
    WINDOWS = "windows"  # 不支持


@dataclass
class SandboxConfig:
    """沙箱配置"""
    allow_write: list[str] = field(default_factory=list)
    deny_write: list[str] = field(default_factory=list)
    allow_read: list[str] = field(default_factory=list)
    deny_read: list[str] = field(default_factory=list)
    network_allowed_domains: list[str] = field(default_factory=list)
    network_denied_domains: list[str] = field(default_factory=list)


@dataclass
class SandboxResult:
    """沙箱执行结果"""
    success: bool
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    error: Optional[str] = None


class SandboxManager:
    """沙箱管理器"""

    # 保护路径
    PROTECTED_PATHS = [
        ".claude/skills",
        ".claude/settings.json",
        ".git/objects",
    ]

    def __init__(self):
        self.enabled = False
        self._check_platform_support()

    def _check_platform_support(self) -> None:
        """检查平台支持"""
        system = platform.system().lower()
        if system == "darwin":
            self.platform = SandboxPlatform.MACOS
        elif system == "linux":
            self.platform = SandboxPlatform.LINUX
        elif "microsoft" in platform.uname().release.lower():
            self.platform = SandboxPlatform.WSL
        else:
            self.platform = SandboxPlatform.WINDOWS
            return

        # 检查依赖
        if self._check_dependencies():
            self.enabled = True

    def _check_dependencies(self) -> bool:
        """检查沙箱依赖"""
        # macOS: 无需额外依赖
        # Linux: 需要 bubblewrap, socat
        if self.platform == SandboxPlatform.LINUX:
            import shutil
            return shutil.which("bubblewrap") is not None
        return True

    def is_enabled(self) -> bool:
        """检查沙箱是否启用"""
        return self.enabled

    def is_excluded_command(self, command: str) -> bool:
        """检查命令是否排除在沙箱外"""
        excluded_patterns = [
            "sudo",
            "su -",
            "login",
        ]
        return any(p in command for p in excluded_patterns)

    def get_config(self, command: str) -> SandboxConfig:
        """获取命令的沙箱配置"""
        config = SandboxConfig()

        # 默认允许读取
        config.allow_read = ["/"]

        # 保护路径
        config.deny_write = self.PROTECTED_PATHS

        return config

    async def run(self, command: str, config: SandboxConfig) -> SandboxResult:
        """在沙箱中运行命令"""
        # 使用 bubblewrap 创建沙箱环境
        # 构建 bubblewrap 命令行参数
        args = [
            "bwrap",
            "--ro-bind", "/", "/",  # 只读挂载根目录
            "--proc", "/proc",      # 允许访问 /proc
            "--dev", "/dev",        # 允许访问设备
        ]

        # 添加写权限
        for path in config.allow_write:
            args.extend(["--bind", path, path])

        # 添加拒绝路径
        for path in config.deny_write:
            args.extend(["--bind-try", path, path])  # 如果失败则忽略

        # 添加网络限制
        if config.network_allowed_domains:
            # 配置网络策略
            pass

        # 执行命令
        args.append("sh")
        args.append("-c")
        args.append(command)

        try:
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await process.communicate()

            return SandboxResult(
                success=process.returncode == 0,
                stdout=stdout.decode("utf-8"),
                stderr=stderr.decode("utf-8"),
                exit_code=process.returncode,
            )
        except Exception as e:
            return SandboxResult(
                success=False,
                error=str(e),
            )
```

### 4.3.4 只读命令检测

```python
# pyclaude/tools/permissions/readonly.py
from typing import Optional


class ReadOnlyDetector:
    """只读命令检测器"""

    # 只读命令分类
    SEARCH_COMMANDS = {"find", "grep", "rg", "ag", "ack", "locate", "which", "whereis"}
    READ_COMMANDS = {"cat", "head", "tail", "less", "more", "wc", "stat", "file", "strings", "jq", "awk"}
    LIST_COMMANDS = {"ls", "tree", "du", "df"}

    @classmethod
    def is_read_only(cls, command: str) -> bool:
        """检测是否为只读命令"""
        first_word = command.strip().split()[0] if command.strip() else ""

        # 移除路径前缀
        cmd = first_word.split("/")[-1]

        # 检查命令类别
        if cmd in cls.SEARCH_COMMANDS | cls.READ_COMMANDS | cls.LIST_COMMANDS:
            return True

        # 检查是否有副作用
        if cls._has_side_effects(command):
            return False

        return True

    @classmethod
    def _has_side_effects(cls, command: str) -> bool:
        """检查是否有副作用"""
        side_effect_patterns = [
            r">\s*\S",          # 输出重定向
            r"<\s*\S",          # 输入重定向
            r"\|",              # 管道
            r"&&\s*\S",         # 命令链
            r"\|\|\s*\S",       # 命令链
            r"\$\(",            # 命令替换
        ]

        import re
        return any(re.search(p, command) for p in side_effect_patterns)
```

## 4.4 其他核心工具

### 4.4.1 FileReadTool

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
                    "file_path": {"type": "string"},
                    "offset": {"type": "number", "default": 0},
                    "limit": {"type": "number"},
                },
                "required": ["file_path"]
            },
            capability=ToolCapability.READ_ONLY,
            visible=True,
        )

    async def execute(self, tool_input: dict[str, Any]) -> dict[str, Any]:
        file_path = Path(tool_input.get("file_path", ""))
        # ... 实现
```

### 4.4.2 AgentTool

```python
# pyclaude/tools/agent.py
class AgentTool(BaseTool):
    """Agent 工具 - 支持内存作用域"""

    def __init__(self):
        self.definition = ToolDefinition(
            name="Agent",
            description="Ask the agent to use tools to accomplish tasks",
            input_schema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string"},
                    "agent": {"type": "string", "default": "default"},
                    "max_turns": {"type": "number", "default": 10},
                    "memory_scope": {
                        "type": "string",
                        "enum": ["user", "project", "local"],
                        "default": "project",
                    },
                },
                "required": ["prompt"]
            },
            capability=ToolCapability.CONCURRENT_SAFE,
        )

    async def execute(self, tool_input: dict) -> dict:
        # Agent 内存管理
        memory_scope = tool_input.get("memory_scope", "project")
        agent_memory_dir = self._get_agent_memory_dir(
            tool_input.get("agent", "default"),
            memory_scope,
        )
        # ... 执行逻辑
```

## 4.5 模块接口清单

| TypeScript | Python | 文件 |
|------------|--------|------|
| `BashTool` | `class BashTool` | `pyclaude/tools/bash.py` |
| `BashPermissionChecker` | `class BashPermissionChecker` | `pyclaude/tools/permissions/rules.py` |
| `BashSecurityValidator` | `class BashSecurityValidator` | `pyclaude/tools/permissions/security.py` |
| `SandboxManager` | `class SandboxManager` | `pyclaude/tools/permissions/sandbox.py` |
| `ReadOnlyDetector` | `class ReadOnlyDetector` | `pyclaude/tools/permissions/readonly.py` |
| `FileReadTool` | `class FileReadTool` | `pyclaude/tools/file.py` |
| `FileEditTool` | `class FileEditTool` | `pyclaude/tools/file_edit.py` |
| `GlobTool` | `class GlobTool` | `pyclaude/tools/glob.py` |
| `GrepTool` | `class GrepTool` | `pyclaude/tools/grep.py` |
| `AgentTool` | `class AgentTool` | `pyclaude/tools/agent.py` |
| `ToolRegistry` | `class ToolRegistry` | `pyclaude/tools/registry.py` |

## 4.6 全部工具列表

| 工具名 | 描述 | 能力 | 安全级别 |
|--------|------|------|----------|
| `bash` | 执行 Bash 命令 | DESTRUCTIVE | 需权限+沙箱 |
| `read` | 读取文件内容 | READ_ONLY | 安全 |
| `edit` | 编辑文件 | DESTRUCTIVE | 需权限 |
| `glob` | 模式匹配文件 | READ_ONLY | 安全 |
| `grep` | 搜索文件内容 | READ_ONLY | 安全 |
| `Agent` | Agent 子任务 | CONCURRENT_SAFE | 内存隔离 |
| `WebFetch` | 获取网页内容 | READ_ONLY | 安全 |
| `TodoWrite` | 任务管理 | CONCURRENT_SAFE | 安全 |
| `ExitPlanMode` | 退出计划模式 | CONCURRENT_SAFE | 安全 |
| `Write` | 写入文件 | DESTRUCTIVE | 需权限 |
| `NotebookEdit` | 笔记本编辑 | DESTRUCTIVE | 不执行代码 |