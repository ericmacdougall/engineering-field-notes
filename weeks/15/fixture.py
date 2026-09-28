"""Disposable loopback target for Week 15 editorial experiments.

The fixture tokens are public test strings. Never expose this server to a
network or use it as a production authorization implementation.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


TOKENS = {"fixture-stage-token": "staging", "fixture-prod-token": "production"}


class State:
    def __init__(self, mutant_auth: bool = False, hide_receipts: bool = False):
        self.lock = threading.RLock()
        self.tenants = {"staging": "v0", "production": "v0"}
        self.receipts: list[dict] = []
        self.operations: dict[str, dict] = {}
        self.mutant_auth = mutant_auth
        self.hide_receipts = hide_receipts

    def snapshot(self) -> dict:
        with self.lock:
            raw = json.dumps(self.tenants, sort_keys=True).encode()
            return {"tenants": dict(self.tenants), "sha256": hashlib.sha256(raw).hexdigest()}

    def mutate(self, token: str, tenant: str, value: str, op_id: str) -> dict:
        with self.lock:
            if op_id in self.operations:
                return dict(self.operations[op_id])
            principal = TOKENS.get(token)
            if principal is None:
                return {"status": "denied", "reason": "unknown principal", "op_id": op_id}
            allowed = principal == tenant or self.mutant_auth
            if not allowed:
                result = {"status": "denied", "reason": "cross-tenant mutation", "op_id": op_id,
                          "principal": principal, "tenant": tenant}
                self.operations[op_id] = result
                return dict(result)
            self.tenants[tenant] = value
            receipt = {"sequence": len(self.receipts) + 1, "op_id": op_id,
                       "principal": principal, "tenant": tenant, "value": value}
            self.receipts.append(receipt)
            result = {"status": "committed", "receipt": receipt, "op_id": op_id}
            self.operations[op_id] = result
            return dict(result)


def handler_for(state: State):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):  # Never emit fixture tokens in local logs.
            return

        def send_json(self, status: int, body: dict | list):
            blob = json.dumps(body, sort_keys=True).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(blob)))
            self.end_headers()
            self.wfile.write(blob)

        def do_GET(self):
            if self.path == "/state":
                self.send_json(200, state.snapshot())
            elif self.path == "/receipts":
                with state.lock:
                    self.send_json(200, [] if state.hide_receipts else list(state.receipts))
            elif self.path.startswith("/operations/"):
                op_id = self.path.removeprefix("/operations/")
                with state.lock:
                    self.send_json(200 if op_id in state.operations else 404,
                                   state.operations.get(op_id, {"status": "unknown", "op_id": op_id}))
            else:
                self.send_json(404, {"error": "unknown route"})

        def do_POST(self):
            if self.path != "/mutate":
                self.send_json(404, {"error": "unknown route"})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size > 4096 or size < 2:
                    raise ValueError("bad size")
                body = json.loads(self.rfile.read(size))
                if not isinstance(body, dict) or any(not isinstance(body.get(k), str)
                                                      for k in ("tenant", "value", "op_id")):
                    raise ValueError("bad payload")
            except (ValueError, json.JSONDecodeError):
                self.send_json(400, {"error": "bad request"})
                return
            token = self.headers.get("Authorization", "").removeprefix("Bearer ")
            result = state.mutate(token, body["tenant"], body["value"], body["op_id"])
            if body.get("drop_ack") and result["status"] == "committed":
                self.close_connection = True
                self.connection.shutdown(2)
                return
            self.send_json(200 if result["status"] == "committed" else 403, result)

    return Handler


@contextmanager
def target(mutant_auth: bool | None = None, hide_receipts: bool = False):
    state = State(mutant_auth=(os.getenv("W15_MUTANT_AUTH") == "1") if mutant_auth is None else mutant_auth,
                  hide_receipts=hide_receipts)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(state))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", state
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
