#!/usr/bin/env python3
"""Deny git and gh operations that write.

One policy, two callers:
  guard.py --claude          Claude Code PreToolUse hook; hook JSON on stdin.
  guard.py --check "<cmd>"   OpenCode plugin; command as an argument.

Exit 0 = allowed. Exit 2 = denied, reason on stderr. The --claude form also
prints the deny decision as JSON on stdout, which is what Claude Code reads.

Policy is an allowlist: anything not positively recognised as read-only is
denied. A new or unknown git subcommand therefore fails closed.

This file is tooling, not application code, so the app's layering and Object
Calisthenics rules in AGENTS.md do not apply to it.
"""

import json
import re
import shlex
import sys

# Subcommands that cannot modify a repository under any arguments.
READ_ONLY = {
    "blame", "cat-file", "check-attr", "check-ignore", "count-objects",
    "describe", "diff", "diff-files", "diff-index", "diff-tree", "for-each-ref",
    "grep", "help", "log", "ls-files", "ls-remote", "ls-tree", "merge-base",
    "name-rev", "rev-list", "rev-parse", "shortlog", "show", "show-ref",
    "status", "var", "verify-commit", "verify-tag", "version", "whatchanged",
}

# Subcommands that read OR write depending on their arguments; each has its own
# predicate below, because "which arguments are safe" differs per subcommand.
BRANCH_READ_FLAGS = {"-a", "--all", "-r", "--remotes", "-v", "-vv", "--verbose",
                     "--list", "--show-current", "--color", "--no-color"}

CONFIG_WRITE_FLAGS = {"--unset", "--unset-all", "--add", "--replace-all",
                      "--edit", "-e", "--rename-section", "--remove-section"}

# git's own options that sit before the subcommand and consume the next token.
GIT_OPTIONS_WITH_VALUE = {"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                          "--exec-path", "--super-prefix"}

# gh subcommands that only read. Checked as the second word, e.g. "gh pr view".
GH_READ_VERBS = {"view", "list", "diff", "status", "checks", "watch", "browse"}

# Tokens after which the next word is a new command, so a `git` there is a real
# invocation rather than text inside an argument.
COMMAND_STARTERS = {
    "&&", "||", ";", "|", "|&", "&", "(", ")", "{", "}", "\n",
    "env", "command", "exec", "time", "sudo", "nohup", "nice", "timeout",
    "xargs", "then", "else", "elif", "do", "while", "until", "if",
    "-exec", "-execdir", "-c",
}

ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
HEREDOC = re.compile(r"<<-?\s*[\"']?([A-Za-z_][A-Za-z0-9_]*)[\"']?")


def strip_heredocs(command):
    """Remove heredoc bodies so documentation text is not read as commands."""
    lines = command.split("\n")
    kept, skip_until = [], None
    for line in lines:
        if skip_until is not None:
            if line.strip() == skip_until:
                skip_until = None
            continue
        kept.append(line)
        match = HEREDOC.search(line)
        if match:
            skip_until = match.group(1)
    return "\n".join(kept)


def tokenize(command):
    """Split into shell tokens, keeping operators. Returns None if unparseable."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        return None


def is_command_position(tokens, index):
    if index == 0:
        return True
    previous = tokens[index - 1]
    return previous in COMMAND_STARTERS or bool(ASSIGNMENT.match(previous))


def program_name(token):
    return token.rsplit("/", 1)[-1]


def subcommand_after(tokens, index):
    """The git subcommand following the `git` token at index, skipping options."""
    position = index + 1
    while position < len(tokens):
        token = tokens[position]
        if not token.startswith("-"):
            return token, tokens[position + 1:]
        if token in GIT_OPTIONS_WITH_VALUE:
            position += 2
            continue
        position += 1
    return None, []


def deny_git(subcommand, arguments):
    if subcommand is None:
        return None
    if subcommand in READ_ONLY:
        return None
    if subcommand in CONDITIONAL:
        return CONDITIONAL[subcommand](arguments)
    return "git %s is a write operation" % subcommand


def branch_violation(arguments):
    for argument in arguments:
        if not argument.startswith("-"):
            return "git branch %s creates or moves a branch" % argument
        if argument.split("=", 1)[0] not in BRANCH_READ_FLAGS:
            return "git branch %s can modify branches" % argument
    return None


def config_violation(arguments):
    for argument in arguments:
        if argument.split("=", 1)[0] in CONFIG_WRITE_FLAGS:
            return "git config %s writes configuration" % argument
    positionals = [a for a in arguments if not a.startswith("-")]
    if len(positionals) >= 2:
        return "git config with a value writes configuration"
    return None


def first_word_rule(subcommand, allowed, allow_bare):
    def violation(arguments):
        if not arguments:
            return None if allow_bare else "git %s alone writes" % subcommand
        if arguments[0] in allowed:
            return None
        return "git %s %s can modify the repository" % (subcommand, arguments[0])
    return violation


CONDITIONAL = {
    "branch": branch_violation,
    "config": config_violation,
    "tag": first_word_rule("tag", {"-l", "--list", "-n"}, True),
    "remote": first_word_rule("remote", {"-v", "--verbose", "show", "get-url"}, True),
    "stash": first_word_rule("stash", {"list", "show"}, False),
    "worktree": first_word_rule("worktree", {"list"}, False),
    "reflog": first_word_rule("reflog", {"show"}, True),
    "notes": first_word_rule("notes", {"list", "show"}, True),
    "submodule": first_word_rule("submodule", {"status", "summary"}, True),
    "bisect": first_word_rule("bisect", {"log"}, False),
}


def deny_gh(tokens, index):
    rest = [token for token in tokens[index + 1:] if not token.startswith("-")]
    if not rest:
        return None
    if rest[0] == "api":
        return deny_gh_api(tokens[index + 1:])
    if len(rest) > 1 and rest[1] in GH_READ_VERBS:
        return None
    return "gh %s is a write operation" % " ".join(rest[:2])


def deny_gh_api(arguments):
    writes = {"-X", "--method", "-f", "--raw-field", "-F", "--field", "--input"}
    for argument in arguments:
        key = argument.split("=", 1)[0]
        if key in writes and not argument.endswith("GET"):
            return "gh api with %s sends a write request" % key
    return None


def check(command):
    """Return a deny reason, or None when the command may run."""
    tokens = tokenize(strip_heredocs(command))
    if tokens is None:
        return quoting_failure(command)
    for index, token in enumerate(tokens):
        reason = check_token(tokens, index, token)
        if reason:
            return reason
    return None


def quoting_failure(command):
    if re.search(r"\bg(it|h)\b", command):
        return "command could not be parsed and mentions git; refusing"
    return None


def check_token(tokens, index, token):
    if " " in token or "\n" in token:
        return check(token) if index and tokens[index - 1] == "-c" else None
    if not is_command_position(tokens, index):
        return None
    name = program_name(token)
    if name == "git":
        return deny_git(*subcommand_after(tokens, index))
    if name.startswith("git-"):
        return deny_git(name[4:], tokens[index + 1:])
    if name == "gh":
        return deny_gh(tokens, index)
    return None


MESSAGE = (
    "Blocked by tools/git-write-guard: %s.\n"
    "AGENTS.md forbids agents from performing git write operations. "
    "Report what you would have run and let the user run it."
)


def run_claude():
    payload = json.load(sys.stdin)
    if payload.get("tool_name") != "Bash":
        return 0
    reason = check(payload.get("tool_input", {}).get("command", ""))
    if reason is None:
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": MESSAGE % reason,
    }}))
    return 0


def run_check(command):
    reason = check(command)
    if reason is None:
        return 0
    sys.stderr.write(MESSAGE % reason)
    return 2


def main(argv):
    if len(argv) > 1 and argv[1] == "--claude":
        return run_claude()
    if len(argv) > 2 and argv[1] == "--check":
        return run_check(argv[2])
    sys.stderr.write(__doc__)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv))
