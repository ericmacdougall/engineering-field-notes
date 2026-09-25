#!/usr/bin/env python3
"""Conservative Claude Code PreToolUse hook example.

The trusted runner sets AGENT_ALLOWED_ROOT. Keep this script outside that
worktree. Hook coverage and startup must be tested on the deployed surface;
use OS confinement and scoped credentials for a stronger boundary.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

READ_ONLY = {"Read", "Glob", "Grep"}
FILE_WRITES = {"Write", "Edit"}

def deny(reason: str) -> int:
    print(f"Agent guard denied: {reason}", file=sys.stderr)
    return 2  # Claude Code: PreToolUse exit 2 blocks the call.

def main() -> int:
    raw_root = os.environ.get("AGENT_ALLOWED_ROOT")
    if not raw_root:
        return deny("AGENT_ALLOWED_ROOT is missing")
    try:
        root = Path(raw_root).resolve(strict=True)
        event = json.load(sys.stdin)
    except (OSError, ValueError, TypeError) as exc:
        return deny(f"bad root or event: {type(exc).__name__}")
    if not root.is_dir() or not isinstance(event, dict):
        return deny("invalid root or event")
    tool = event.get("tool_name")
    if tool in READ_ONLY:
        return 0  # Normal platform permissions still apply.
    if tool in FILE_WRITES:
        tool_input = event.get("tool_input")
        if not isinstance(tool_input, dict) or not isinstance(tool_input.get("file_path"), str):
            return deny("missing absolute file_path")
        target = Path(tool_input["file_path"])
        if not target.is_absolute():
            return deny("relative target path")
        try:
            resolved = target.resolve(strict=False)
        except (OSError, RuntimeError):
            return deny("unresolvable target")
        if not resolved.is_relative_to(root):
            return deny("write escapes assigned worktree")
        return 0
    # Parsing an arbitrary Bash/PowerShell string is not confinement.
    # Grant shell only through a separate OS sandbox and reviewed adapter.
    return deny(f"tool {tool!r} has no reviewed route")

if __name__ == "__main__":
    raise SystemExit(main())
