# Engineering Field Notes

Working examples and decision records for [Eric MacDougall's field notes](https://ericmacdougall.com/). Each note starts with a problem encountered in agentic software work, then shows a small control or experiment you can inspect. This repository keeps the scripts and their limits in one place.

## Weekly field notes

The article link and the week's tested additions are entered here **when that article is publicly released**. The same release updates its companion folder and links the repo from the article.

<!-- RELEASES_START -->
- **2026-09-25 - Week 14: [The demo worked. The engineering problem began afterward.](https://ericmacdougall.com/journal/the-demo-worked-the-engineering-problem-began-afterward/)** - [week-specific examples, sources and evidence boundaries](weeks/14/README.md)
- **2026-09-25 - Week 13: [The agent timed out after the change went through](https://ericmacdougall.com/journal/the-agent-timed-out-after-the-change-went-through/)** - [week-specific examples, sources and evidence boundaries](weeks/13/README.md)
- **2026-09-25 - Week 12: [The agent missed the one fact that mattered](https://ericmacdougall.com/journal/the-agent-missed-the-one-fact-that-mattered/)** - [week-specific examples, sources and evidence boundaries](weeks/12/README.md)
- **2026-09-25 - Week 11: [The schema is green. The action is wrong.](https://ericmacdougall.com/journal/where-jev-and-model-control-actually-live/)** - [week-specific examples, sources and evidence boundaries](weeks/11/README.md)
- **2026-09-25 - Week 10: [The attention drift bubble](https://ericmacdougall.com/journal/the-attention-drift-bubble/)** - [week-specific examples, sources and evidence boundaries](weeks/10/README.md)
- **2026-09-25 - Week 09: [What computer-use agents can prove](https://ericmacdougall.com/journal/what-computer-use-agents-can-prove/)** - [week-specific examples, sources and evidence boundaries](weeks/09/README.md)
- **2026-09-25 - Week 08: [The release gate is the product](https://ericmacdougall.com/journal/the-release-gate-is-the-product/)** - [week-specific examples, sources and evidence boundaries](weeks/08/README.md)
- **2026-09-25 - Week 07: [Hire engineers for the decisions](https://ericmacdougall.com/journal/hire-engineers-for-the-decisions/)** - [week-specific examples, sources and evidence boundaries](weeks/07/README.md)
- **2026-09-25 - Week 06: [Your agentic workflow depends on other people’s rules](https://ericmacdougall.com/journal/your-agentic-workflow-depends-on-other-peoples-rules/)** - [week-specific examples, sources and evidence boundaries](weeks/06/README.md)
- **2026-09-25 - Week 05: [AI in industrial control needs physical evidence](https://ericmacdougall.com/journal/ai-in-industrial-control-needs-physical-evidence/)** - [physical-evidence oracle and ten discriminating probes](weeks/05/README.md)
- **2026-09-25 - Week 04: [The GPU number is not the compute product](https://ericmacdougall.com/journal/the-gpu-number-is-not-the-compute-product/)** - [week-specific examples, sources and evidence boundaries](weeks/04/README.md)
- **2026-09-25 - Week 03: [Where model control actually lives](https://ericmacdougall.com/journal/where-model-control-actually-lives/)** - [model control contract, authority map and ten discriminating probes](weeks/03/README.md)
- **2026-09-25 - Week 02: [Model consensus is not engineering evidence](https://ericmacdougall.com/journal/model-consensus-is-not-engineering-evidence/)** - [migration decision contract, decision packet and ten discriminating probes](weeks/02/README.md)
- **2026-09-25 - Week 01: [Agents need an independent exam](https://ericmacdougall.com/journal/agents-need-an-independent-exam/)** - [agent harness and commerce acceptance contracts](weeks/01/README.md)
<!-- RELEASES_END -->

## Approved companion material

[Week 01 — Agents need an independent exam](weeks/01/README.md) connects the argument to two small, runnable examples:

- [Agent harness](examples/agent-harness/README.md): a worktree launcher, a narrow PreToolUse path guard, a PostToolUse write receipt, and a CI verifier that rejects missing or vacuous evidence.
- [Commerce acceptance contract](examples/commerce-harness/README.md): one-stock-unit and payment-retry examples with deliberate broken variants that the contract catches.

Run the hook tests with `python -m unittest discover -s examples/agent-harness -p test_harness.py -v`. Run the commerce negative control with `python examples/commerce-harness/run_contract.py` after installing `pytest`.

The commerce example uses SQLite and a fake provider. The hook example tests the Python script directly. Neither result establishes production PostgreSQL/Stripe behavior, nor that a particular agent product invoked a hook in every local, cloud, or delegated route. Those are separate integration tests.

[Week 02 — Model consensus is not engineering evidence](weeks/02/README.md) adds a synthetic migration decision contract, a durable decision packet and ten proposed probes. Its [contract runner](examples/migration-decision/README.md) compares owner-labeled state and audit outcomes with two deliberate faults. The example does not report a client migration or choose a real organization's policy.

[Week 03 — Where model control actually lives](weeks/03/README.md) adds a synthetic model control contract, an authority map for host and provider tool loops, and ten proposed probes. Its [contract runner](examples/model-control-contract/README.md) catches typed-but-wrong choices and stale routes in owner-labeled fixtures. It does not claim a live Jev integration, provider hook, Kimi K3 benchmark or production business decision.

[Week 05 — AI in industrial control needs physical evidence](weeks/05/README.md) adds a synthetic [physical-evidence oracle](examples/physical-evidence-oracle/README.md) and ten proposed probes. Its local runner passes ten owner-labeled fixture cases; it does not connect to a PLC, validate a safety function, run a vendor simulator or commission equipment.

## How this repo grows

[Week 15 — Did the forbidden effect stay blocked?](weeks/15/README.md) adds a disposable loopback service, narrow pre-call checks, target authorization, durable operation receipts, ten route/failure probes and a deliberately bad effect that the independent oracle catches. These are synthetic local experiments; no named agent harness or customer environment was tested. The corresponding article link is added after its public site release.

Each weekly article gets a folder under `weeks/NN/` with its claim, examples, sources, test evidence and untested boundary. We add an entry above only on the corresponding article's live release. Code changes that alter an example's claimed behavior need a new normal run and a deliberately failing counterexample. We retain old limits rather than silently turning an illustrative fixture into a production claim.

Everything here is authored for these field notes. External references are cited; third-party project code and scripts are not imported to make the examples appear more complete.

The scripts and documentation in this repository are available under the [MIT License](LICENSE), copyright 2026 Eric MacDougall.
