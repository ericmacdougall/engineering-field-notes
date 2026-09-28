"""Uninstalled Claude Code PreToolUse example for one fixture MCP operation.

The output shape follows the official Sep 25 2026 docs. This adapter is only
unit-tested on fixture JSON. Do not claim real-host coverage without installing
it in a harmless environment and probing direct/delegated/alternate routes.
"""
from __future__ import annotations

import json
import sys

from policy import decision


def respond(raw: str) -> dict:
    try:
        event = json.loads(raw)
        if not isinstance(event, dict) or event.get("hook_event_name") != "PreToolUse":
            raise ValueError("wrong event")
        if event.get("tool_name") != "mcp__fixture__mutate":
            raise ValueError("unmatched tool")
        tool_input = event.get("tool_input")
    except (ValueError, json.JSONDecodeError):
        tool_input = None
    result = decision(tool_input)
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                   "permissionDecision": "allow" if result["allowed"] else "deny",
                                   "permissionDecisionReason": result["reason"]}}


if __name__ == "__main__":
    print(json.dumps(respond(sys.stdin.read(4097)), sort_keys=True))
