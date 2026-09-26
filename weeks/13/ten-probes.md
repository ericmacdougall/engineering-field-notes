# Ten bounded Week 13 probes

For each authorized staging experiment, capture the intent ID, source version, protected operation journal, target-state readbacks, agent-visible summary, forbidden-action assertion and owner decision. These are experiments to run; the local fixture only simulates their branches.

1. Lose the reply before the placement service accepts. Keep the first effect `UNKNOWN` until an authoritative lookup resolves it; do not issue a fresh move from a timeout alone.
2. Lose the reply after acceptance. Recover the original operation ID and accepted receipt; do not mistake that receipt for customer-visible convergence.
3. Resume with only “move failed” prose. Require the protected journal or an owner route before any new move or compensation.
4. Resume from a versioned operation record. Check that the original intent and precondition are preserved across session and worker boundaries.
5. Deliver the same operation ID twice. Inspect the service's real deduplication scope and retention window; assert one accepted effect without claiming global exactly-once semantics.
6. Delay a child mapping/route update past the parent timeout. Preserve partial states and refuse a green result while serving is draining.
7. Deliver late success after the orchestrator declares failure. Reconcile against the same operation, then inspect all target branches before closing.
8. Change the placement version concurrently. Block automatic undo and route compensation to the owner with a fresh precondition.
9. Lose child-message correlation. Require case and operation identity on each relevant message and trace link; a “success” without binding is not proof for this case.
10. Withhold one target readback. Keep the effect unknown even when the model's explanation and other dashboards look correct.

In this repository, `test_fixture.py` runs ten synthetic cases with these labels. It does not execute a cloud control plane, durable queue, real agent, or customer traffic probe. The `W13_TEST_MUTANT` negative control proves the tests reject one unsafe second-move branch.
