# Week 06: ten discriminating route-loss probes

These are **proposed** tests for a disposable queue and synthetic cases. They are not observations of Eric's providers or a real security operation. Name the expected downstream case owner, state and permissible effect before each injection.

1. Return an explicit simulated refusal for an authorized synthetic report. The case must remain open with the policy owner and original evidence; no alternate provider is dispatched.
2. Return a completed-looking classification without the required evidence reference. The adapter must mark it uncertain rather than complete.
3. Return an unknown upstream status code. Require a visible unclassified failure and an open case, never an empty successful result.
4. Cut a test connection after dispatch and before response. Reconcile the provider request ID and queue state before retrying; do not invent an answer.
5. Revoke a test credential. Bound retries, alert the operator and preserve the unfinished case.
6. Retire a test model route while work is queued. Recheck route availability at dispatch and record a separately reviewed alternate or human handoff.
7. Change a synthetic case from public to restricted data. The public-only fallback must be rejected despite being otherwise available.
8. Return a structurally valid answer requesting an action beyond the current actor's scope. The final application check must block it, independent of model confidence.
9. Change registry or provider-policy version between two attempts. Each attempt's decision receipt must identify which version governed it.
10. Restore a test route and replay unresolved work. Read back every final case state, confirm no silent closure or duplicate external action, and measure human rescue time.

The [route-registry and handoff template](route-registry-and-handoff-template.md) records who owns each boundary. The local Python [rehearsal](route_loss.py) covers a narrower, effect-free subset; a production adapter additionally needs authenticated provider and ticket APIs, current policy review, idempotent action identity, bounded retries, protected evidence and independent state readback.
