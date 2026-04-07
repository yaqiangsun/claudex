"""Git operation tracking matching src/tools/shared/gitOperationTracking.ts"""
import re
from typing import Optional, Dict, Any
from dataclasses import dataclass


CommitKind = str  # 'committed' | 'amended' | 'cherry-picked'
BranchAction = str  # 'merged' | 'rebased'
PrAction = str  # 'created' | 'edited' | 'merged' | 'commented' | 'closed' | 'ready'


def git_cmd_re(subcmd: str, suffix: str = '') -> re.Pattern:
    """Build a regex that matches `git <subcmd>` while tolerating git's global options."""
    return re.compile(rf'\bgit(?:\s+-[cC]\s+\S+|\s+--\S+=)*\s+{subcmd}\b{suffix}')


GIT_COMMIT_RE = git_cmd_re('commit')
GIT_PUSH_RE = git_cmd_re('push')
GIT_CHERRY_PICK_RE = git_cmd_re('cherry-pick')
GIT_MERGE_RE = git_cmd_re('merge', r'(?!-)')
GIT_REBASE_RE = git_cmd_re('rebase')

GH_PR_ACTIONS = [
    {'re': re.compile(r'\bgh\s+pr\s+create\b'), 'action': 'created', 'op': 'pr_create'},
    {'re': re.compile(r'\bgh\s+pr\s+edit\b'), 'action': 'edited', 'op': 'pr_edit'},
    {'re': re.compile(r'\bgh\s+pr\s+merge\b'), 'action': 'merged', 'op': 'pr_merge'},
    {'re': re.compile(r'\bgh\s+pr\s+comment\b'), 'action': 'commented', 'op': 'pr_comment'},
    {'re': re.compile(r'\bgh\s+pr\s+close\b'), 'action': 'closed', 'op': 'pr_close'},
    {'re': re.compile(r'\bgh\s+pr\s+ready\b'), 'action': 'ready', 'op': 'pr_ready'},
]


@dataclass
class PrInfo:
    pr_number: int
    pr_url: str
    pr_repository: str


def parse_pr_url(url: str) -> Optional[PrInfo]:
    """Parse PR info from a GitHub PR URL."""
    match = re.search(r'https://github.com/([^/]+/[^/]+)/pull/(\d+)', url)
    if match:
        return PrInfo(
            pr_number=int(match.group(2)),
            pr_url=url,
            pr_repository=match.group(1),
        )
    return None


def find_pr_in_stdout(stdout: str) -> Optional[PrInfo]:
    """Find a GitHub PR URL embedded in stdout and parse it."""
    m = re.search(r'https://github.com/[^/\s]+/[^/\s]+/pull/\d+', stdout)
    return parse_pr_url(m.group(0)) if m else None


def parse_git_commit_id(stdout: str) -> Optional[str]:
    """Parse git commit SHA from output."""
    # git commit output: [branch abc1234] message
    match = re.search(r'\[[\w./-]+(?: \(root-commit\))? ([0-9a-f]+)\]', stdout)
    return match.group(1) if match else None


def parse_git_push_branch(output: str) -> Optional[str]:
    """Parse branch name from git push output."""
    match = re.search(r'^\s*[+\-*!= ]?\s*(?:\[new branch\]|\S+\.\.+\S+)\s+\S+\s*->\s*(\S+)', output, re.MULTILINE)
    return match.group(1) if match else None


def parse_pr_number_from_text(stdout: str) -> Optional[int]:
    """Extract PR number from text."""
    match = re.search(r'[Pp]ull request (?:\S+#)?#?(\d+)', stdout)
    return int(match.group(1)) if match else None


def parse_ref_from_command(command: str, verb: str) -> Optional[str]:
    """Extract target ref from git merge/rebase command."""
    pattern = git_cmd_re(verb)
    match = pattern.search(command)
    if not match:
        return None
    after = command[match.end():]
    for t in after.strip().split():
        if t.startswith('&|;><'):
            break
        if t.startswith('-'):
            continue
        return t
    return None


def detect_git_operation(
    command: str,
    output: str,
) -> Dict[str, Any]:
    """Scan command + output for git operations."""
    result = {}

    is_cherry_pick = GIT_CHERRY_PICK_RE.search(command) is not None
    if GIT_COMMIT_RE.search(command) or is_cherry_pick:
        sha = parse_git_commit_id(output)
        if sha:
            result['commit'] = {
                'sha': sha[:6],
                'kind': 'cherry-picked' if is_cherry_pick else ('amended' if '--amend' in command else 'committed'),
            }

    if GIT_PUSH_RE.search(command):
        branch = parse_git_push_branch(output)
        if branch:
            result['push'] = {'branch': branch}

    if GIT_MERGE_RE.search(command) and ('Fast-forward' in output or 'Merge made by' in output):
        ref = parse_ref_from_command(command, 'merge')
        if ref:
            result['branch'] = {'ref': ref, 'action': 'merged'}

    if GIT_REBASE_RE.search(command) and 'Successfully rebased' in output:
        ref = parse_ref_from_command(command, 'rebase')
        if ref:
            result['branch'] = {'ref': ref, 'action': 'rebased'}

    for action_def in GH_PR_ACTIONS:
        if action_def['re'].search(command):
            pr = find_pr_in_stdout(output)
            if pr:
                result['pr'] = {'number': pr.pr_number, 'url': pr.pr_url, 'action': action_def['action']}
            else:
                num = parse_pr_number_from_text(output)
                if num:
                    result['pr'] = {'number': num, 'action': action_def['action']}
            break

    return result


def track_git_operations(
    command: str,
    exit_code: int,
    stdout: str = "",
) -> None:
    """Track git operations for analytics."""
    if exit_code != 0:
        return

    # This function would integrate with analytics in a full implementation
    # For now, just detect and return info
    return detect_git_operation(command, stdout or "")


__all__ = [
    'detect_git_operation',
    'track_git_operations',
    'parse_git_commit_id',
    'find_pr_in_stdout',
    'PrInfo',
    'CommitKind',
    'BranchAction',
    'PrAction',
]