# Week 10 — The attention drift bubble

**Article:** [The attention drift bubble](https://ericmacdougall.com/journal/the-attention-drift-bubble/) · link becomes live after the separate public film, companion and site readbacks.  
**Overview film:** [Why AI-to-AI Workflows Lose the Original Decision](https://www.youtube.com/watch?v=2n68fHS8v6U) · Public YouTube watch page, with English captions and transcript.

The [field note](https://ericmacdougall.com/journal/the-attention-drift-bubble/) argues that a chain of AI-authored plans, summaries and tasks can lose a decisive source condition without any single step inventing a fact. This folder contains a **synthetic** decision-packet checker that asks whether a downstream packet and acknowledgment preserve material clauses from a protected source record. Its `PASS` means packet fidelity in this toy fixture only; `execution_authorized` is always `false`.

Run from this folder:

```sh
python handoff_contract.py examples/source.json examples/packet.json examples/ack.json 2026-09-25
python -m unittest discover -s tests -p test_handoff_contract.py -v
```

The final argument pins the illustrative as-of date. Without it, the checker uses today's date; after the fixture's `2026-12-01` expiry, an old packet should fail. The SHA-256 digest binds the packet to the supplied source bytes only when the source is fetched from a protected authority. The example cannot authenticate a person, demonstrate that a model understood the clause, authorize a real action or verify target state.

The [ten probes](ten-probes.md) move from deterministic clause preservation to a consent-safe real workflow with independent source and target observations. The local seven-test suite includes missing, altered, invented, wrong-tenant, expired and unacknowledged-clause cases. The September 25 local readback recorded 7/7 passing; no model or external action was exercised.

**Release state:** staged locally; no Public GitHub readback is claimed here. Keep this notice current when the companion is published.
