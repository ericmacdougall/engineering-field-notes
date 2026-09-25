#!/usr/bin/env python3
"""Append a small action receipt after a Claude Code tool call.

PostToolUse cannot undo the action. CI reconciles these receipts against a
trusted platform trace; the WAL alone is not proof of complete coverage.
"""
from __future__ import annotations
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

def main() -> int:
    raw = os.environ.get("AGENT_WAL_PATH")
    run_id = os.environ.get("AGENT_RUN_ID")
    if not raw or not run_id:
        print("WAL path or run ID missing", file=sys.stderr)
        return 2
    try:
        event = json.load(sys.stdin)
        if not isinstance(event, dict) or not event.get("tool_use_id"):
            raise ValueError("invalid event or tool_use_id")
        receipt = {
            "at_utc": datetime.now(timezone.utc).isoformat(),
            "run_id": run_id,
            "event": event.get("hook_event_name"),
            "tool_name": event.get("tool_name"),
            "tool_use_id": event["tool_use_id"],
            "file_path": (event.get("tool_input") or {}).get("file_path"),
        }
        path = Path(raw)
        if not path.parent.is_dir():
            raise ValueError("WAL parent does not exist")
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(receipt, ensure_ascii=False) + "\n")
    except (OSError, ValueError, TypeError) as exc:
        print(f"WAL write failed: {type(exc).__name__}", file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
