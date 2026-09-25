# Real-script companion: worktree, tool gate, WAL, non-vacuous tests

This is the runnable companion to the day-05 LinkedIn video. It demonstrates where an instruction file stops and executable enforcement begins. It is a narrow example, not a complete security sandbox or a claim that every Claude Code route has been tested.

## The boundary chain

1. A trusted launcher runs [prepare_worktree.sh](prepare_worktree.sh), which creates a fresh linked Git worktree. The agent does not choose the allowed root.
2. The launcher sets AGENT_ALLOWED_ROOT to that root and places [claude_pretool_guard.py](claude_pretool_guard.py) outside the worktree. On covered Claude Code PreToolUse events, it allows read tools, allows Write/Edit only when the resolved target stays inside the root, and exits **2** for an unreviewed route. It denies arbitrary Bash/PowerShell commands because regex inspection of a command string is not OS confinement.
3. [claude_posttool_wal.py](claude_posttool_wal.py) appends a small receipt after a successful or failed write. The trusted runner sets AGENT_RUN_ID and AGENT_WAL_PATH to an external, agent-inaccessible location. A post-tool hook records an action; it cannot reverse it.
4. Trusted CI runs the tests itself from the assigned worktree and writes reports outside the agent's authority. [verify_evidence.py](verify_evidence.py) rejects zero executed tests, normal-suite failures, a deliberate fault that survives, stale reports, and missing WAL receipts relative to the runner's expected successful write-tool IDs. The deliberate fault must target a consequential project invariant.

Claude Code's [hook reference](https://code.claude.com/docs/en/hooks) documents PreToolUse blocking and exit code 2. It also says command hooks that cannot start or time out may let the call proceed. For a hard boundary, use managed hook deployment, test a deny canary on the actual runtime, and place sensitive files/credentials behind OS permissions or a sandbox the agent cannot change. A hook is a useful interceptor, not the only control. [Git worktree docs](https://git-scm.com/docs/git-worktree) explain checkout isolation; a worktree is not itself a security sandbox.

## Example wiring

The exact command paths are deployment-specific. Put hook files and policy settings outside the agent-writable checkout or in managed policy. This is a template; check registration and timeout behavior on the installed version before relying on it:

~~~json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{"type": "command", "command": "python3 /trusted-control/claude_pretool_guard.py", "timeout": 5}]
    }],
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{"type": "command", "command": "python3 /trusted-control/claude_posttool_wal.py", "timeout": 5}]
    }],
    "PostToolUseFailure": [{
      "matcher": "Write|Edit",
      "hooks": [{"type": "command", "command": "python3 /trusted-control/claude_posttool_wal.py", "timeout": 5}]
    }]
  }
}
~~~

The policy must also review other mutation routes, including MCP tools and shell, or deny them. If the hook has a missing path, times out, or is not loaded in a cloud/hosted surface, the script never gets to return exit 2. Scoped credentials and independent CI remain necessary.

## Tests run here

[test_harness.py](test_harness.py) exercises in-root and out-of-root writes, default shell denial, missing configuration, WAL writing, zero-test rejection, a surviving fault, stale reports and missing receipts. It passed locally on 2026-09-24. [run_negative_control.sh](run_negative_control.sh) ran a real two-test pytest suite against [demo_policy.py](demo_policy.py), then deliberately changed the zero-test rule through an environment-controlled mutant: normal suite **2 passed**, mutant suite **1 failed / 1 passed**. The runner writes `demo-reports/normal.xml` and `demo-reports/deliberate-fault.xml` locally. Raw reports are excluded from this repository because pytest can include machine names and absolute local paths in failure output. Run the command yourself to inspect fresh reports.

The shell worktree launcher created a real temporary Git worktree in a disposable fixture. Its cleanup was rejected by the host's automatic approval review as “blocked by policy”; the fixture was left in the OS Temp directory. This is not a deployed Claude Code hook test. The first real gate test still needs a harmless denied write in the installed Claude Code runtime, followed by trace and actual-file readback.

## Why this is non-vacuous

[pytest](https://docs.pytest.org/en/stable/reference/exit-codes.html) documents an exit code for no tests collected. [Mutation testing](https://stryker-mutator.io/docs/) checks whether an intentional behavioral fault turns tests red. A green test process alone is insufficient: verify the selected test count, report freshness, expected worktree, a relevant killed mutant and the independent business outcome. The demo mutant only proves the example gate catches its own chosen fault.
