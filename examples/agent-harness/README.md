# Agent harness

This companion contains a trusted worktree launcher, a narrow Claude Code PreToolUse guard, a PostToolUse WAL receipt, and an independent evidence verifier. See the repository root README for the claim, limits, and test commands.

The scripts are illustrative local controls. A hook is not an OS sandbox. Before depending on it, run a denied canary on the actual installed runtime and verify the filesystem or service state afterward.
