# Ten bounded Week 14 probes

For each probe, record the source record, owner-labeled expected state, actual state, intervention, operator time and target readback. A local fixture establishes only local behavior. Do not invent results for a real system.

1. Valid historical approval: provenance and current policy agree; require ACTIVE.
2. Revocation after approval: a legacy true flag survives, but require INACTIVE.
3. Ambiguous legacy Boolean: no source event; require UNKNOWN and owner route.
4. Missing policy version: approval event exists but its governing rule is unknown; require UNKNOWN.
5. Second change: add temporary approval; inspect controller, worker, export and notification contracts, then test expiry.
6. Resume from prose: terminate the first session and supply only “customer approved”; forbid a grant without current source readback.
7. Resume from versioned record: supply source ID, version and effective time; read current source and classify correctly.
8. Stale handoff: revoke after the note; require stale-note detection and hold.
9. Follow-on cost: compare changed files, contracts, review cycles, regression failures and target readbacks for the same second change across two designs. Log measured values only.
10. Build/buy/stop: enter actual license, operating, support, integration and diverted-role hours. Make the owner and exit criterion explicit. If inputs are unavailable, leave decision UNKNOWN.

The current test suite exercises 1–4, 6–8 and pieces of 5; it does **not** execute 9–10 or a real customer workflow. The latter remain experimental designs.
