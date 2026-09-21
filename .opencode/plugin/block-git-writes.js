/**
 * Denies any git or gh write operation attempted through the bash tool.
 *
 * The policy itself lives in tools/git-write-guard/guard.py so that this
 * plugin and the Claude Code PreToolUse hook cannot drift apart. Commands that
 * do not mention git or gh never reach the guard, so the cost is only paid on
 * the commands that could matter.
 *
 * Fails closed: if the guard cannot be run, a git-mentioning command is denied.
 *
 * OpenCode reads plugins from .opencode/plugin/ and .opencode/plugins/ alike.
 */

const GUARD = "tools/git-write-guard/guard.py"
const MENTIONS_GIT = /(^|[^\w.-])(git|gh)([^\w-]|$)/

export const BlockGitWrites = async ({ $, directory, worktree }) => {
  const guard = `${worktree || directory}/${GUARD}`

  return {
    "tool.execute.before": async (input, output) => {
      if (input?.tool !== "bash") return

      const command = output?.args?.command
      if (typeof command !== "string") return
      if (!MENTIONS_GIT.test(command)) return

      const result = await $`python3 ${guard} --check ${command}`.nothrow().quiet()
      if (result.exitCode === 0) return

      const reason = result.stderr.toString().trim()
      throw new Error(
        reason ||
          `Blocked: the git write guard at ${GUARD} could not be run, so this ` +
            `git command is refused. AGENTS.md forbids agents from performing ` +
            `git write operations.`,
      )
    },
  }
}
