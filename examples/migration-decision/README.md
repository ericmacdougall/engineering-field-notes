# Migration decision contract — Week 02 example

This is an original, runnable **illustration**, not a production access system or an observed client incident. It accompanies the Week 02 argument that two agreeing models cannot infer a missing business policy from a polished UI. The synthetic owner rule distinguishes an evidenced, certified legacy approval (`LEGACY_APPROVED`) from an ambiguous old Boolean (`QUARANTINED`) and a later revoked record (`REVOKED`). A real organization may choose another policy after reviewing its own records and obligations.

From this folder, run `python run_contract.py` with Python 3.11 or newer. It executes two normal contract checks and repeats them with two deliberate faults:

1. `accept_every_true` blindly maps an old Boolean to current `APPROVED`.
2. `new_key_on_retry` changes the audit-event identity on replay after a simulated committed write and lost checkpoint.

The runner succeeds only if it executes both normal contract tests, the normal case stays green, and **both** faults turn red with the same test count. It saves an ignored local receipt in `reports/latest.json`. The protected expectations in `trusted_contract.py` and the database/audit readback are the actual acceptance criteria for this illustration. In an agent deployment they must be kept outside the worker's writable checkout; colocating them here makes the example easy to run, not secure.

Before reusing the approach, sample real historical records, have a policy owner label the expected states, test actual migration and revocation routes in a disposable target environment, inject a real crash/restart seam, and compare authoritative final state and audit events. The example uses in-memory SQLite and synthetic rows; it does not prove any platform hook, real access control, or a live backfill.

The [Week 02 field note](../../weeks/02/README.md) lists the wider ten-experiment plan and the article release gate. The article and overview film have Eric's editorial approval; that approval does not turn this synthetic fixture into a production migration result.
