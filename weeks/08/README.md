# Week 08 — The release gate is the product

The [field note](https://ericmacdougall.com/journal/the-release-gate-is-the-product/) argues that a passing agent-written patch can satisfy a shortened requirement while violating the actual customer decision. The fictional enterprise entitlement example separates source-linked intent, evidence tied to the exact artifact, and post-release behavior for the affected cohort.

## Companion material

- [Three-rail release packet](../../examples/release-packet-gate/README.md): a local, effect-free Python demonstration of `PASS`, `FAIL` and `UNVERIFIED` for intent, behavior and operation.
- [Ten discriminating probes](ten-probes.md): a progression from a protected customer rule and artifact mutation to target-state and canary readback in a disposable environment.

Run `python -m unittest discover -s examples/release-packet-gate/tests -p test_release_packet.py -v` from the repository root. The local normal fixture and negative controls test decision logic, not report authenticity. The packet's `issuer` string is not an authenticated identity. A real gate needs a trusted check origin, protected acceptance source, immutable artifact identifiers and independent target-state readback.

[GitHub's ruleset documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) describes selecting an expected GitHub App for a required status check. [Argo Rollouts analysis](https://argoproj.github.io/argo-rollouts/features/analysis/) distinguishes successful, failed and inconclusive runs and pauses on inconclusive analysis. These mechanisms are useful parts of a gate; neither establishes that this fictional tenant promise was met.

**Release status:** this local folder is ready for publication after exact film, article, repository and live-site gates pass. A local test is not a public release readback.
