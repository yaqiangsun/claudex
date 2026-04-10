# 技能系统分析

本文档详细分析 Claude Code 的技能（Skills）系统。

---

## 一、Skills 目录结构

```
src/skills/
├── bundled/                    # 内置技能实现
│   ├── index.ts               # 内置技能初始化入口
│   ├── batch.ts               # 批量操作技能
│   ├── claudeApi.ts           # Claude API 技能
│   ├── claudeInChrome.ts      # Chrome 集成技能
│   ├── debug.ts               # 调试技能 ⭐
│   ├── keybindings.ts         # 快捷键技能
│   ├── loop.ts                # 循环技能
│   ├── loremIpsum.ts          # 占位符技能
│   ├── remember.ts            # 记忆技能
│   ├── scheduleRemoteAgents.ts # 远程 Agent 调度
│   ├── simplify.ts            # 代码简化技能 ⭐
│   ├── skillify.ts            # 技能化技能
│   ├── stuck.ts               # 卡住处理技能
│   ├── updateConfig.ts        # 更新配置技能
│   ├── verify.ts              # 验证技能
│   └── verifyContent.ts       # 内容验证技能
├── bundledSkills.ts           # 技能注册核心逻辑
├── loadSkillsDir.ts           # 技能加载逻辑
└── mcpSkillBuilders.ts        # MCP 技能构建器
```

---

## 二、技能系统架构

### 2.1 技能类型

| 类型 | 来源 | 加载方式 |
|------|------|----------|
| **bundled** | CLI 内置 (15+ 个) | 程序化注册 (`registerBundledSkill`) |
| **skills/** | 用户/项目技能目录 | 目录加载 (`skill-name/SKILL.md`) |
| **commands/** | 传统命令目录 | 兼容加载 (支持单文件和目录格式) |
| **mcp** | MCP 服务器 | MCP 协议加载 |
| **plugin** | 插件 | 插件加载 |

### 2.2 技能加载来源

```typescript
// loadSkillsDir.ts
export type LoadedFrom =
  | 'commands_DEPRECATED'  // 传统 /commands/ 目录
  | 'skills'               // /skills/ 目录
  | 'plugin'               // 插件
  | 'managed'              // 托管策略
  | 'bundled'              // 内置
  | 'mcp'                  // MCP 服务器
```

---

## 三、内置技能详解

### 3.1 技能初始化流程

```typescript
// bundled/index.ts
export function initBundledSkills(): void {
  registerUpdateConfigSkill()    // 更新配置
  registerKeybindingsSkill()     // 快捷键
  registerVerifySkill()          // 验证
  registerDebugSkill()           // 调试
  registerLoremIpsumSkill()      // 占位符
  registerSkillifySkill()        // 技能化
  registerRememberSkill()        // 记忆
  registerSimplifySkill()        // 代码简化
  registerBatchSkill()           // 批量操作
  registerStuckSkill()           // 卡住处理
  // 条件加载...
}
```

### 3.2 核心内置技能

#### Debug Skill (`/debug`)

```typescript
// 用途: 调试当前会话
// 工具: Read, Grep, Glob
// 特点: disableModelInvocation (用户必须显式调用)
registerBundledSkill({
  name: 'debug',
  description: 'Enable debug logging for this session and help diagnose issues',
  allowedTools: ['Read', 'Grep', 'Glob'],
  disableModelInvocation: true,
  async getPromptForCommand(args) {
    // 读取调试日志最后 N 行
    // 返回调试提示
  }
})
```

#### Simplify Skill (`/simplify`)

```typescript
// 用途: 代码审查和清理
// 启动三个并行 Agent:
//   1. Code Reuse Review - 代码复用审查
//   2. Code Quality Review - 代码质量审查
//   3. Efficiency Review - 效率审查

// 示例 prompt 结构:
const SIMPLIFY_PROMPT = `# Simplify: Code Review and Cleanup

## Phase 1: Identify Changes
Run \`git diff\` to see what changed.

## Phase 2: Launch Three Review Agents in Parallel
Use AgentTool to launch all three agents concurrently.

### Agent 1: Code Reuse Review
- Search for existing utilities that could replace new code
- Flag duplicate functionality

### Agent 2: Code Quality Review
- Redundant state, parameter sprawl, copy-paste
- Leaky abstractions, stringly-typed code

### Agent 3: Efficiency Review
- Unnecessary work, missed concurrency
- Hot-path bloat, memory issues
`
```

#### 其他内置技能

| 技能名 | 功能 | 条件 |
|--------|------|------|
| `/updateConfig` | 更新配置文件 | 默认 |
| `/keybindings` | 显示快捷键 | 默认 |
| `/verify` | 验证代码 | 默认 |
| `/debug` | 调试会话 | 默认 |
| `/loremIpsum` | 生成占位符 | 默认 |
| `/skillify` | 将命令转为技能 | 默认 |
| `/remember` | 记住信息 | 默认 |
| `/simplify` | 代码简化 | 默认 |
| `/batch` | 批量操作 | 默认 |
| `/stuck` | 处理卡住 | 默认 |
| `/dream` | 梦的模式 | `KAIROS` 或 `KAIROS_DREAM` |
| `/hunter` | 审查 Artifact | `REVIEW_ARTIFACT` |
| `/loop` | 循环触发 | `AGENT_TRIGGERS` |
| `/scheduleRemoteAgents` | 远程调度 | `AGENT_TRIGGERS_REMOTE` |
| `/claudeApi` | Claude API | `BUILDING_CLAUDE_APPS` |
| `/claudeInChrome` | Chrome 集成 | `shouldAutoEnableClaudeInChrome()` |
| `/runSkillGenerator` | 技能生成器 | `RUN_SKILL_GENERATOR` |

---

## 四、技能注册机制

### 4.1 registerBundledSkill

```typescript
// bundledSkills.ts
export type BundledSkillDefinition = {
  name: string              // 技能名称 (/name 调用)
  description: string       // 描述
  aliases?: string[]        // 别名
  whenToUse?: string        // 使用时机提示
  argumentHint?: string     // 参数提示
  allowedTools?: string[]   // 允许的工具
  model?: string            // 指定模型
  disableModelInvocation?: boolean  // 禁用模型调用
  userInvocable?: boolean   // 用户可调用
  isEnabled?: () => boolean // 启用条件
  hooks?: HooksSettings     // Hooks 配置
  context?: 'inline' | 'fork'  // 执行上下文
  agent?: string            // 指定 agent
  files?: Record<string, string>  // 附加文件
  getPromptForCommand: (
    args: string,
    context: ToolUseContext
  ) => Promise<ContentBlockParam[]>
}

// 注册函数
export function registerBundledSkill(definition: BundledSkillDefinition): void
```

### 4.2 技能命令结构

```typescript
// 创建技能命令
const command: Command = {
  type: 'prompt',
  name: 'debug',
  description: '...',
  allowedTools: ['Read', 'Grep'],
  argumentHint: '[issue description]',
  disableModelInvocation: true,
  userInvocable: true,
  source: 'bundled',
  loadedFrom: 'bundled',
  isHidden: false,
  progressMessage: 'running',
  getPromptForCommand: async (args, context) => {
    // 返回 prompt 内容
    return [{ type: 'text', text: prompt }]
  }
}
```

---

## 五、磁盘技能加载

### 5.1 技能目录结构

```
.claude/
├── skills/                  # 用户/项目技能目录
│   ├── skill-name-1/
│   │   └── SKILL.md        # 技能定义 (必须)
│   │   └── [其他文件]       # 辅助文件
│   └── skill-name-2/
│       └── SKILL.md
└── commands/               # 传统命令目录 (兼容)
    ├── cmd-name.md
    └── legacy-skill/
        └── SKILL.md
```

### 5.2 SKILL.md 格式

```markdown
---
name: My Skill              # 显示名称 (可选)
description: 技能描述        # 必填
when_to_use: 何时使用        # 可选
arguments: [arg1, arg2]     # 参数名称
argument-hint: 参数提示      # 可选
allowed-tools: [Read, Grep] # 允许的工具
user-invocable: true        # 用户可调用 (默认 true)
model: claude-sonnet-4-20250514  # 指定模型
disable-model-invocation: false  # 禁用模型调用
paths:                      # 条件触发路径
  - "src/**/*.ts"
  - "**/*.js"
hooks:                      # Hooks 配置
  on_match: ...
shell: !`echo hello`        # Shell 命令 (内联执行)
---

# 技能 Prompt

技能的实际 prompt 内容...

## 变量替换

- \${CLAUDE_SKILL_DIR} - 技能目录路径
- \${CLAUDE_SESSION_ID} - 会话 ID
- \$1, \$2 - 位置参数

## 内联 Shell

\`\`\`!bash
echo "执行 shell 命令"
\`\`\`
```

### 5.3 Frontmatter 字段

```typescript
parseSkillFrontmatterFields 返回:
{
  displayName: string | undefined        // 显示名称
  description: string                    // 描述
  hasUserSpecifiedDescription: boolean   // 是否用户指定
  allowedTools: string[]                 // 允许工具
  argumentHint: string | undefined       // 参数提示
  argumentNames: string[]                // 参数名
  whenToUse: string | undefined          // 使用时机
  version: string | undefined            // 版本
  model: ModelConfig | undefined         // 模型配置
  disableModelInvocation: boolean        // 禁用模型调用
  userInvocable: boolean                 // 用户可调用
  hooks: HooksSettings | undefined       // Hooks
  executionContext: 'fork' | undefined   // 执行上下文
  agent: string | undefined              // 指定 Agent
  effort: EffortValue | undefined        // 努力级别
  shell: FrontmatterShell | undefined    // Shell 配置
}
```

---

## 六、动态技能发现

### 6.1 条件技能 (Conditional Skills)

```typescript
// 带 paths frontmatter 的技能会延迟加载
// 只有当匹配的文件被操作时才激活

// 激活逻辑 (loadSkillsDir.ts)
export function activateConditionalSkillsForPaths(
  filePaths: string[],
  cwd: string
): string[] {
  // 使用 ignore 库匹配 gitignore 模式
  const skillIgnore = ignore().add(skill.paths)

  for (const filePath of filePaths) {
    const relativePath = relative(cwd, filePath)
    if (skillIgnore.ignores(relativePath)) {
      // 激活技能
      dynamicSkills.set(name, skill)
      activated.push(name)
    }
  }
}
```

### 6.2 动态目录发现

```typescript
// 动态发现嵌套的 .claude/skills 目录
export async function discoverSkillDirsForPaths(
  filePaths: string[],
  cwd: string
): Promise<string[]> {
  // 从文件路径向上遍历到 cwd
  // 发现嵌套的 skills 目录
}
```

---

## 七、Python 版本实现建议

### 7.1 技能系统架构

```python
# claudex/skills/__init__.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncGenerator

@dataclass
class SkillDefinition:
    name: str
    description: str
    allowed_tools: list[str]
    argument_hint: str | None = None
    user_invocable: bool = True
    disable_model_invocation: bool = False

class Skill(ABC):
    @property
    @abstractmethod
    def definition(self) -> SkillDefinition:
        pass

    @abstractmethod
    async def get_prompt(
        self,
        args: str,
        context: "ToolUseContext"
    ) -> list[ContentBlock]:
        pass
```

### 7.2 内置技能注册

```python
# claudex/skills/bundled.py

from claudex.skills.base import Skill, SkillDefinition
from claudex.skills.registry import register_bundled_skill

class DebugSkill(Skill):
    @property
    def definition(self) -> SkillDefinition:
        return SkillDefinition(
            name="debug",
            description="Enable debug logging for this session",
            allowed_tools=["Read", "Grep", "Glob"],
            disable_model_invocation=True,
        )

    async def get_prompt(self, args: str, context) -> list[ContentBlock]:
        # 读取调试日志
        # 返回 prompt
        return [{"type": "text", "text": "..."}]

def register_debug_skill():
    register_bundled_skill(DebugSkill())
```

### 7.3 磁盘技能加载

```python
# claudex/skills/loader.py

import os
from pathlib import Path

class SkillLoader:
    def __init__(self, config_dir: str):
        self.skills_dir = Path(config_dir) / "skills"

    async def load_skills(self) -> list[Skill]:
        skills = []
        if not self.skills_dir.exists():
            return skills

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skill = await self._load_skill(skill_dir, skill_file)
                skills.append(skill)
        return skills

    async def _load_skill(self, skill_dir: Path, skill_file: Path):
        content = skill_file.read_text()
        frontmatter, markdown = parse_frontmatter(content)
        # 解析 frontmatter
        # 创建 Skill 实例
        return DiskSkill(
            name=skill_dir.name,
            description=frontmatter.get("description", ""),
            content=markdown,
            allowed_tools=frontmatter.get("allowed-tools", []),
        )
```

### 7.4 技能目录结构

```
claudex/skills/
├── __init__.py
├── base.py              # Skill 基类和接口
├── registry.py          # 技能注册表
├── bundled/
│   ├── __init__.py      # init_bundled_skills()
│   ├── debug.py         # DebugSkill
│   ├── simplify.py      # SimplifySkill
│   └── ...
├── loader.py            # 磁盘技能加载
├── frontmatter.py       # Frontmatter 解析
└── executor.py          # 技能执行器
```

---

## 八、关键设计模式

### 8.1 技能 vs 命令

| 特性 | 技能 (Skill) | 命令 (Command) |
|------|-------------|----------------|
| 格式 | 目录/SKILL.md | .md 文件 |
| 加载 | /skills/ | /commands/ |
| 参数 | 支持 ${1}, ${2} | 支持 |
| 内联 Shell | 支持 !`...` | 不支持 |
| 条件触发 | 支持 paths | 不支持 |

### 8.2 变量替换

```markdown
---
arguments: [filename, content]
---

Review the file ${1:filename} and check if it contains: ${2:content}

CLI 会替换为:
Review the file test.py and check if it contains: TODO
```

### 8.3 安全机制

```typescript
// MCP 技能禁止内联 Shell 执行
if (loadedFrom !== 'mcp') {
  finalContent = await executeShellCommandsInPrompt(finalContent, ...)
}

// 路径遍历防护
function resolveSkillFilePath(baseDir: string, relPath: string): string {
  const normalized = normalize(relPath)
  if (normalized.includes('..')) {
    throw new Error('path escapes skill dir')
  }
  return join(baseDir, normalized)
}
```

---

*文档版本: 1.0*
*分析时间: 2026-04-10*