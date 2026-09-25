# Week 02 — Model consensus is not engineering evidence

<!-- ARTICLE_START -->
**Article:** Eric approved the article and overview film on 2026-09-25. Publication is planned no earlier than 2026-10-12 Pacific time. Add the verified public article URL here and to the root README only after the weekly release gate passes.
<!-- ARTICLE_END -->

## The claim

Two capable models can converge on a polished implementation when both lack the same business history. A working surface is not proof that authority, legacy migration, replay and recovery were decided. The operator needs a causal model that survives future agent sessions; otherwise repair and expansion consume attention. Model debate is best used to produce falsifiable alternatives, not award its own final signoff.

## Companion material

- [Migration decision contract](../../examples/migration-decision/README.md): synthetic legacy approvals, a replay seam, authoritative state/audit readback and two deliberate mutations.
- [Decision packet template](decision-packet-template.md): concise policy provenance and counterexample to inject into a successor agent when it touches the boundary.
- [Ten discriminating probes](ten-probes.md): safe, isolated experiments to converge on a real migration design before committing to one. No production run is claimed.

## Evidence and limits

The local example proves only that **its** normal synthetic implementation satisfies **its** owner-labeled fixtures and two deliberate faults make the contract fail. It does not prove which migration policy a real organization should adopt or that a model pair failed on a real client system. Research on correlated errors is task-scoped; research finding debate gains on a bounded task is a genuine countercase. Sources and limits appear in the weekly article draft and [Kim et al. ICML 2025](https://proceedings.mlr.press/v267/kim25e.html), [Ki et al. ACL 2025](https://aclanthology.org/2025.acl-long.1210/), and [METR's 2026 update](https://metr.org/blog/2026-02-24-uplift-update/).

## Publication gate

Eric approved all 28 original Week 02 daily cuts and their written reads, plus the Week 02 overview film and article, on 2026-09-25. That is editorial approval, not proof of publication; the 84 reference recuts remain pending separate review. This folder can be published and read back in the companion repository ahead of the article. Do not add a Week 02 release entry to `releases.json` yet.

The article release is planned for 2026-10-12 at 10:00 Pacific time or later. Its gate requires the approved film/article fingerprints, a verified Public overview film, verified Public YouTube copies of the related daily videos, and a publicly readable Week 02 companion README. Native social permalinks may be added when those posts are actually live; they are not a substitute for missing public readback. After the article is live and verified, update `releases.json`, run `scripts/build_release_readme.py`, and read back both the article and public repository links. A SaaS tool can maintain commodity implementation but does not replace the business policy owner.
