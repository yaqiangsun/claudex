# 启动流程分析

本文档详细分析 Claude Code 的启动流程，包括 setup.ts 和 main.tsx 的核心逻辑。

---

## 一、启动流程概述

### 1.1 启动流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                        main.tsx (入口)                          │
│  1. 性能分析开始 (profileCheckpoint)                            │
│  2. MDM 读取 (startMdmRawRead) - 并行                           │
│  3. Keychain 预取 (startKeychainPrefetch) - 并行                │
│  4. CLI 参数解析 (Commander.js)                                  │
│  5. 命令执行                                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      setup.ts (初始化)                          │
│  1. 版本检查 (Node.js >= 18)                                    │
│  2. UDS 消息服务器启动                                          │
│  3. 队友模式快照                                                │
│  4. 终端备份恢复                                                │
│  5. 工作目录设置 (setCwd)                                       │
│  6. Hooks 配置快照                                              │
│  7. Worktree 创建 (可选)                                        │
│  8. 预加载命令和插件                                            │
│  9. 分析服务初始化                                              │
│  10. 权限模式检查                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     interactiveHelpers.tsx                      │
│  1. 设置检查 (首次运行、版本更新)                                │
│  2. 认证检查                                                    │
│  3. 启动 REPL (launchRepl)                                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、main.tsx 详解

### 2.1 入口点结构

**文件**: `src/main.tsx` (803KB)

main.tsx 是 Claude Code 的主入口，使用 Commander.js 进行 CLI 参数解析。

#### 顶层副作用（模块加载前执行）

```typescript
// 这些副作用必须在所有其他导入之前运行：
// 1. profileCheckpoint 在重型模块评估开始前标记入口
// 2. startMdmRawRead 启动 MDM 子进程，使其与剩余导入并行运行
// 3. startKeychainPrefetch 启动 macOS keychain 读取
import { profileCheckpoint, profileReport } from './utils/startupProfiler.js';
profileCheckpoint('main_tsx_entry');

import { startMdmRawRead } from './utils/settings/mdm/rawRead.js';
startMdmRawRead();  // 并行执行 MDM 读取

import { startKeychainPrefetch } from './utils/secureStorage/keychainPrefetch.js';
startKeychainPrefetch();  // 并行执行 Keychain 预取
```

### 2.2 CLI 命令结构

```typescript
// 主程序
const program = new Command()

// 全局选项
program
  .name('claude')
  .description('Claude Code CLI')
  .version(APP_VERSION)
  .option('-p, --print', 'Print mode (headless)')
  .option('-c, --continue', 'Continue most recent session')
  .option('-r, --resume <session-id>', 'Resume specified session')

// 主要命令
program.command('chat', { isDefault: true })  // 默认命令

// 子命令
program.command('mcp')            // MCP 服务器管理
program.command('auth')           // 认证管理
program.command('plugin')         // 插件管理
program.command('open')           // 连接到远程服务器
program.command('remote-control') // 远程控制
program.command('doctor')         // 健康检查
program.command('update')         // 检查更新
program.command('install')        // 安装
```

### 2.3 关键初始化步骤

```typescript
async function main() {
  // 1. 初始化 GrowthBook (特性开关)
  initializeGrowthBook()

  // 2. 获取系统上下文
  const systemContext = getSystemContext()
  const userContext = getUserContext()

  // 3. 初始化遥测
  initializeTelemetryAfterTrust()

  // 4. 获取命令列表
  const commands = await getCommands(cwd)

  // 5. 获取工具列表
  const tools = getTools()

  // 6. 启动 REPL
  await launchRepl({
    tools,
    commands,
    messages: initialMessages,
  })
}
```

---

## 三、setup.ts 详解

### 3.1 setup 函数签名

```typescript
export async function setup(
  cwd: string,
  permissionMode: PermissionMode,
  allowDangerouslySkipPermissions: boolean,
  worktreeEnabled: boolean,
  worktreeName: string | undefined,
  tmuxEnabled: boolean,
  customSessionId?: string | null,
  worktreePRNumber?: number,
  messagingSocketPath?: string,
): Promise<void>
```

### 3.2 初始化步骤详解

#### 步骤 1: 版本检查

```typescript
// Check for Node.js version < 18
const nodeVersion = process.version.match(/^v(\d+)\./)?.[1]
if (!nodeVersion || parseInt(nodeVersion) < 18) {
  console.error('Error: Claude Code requires Node.js version 18 or higher.')
  process.exit(1)
}
```

#### 步骤 2: UDS 消息服务器

```typescript
// 启动 Unix Domain Socket 消息服务器 (Mac/Linux only)
if (feature('UDS_INBOX')) {
  const m = await import('./utils/udsMessaging.js')
  await m.startUdsMessaging(
    messagingSocketPath ?? m.getDefaultUdsSocketPath(),
    { isExplicit: messagingSocketPath !== undefined },
  )
}
```

#### 步骤 3: 队友模式快照

```typescript
// 捕获队友模式快照 (非 --bare 模式且启用了 swarms)
if (!isBareMode() && isAgentSwarmsEnabled()) {
  const { captureTeammateModeSnapshot } = await import(
    './utils/swarm/backends/teammateModeSnapshot.js'
  )
  captureTeammateModeSnapshot()
}
```

#### 步骤 4: 终端备份恢复

```typescript
// 检查并恢复 iTerm2/Terminal.app 备份
if (!getIsNonInteractiveSession()) {
  if (isAgentSwarmsEnabled()) {
    const restoredIterm2Backup = await checkAndRestoreITerm2Backup()
    // 处理恢复结果...
  }

  const restoredTerminalBackup = await checkAndRestoreTerminalBackup()
  // 处理恢复结果...
}
```

#### 步骤 5: 设置工作目录

```typescript
// IMPORTANT: setCwd() 必须在依赖 cwd 的任何其他代码之前调用
setCwd(cwd)
```

#### 步骤 6: Hooks 配置快照

```typescript
// 捕获 hooks 配置快照以避免隐藏的 hook 修改
captureHooksConfigSnapshot()

// 初始化 FileChanged hook watcher
initializeFileChangedWatcher(cwd)
```

#### 步骤 7: Worktree 创建 (可选)

```typescript
// 处理 worktree 创建请求
if (worktreeEnabled) {
  // 检查 git 仓库
  const inGit = await getIsGit()

  // 创建 worktree
  const worktreeSession = await createWorktreeForSession(
    getSessionId(),
    slug,
    tmuxSessionName,
    worktreePRNumber ? { prNumber: worktreePRNumber } : undefined,
  )

  // 创建 tmux 会话 (如果启用)
  if (tmuxEnabled && tmuxSessionName) {
    await createTmuxSessionForWorktree(tmuxSessionName, worktreeSession.worktreePath)
  }

  // 切换到 worktree 目录
  process.chdir(worktreeSession.worktreePath)
  setCwd(worktreeSession.worktreePath)
}
```

#### 步骤 8: 后台任务初始化

```typescript
// 初始化会话内存
initSessionMemory()

// 初始化 Context Collapse (如果启用)
if (feature('CONTEXT_COLLAPSE')) {
  const { initContextCollapse } = await import('./services/contextCollapse/index.js')
  initContextCollapse()
}

// 锁定当前版本
void lockCurrentVersion()
```

#### 步骤 9: 预加载

```typescript
// 预加载命令
void getCommands(getProjectRoot())

// 预加载插件 hooks
void import('./utils/plugins/loadPluginHooks.js').then(m => {
  void m.loadPluginHooks()
  m.setupPluginHookHotReload()
})
```

#### 步骤 10: 分析服务

```typescript
// 初始化分析接收器
initSinks()

// 记录启动事件
logEvent('tengu_started', {})
```

#### 步骤 11: 权限模式检查

```typescript
// 如果权限模式设置为 bypass，验证我们在安全环境中
if (permissionMode === 'bypassPermissions' || allowDangerouslySkipPermissions) {
  // 安全检查...
}
```

---

## 四、launchRepl 流程

### 4.1 REPL 启动

```typescript
export async function launchRepl(options: LaunchReplOptions): Promise<void> {
  const { tools, commands, messages, resumeSessionId } = options

  // 1. 创建 Ink 应用
  const app = createApp({
    tools,
    commands,
    messages,
  })

  // 2. 渲染应用
  render(app, () => {
    // 3. 处理退出
    process.exit(0)
  })
}
```

---

## 五、Python 版本实现建议

### 5.1 启动流程实现

```python
# claudex/cli/startup.py

import asyncio
from dataclasses import dataclass

@dataclass
class SetupConfig:
    cwd: str
    permission_mode: str
    skip_permissions: bool
    worktree_enabled: bool
    worktree_name: str | None
    tmux_enabled: bool
    custom_session_id: str | None

async def setup(config: SetupConfig) -> None:
    """主初始化函数"""
    # 1. 版本检查
    check_node_version()

    # 2. 初始化分析服务
    init_analytics()

    # 3. 设置工作目录
    set_cwd(config.cwd)

    # 4. 捕获 hooks 配置
    capture_hooks_config()

    # 5. 加载命令和工具
    commands = await load_commands()
    tools = load_tools()

    # 6. 启动 REPL
    await launch_repl(commands, tools)

async def launch_repl(commands: list[Command], tools: list[Tool]) -> None:
    """启动 REPL 循环"""
    while True:
        # 读取输入
        line = await read_input()

        # 处理命令
        if line.startswith('/'):
            await handle_command(line, commands)
        else:
            # 查询引擎
            await query_engine.submit(line)
```

### 5.2 CLI 参数解析

```python
# claudex/cli/parser.py

import click

@click.group()
@click.option('--print', 'print_mode', is_flag=True)
@click.option('-c', '--continue', 'continue_session', is_flag=True)
@click.option('-r', '--resume', 'session_id')
def cli(print_mode, continue_session, session_id):
    pass

@cli.command()
def mcp():
    """Configure and manage MCP servers"""
    pass

@cli.command()
def auth():
    """Manage authentication"""
    pass

@cli.command()
def doctor():
    """Check health"""
    pass

if __name__ == '__main__':
    cli()
```

---

## 六、关键文件映射

| TypeScript | 功能 | Python 建议 |
|------------|------|-------------|
| `main.tsx` | 入口点、CLI 解析 | `cli.py` |
| `setup.ts` | 初始化逻辑 | `startup.py` |
| `replLauncher.tsx` | REPL 启动 | `repl.py` |
| `interactiveHelpers.tsx` | 交互帮助 | `helpers.py` |
| `ink.ts` | React 渲染 | - (Python 无需) |

---

## 七、启动参数示例

```bash
# 交互式启动
claude

# 打印模式（无头）
claude -p "your prompt"

# 继续最近会话
claude -c

# 恢复指定会话
claude -r session-abc123

# 使用 worktree
claude --worktree my-branch

# 带 tmux 的 worktree
claude --worktree --tmux

# MCP 管理
claude mcp list
claude mcp add my-server "npx -y server"

# 认证
claude auth status
claude auth logout

# 健康检查
claude doctor
```

---

*文档版本: 1.0*
*分析时间: 2026-04-09*