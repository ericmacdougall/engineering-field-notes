# Week 14 companion: the demo and the owner

This MIT-licensed, synthetic approval-history fixture accompanies [The demo worked. The engineering problem began afterward](https://ericmacdougall.com/journal/the-demo-worked-the-engineering-problem-began-afterward/). It does not contain customer data, a model call, a provider API or a SaaS integration.

`naive_migration` deliberately converts a legacy `approved=true` flag to `ACTIVE`, including a record with a later revocation. `protected_decision` instead uses ordered owner-labeled events, policy version, approver and expiry; ambiguous provenance becomes `UNKNOWN`. `resume_from_handoff` ignores a prose summary as authority and checks the current record and sequence. These are rules for the fictional exercise, not a real company's approval policy.

Run from this folder with Python 3.11+:

```sh
python -m unittest -v test_approval_fixture.py
```

For the deliberate bad-code control, set `W14_TEST_MUTANT=1` for one test process and rerun. The revocation test must fail. On PowerShell: `$env:W14_TEST_MUTANT='1'; python -m unittest -v test_approval_fixture.py; Remove-Item Env:W14_TEST_MUTANT`. The mutation belongs only in this disposable fixture.

The [blank cost worksheet](ownership-cost-template.csv) calls for actual license terms, owner time, support, infrastructure, integration and opportunity costs before a build/buy/stop conclusion. The [ten proposed probes](ten-probes.md) include held-out history, an accepted second change, a resumed session and a real owner decision. The local suite exercises only the named synthetic branches; it does not measure a coding model, migrate records or establish a company-specific cost ratio.

The article cites [GitHub's Copilot agent application card](https://docs.github.com/en/copilot/responsible-use/agents), [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/), [2025 DORA research](https://dora.dev/research/2025/dora-report/) and [maintainability sensors for coding agents](https://martinfowler.com/articles/sensors-for-coding-agents.html). Those sources frame review, ownership and measurement; they do not validate this fictional company's policy or economics.
