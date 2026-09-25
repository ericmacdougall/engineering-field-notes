# Commerce invariant harness

This companion provides a local SQLite and fake-provider acceptance contract for a one-unit inventory race and a lost payment acknowledgment. It deliberately introduces broken variants and requires the contract to reject them.

These are illustrative fixtures, not evidence of real PostgreSQL, Stripe, or deployed-agent behavior. Run `python examples/commerce-harness/run_contract.py` after installing pytest; keep protected acceptance tests and provider credentials outside the agent worktree in a real system.
