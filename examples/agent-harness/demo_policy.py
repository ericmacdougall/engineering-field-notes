"""Toy policy only for the negative-control demonstration."""
import os

def release_allowed(executed_tests: int, oracle_ok: bool) -> bool:
    if os.environ.get("AGENT_DELIBERATE_FAULT") == "1":
        # A deliberate mutant: zero executed tests now appear acceptable.
        return executed_tests >= 0 and oracle_ok
    return executed_tests > 0 and oracle_ok
