#!/usr/bin/env python3
"""Checks for the git write guard. Run: python3 test_guard.py"""
import sys
from guard import check

MUST_BLOCK = [
    "git commit -m 'x'",
    "git push",
    "git push origin main",
    "git add -A",
    "git rm file",
    "git merge main",
    "git rebase -i main",
    "git reset --hard origin/main",
    "git checkout -b feature",
    "git switch main",
    "git restore .",
    "git cherry-pick abc",
    "git revert HEAD",
    "git clean -fd",
    "git pull",
    "git fetch origin",
    "git clone https://example.com/r.git",
    "git init",
    "git gc",
    "git update-ref refs/heads/main abc",
    "git format-patch HEAD~1",
    "git stash push",
    "git stash pop",
    "git stash",
    "git branch -D old",
    "git branch newbranch",
    "git branch --contains HEAD",
    "git tag v1.0",
    "git tag -d v1.0",
    "git remote add origin url",
    "git remote set-url origin url",
    "git config user.email a@b.c",
    "git config --global user.name x",
    "git worktree add ../w",
    "git worktree prune",
    "git submodule update --init",
    "git bisect start",
    "git notes add -m x",
    "git reflog expire --all",
    # invocation forms
    "/usr/bin/git push",
    "git -C /other/repo commit -m x",
    "git -c user.name=x commit -m y",
    "git --git-dir=/r/.git --work-tree=/r push",
    "git --no-pager commit -m x",
    "git-push",
    "GIT_DIR=.git git commit -m x",
    # chaining and nesting
    "git status && git push",
    "git status; git commit -m x",
    "true || git push",
    "cd /tmp && git push",
    "bash -c 'git push'",
    "sh -c \"git commit -m x\"",
    "echo a | xargs git push",
    "find . -name '*.py' -exec git add {} ;",
    # unknown subcommand fails closed
    "git frobnicate",
    "git ci -m x",
    # gh
    "gh pr create --title x",
    "gh pr merge 3",
    "gh release create v1",
    "gh repo delete owner/r",
    "gh issue comment 1 -b x",
    "gh api -X POST /repos/o/r/issues",
    "gh api repos/o/r/issues -f title=x",
]

MUST_ALLOW = [
    "git status",
    "git status --short",
    "git log --oneline -5",
    "git diff HEAD",
    "git show abc123",
    "git branch",
    "git branch -a",
    "git tag -l",
    "git tag -l v*",
    "git remote -v",
    "git remote show origin",
    "git config --get user.email",
    "git config user.email",
    "git stash list",
    "git worktree list",
    "git notes",
    "git submodule status",
    "git rev-parse --is-inside-work-tree",
    "git ls-files",
    "git blame file.py",
    "git -C /other/repo status",
    "git --no-pager log",
    "git status && git diff",
    "gh pr view 3",
    "gh pr list",
    "gh run list",
    "gh api repos/o/r",
    # non-git commands must be untouched
    "ls -la",
    "python3 -m pytest",
    "echo hello",
    # git named as data, not invoked
    "echo 'git push'",
    "grep -r 'git commit' docs/",
    "cat > f.md <<'EOF'\nRun git push to publish.\ngit commit -m x\nEOF",
    "cat > AGENTS.md <<'MD'\n- Never run git commit or git push.\nMD",
]


def main():
    failures = []
    for command in MUST_BLOCK:
        if check(command) is None:
            failures.append("NOT BLOCKED: %s" % command)
    for command in MUST_ALLOW:
        reason = check(command)
        if reason is not None:
            failures.append("WRONGLY BLOCKED: %s  (%s)" % (command, reason))
    for line in failures:
        print(line)
    total = len(MUST_BLOCK) + len(MUST_ALLOW)
    print("\n%d/%d passed" % (total - len(failures), total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
