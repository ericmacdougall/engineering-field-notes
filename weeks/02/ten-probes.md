# Ten probes before a migration architecture hardens

Run only in a disposable copy with synthetic or properly authorized historical data. These are proposed experiments, not evidence of a live migration.

| # | Probe | Observation that matters |
|---:|---|---|
| 1 | Sample records from every old policy period, including missing approval evidence. | Cohort size and provenance gaps. |
| 2 | Have the policy owner label representative outcomes before model review. | Explicit expected state and exception owner. |
| 3 | Run competing migration rules on the same sample. | Which rows differ from owner labels and why. |
| 4 | Include approval followed by revocation in a different source. | Final authority remains revoked. |
| 5 | Attempt a transition from a role without authority. | Persisted state and audit history remain unchanged. |
| 6 | Commit a batch write, lose the checkpoint, then restart. | No duplicate approval or audit effect. |
| 7 | Change a legacy identifier without changing the business entity. | Stable identity still prevents duplicate effects. |
| 8 | Remove an audit source during import. | Stop or quarantine according to declared policy. |
| 9 | Start a fresh agent with only the durable decision packet. | It predicts the old failure and keeps the accepted behavior. |
| 10 | Deliberately mutate one policy or replay guard. | The protected release test turns red. |

If the real system offers a VM or computer-use harness, record action, version, route, permission, and authoritative readback for each probe. A successful UI screen or a model-written explanation is not the measurement.
