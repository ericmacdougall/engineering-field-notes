"""Boundary tests for the companion hook/CI examples."""
from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent

class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "run"
        self.root.mkdir()
        self.env = dict(os.environ, AGENT_ALLOWED_ROOT=str(self.root))
        self.run_start = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()

    def hook(self, tool, tool_input):
        event = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input}
        return subprocess.run(
            [sys.executable, str(HERE / "claude_pretool_guard.py")],
            input=json.dumps(event), text=True, capture_output=True, env=self.env,
        )

    def test_write_inside_worktree_is_left_to_normal_permissions(self):
        self.assertEqual(self.hook("Write", {"file_path": str(self.root / "src" / "a.py")}).returncode, 0)

    def test_write_outside_worktree_is_blocked(self):
        self.assertEqual(self.hook("Edit", {"file_path": str(self.base / "outside.py")}).returncode, 2)

    def test_shell_is_blocked_without_a_sandboxed_adapter(self):
        self.assertEqual(self.hook("Bash", {"command": "echo hello"}).returncode, 2)

    def test_missing_root_fails_closed_when_hook_runs(self):
        env = dict(self.env)
        env.pop("AGENT_ALLOWED_ROOT")
        run = subprocess.run(
            [sys.executable, str(HERE / "claude_pretool_guard.py")],
            input='{"tool_name":"Write","tool_input":{"file_path":"x"}}',
            text=True, capture_output=True, env=env,
        )
        self.assertEqual(run.returncode, 2)

    def test_posttool_appends_a_reconcilable_receipt(self):
        wal = self.base / "wal.jsonl"
        env = dict(self.env, AGENT_WAL_PATH=str(wal), AGENT_RUN_ID="r1")
        event = {"hook_event_name": "PostToolUse", "tool_name": "Write",
                 "tool_use_id": "tool-1", "tool_input": {"file_path": str(self.root / "a.py")}}
        run = subprocess.run(
            [sys.executable, str(HERE / "claude_posttool_wal.py")],
            input=json.dumps(event), text=True, capture_output=True, env=env,
        )
        self.assertEqual(run.returncode, 0)
        receipt = json.loads(wal.read_text(encoding="utf-8").strip())
        self.assertEqual((receipt["run_id"], receipt["tool_use_id"]), ("r1", "tool-1"))

    def test_ci_rejects_zero_tests_and_surviving_fault(self):
        normal = self.base / "normal.xml"
        fault = self.base / "fault.xml"
        wal = self.base / "wal.jsonl"
        expected = self.base / "expected.json"
        expected.write_text('["tool-1"]', encoding="utf-8")
        wal.write_text(json.dumps({"run_id": "r1", "tool_use_id": "tool-1"}) + "\n", encoding="utf-8")
        normal.write_text('<testsuite tests="0" failures="0" skipped="0"/>', encoding="utf-8")
        fault.write_text('<testsuite tests="1" failures="1" skipped="0"/>', encoding="utf-8")
        self.assertEqual(self.verify(normal, fault, wal, expected), 1)
        normal.write_text('<testsuite tests="1" failures="0" skipped="0"/>', encoding="utf-8")
        fault.write_text('<testsuite tests="1" failures="0" skipped="0"/>', encoding="utf-8")
        self.assertEqual(self.verify(normal, fault, wal, expected), 1)
        fault.write_text('<testsuite tests="1" failures="1" skipped="0"/>', encoding="utf-8")
        self.assertEqual(self.verify(normal, fault, wal, expected), 0)
        wal.write_text("", encoding="utf-8")
        self.assertEqual(self.verify(normal, fault, wal, expected), 1)
        wal.write_text(json.dumps({"run_id": "r1", "tool_use_id": "tool-1"}) + "\n", encoding="utf-8")
        future = (datetime.now(timezone.utc) + timedelta(minutes=1)).isoformat()
        self.assertEqual(self.verify(normal, fault, wal, expected, run_start=future), 1)

    def verify(self, normal, fault, wal, expected, run_start=None):
        return subprocess.run(
            [sys.executable, str(HERE / "verify_evidence.py"),
             "--normal", str(normal), "--deliberate-fault", str(fault),
             "--wal", str(wal), "--expected-ids", str(expected), "--run-id", "r1",
             "--run-start-utc", run_start or self.run_start],
            text=True, capture_output=True,
        ).returncode

if __name__ == "__main__":
    unittest.main(verbosity=2)
