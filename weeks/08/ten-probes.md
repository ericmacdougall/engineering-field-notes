# Week 08 — ten discriminating release-gate probes

These are proposed experiments for a **disposable** environment and a fictional enterprise-entitlement rule. They are not tests already run against a customer product. Name the protected decision owner, artifact and expected state before each run.

1. **Mutate the grader.** Let the coding worker make its own test always pass. A protected, independently sourced entitlement check must still reject the broken build.
2. **Wrong artifact.** Run a valid-looking report against one commit, then attach it to another. The release packet must reject the digest mismatch. The [local companion](../../examples/release-packet-gate/README.md) covers this decision logic.
3. **Stale report.** Attach yesterday's browser result to today's build. The gate must return `UNVERIFIED`, not reuse a green state.
4. **Empty report.** Exit a test process successfully but remove its observations. The gate must pause because there is no measured result.
5. **Shortened instruction.** Remove “migration-only” from the worker's task while keeping the original customer decision protected. The independent acceptance test must catch broadened entitlement.
6. **UI/API split.** Show the right UI for a non-entitled tenant while the API allows access. Compare the target API state with the source decision and reject the release.
7. **Warm identity.** Reuse a signed-in browser session where a clean tenant is required. The identity check must fail or mark the observation unverified.
8. **Missing canary cohort.** Send traffic that omits the affected migration tenant. An aggregate green metric must not promote the release without relevant exposure.
9. **Metric outage.** Make the analysis provider return no useful observation. The rollout should pause and route to a named owner; do not translate missing data to zero failures.
10. **Expired override.** Apply a bounded exception, let its expiry pass, then rerun the gate. It must demand renewed evidence or a new owner-authorized decision and log the prior bypass.

The local Python example tests a narrower subset: valid packet, measured failure, missing operation, wrong artifact, stale report, wrong cohort, unrecognized issuer string and prelaunch behavior. It does **not** authenticate CI, mutate a repository or deployment, drive a browser, observe customers, or test an override store. Those require an authorized real integration and separate readback. [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets), [Playwright traces](https://playwright.dev/docs/trace-viewer), [Argo analysis](https://argoproj.github.io/argo-rollouts/features/analysis/) and [Google SRE canary guidance](https://sre.google/workbook/canarying-releases/) inform the operational design; Eric's three-rail acceptance policy is the editorial proposal.
