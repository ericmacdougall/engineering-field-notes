# Week 06 — Your agentic workflow depends on other people's rules

<!-- ARTICLE_START -->
**Article:** Eric-approved Week 06 field note; public master article link is added after its independent release readback. **Overview film:** [Your agentic workflow depends on other people's rules](https://www.youtube.com/watch?v=qZndKypZ1Ms), recorded Public in the campaign release manifest on 2026-09-25.
<!-- ARTICLE_END -->

## The claim

An upstream refusal, outage or policy change is unfinished work. It must not become an implicit business verdict because the adapter returned an empty classification. Law, provider policy and application authority are separate boundaries with separate owners. The company still owns the queue, evidence and downstream action.

## Runnable route-loss rehearsal

[`route_loss.py`](route_loss.py) evaluates five fictional cases in [`examples.json`](examples.json). It has no network client, credentials, live data or side effects. The first case simulates a provider refusal on an otherwise authorized internal report. It stays `OPEN_UNFINISHED` with a named security-review owner, a policy-review flag, **no fallback proposal**, and `action_executed: false`. An outage may get a **proposal only** when the local synthetic registry matches task/data class and records active approval, permitted-use review, data-agreement review, legal-use review and owner. The restricted-data case does not match. A completed-looking answer without an evidence ID becomes uncertain. A complete answer outside the actor's scope is blocked; no fixture executes a ticket or closes a case.

Run from the repository root:

```text
python weeks/06/route_loss.py weeks/06/examples.json
python -m unittest discover -s weeks/06/tests -v
```

The negative controls catch the original failure modes: a refusal cannot silently close, a refusal cannot trigger policy-shopping by this program, an unknown upstream code cannot default to success, missing evidence stays open, a data-agreement mismatch blocks an alternate proposal, and a complete model response cannot override application action rights. The code is a **toy adapter and proposal screen**, not a deployable authorization service. A registry flag is a local fixture value; it does not establish legality, provider consent, security review, data residency or current permissions. A real dispatcher must re-evaluate those against the current request and target immediately before any external effect, then read back the result.

## Operating material

- [Route-registry and handoff template](route-registry-and-handoff-template.md): capture the route owner, allowed task/data classes, policy version, refusal owner, fallback authority and queue-age limit.
- [Ten discriminating probes](ten-probes.md): inject synthetic refusal, unknown errors, missing evidence, permission drift and replay before a workflow depends on the model route.

For context, [OpenAI's published Usage Policies](https://openai.com/policies/usage-policies/) describe enforcement and an appeal path; [Anthropic's policy update](https://www.anthropic.com/news/usage-policy-update) describes changed treatment of agentic and high-risk uses. They show that provider terms are an active control layer, not that Eric's workflow experienced a refusal. The [European Commission's AI Act enforcement overview](https://digital-strategy.ec.europa.eu/en/policies/enforcement-ai-act) and the [official Regulation 2024/1689 text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689) address legal obligations for specified uses and systems. They do not turn every question in a regulated sector into a prohibited prompt. Sources rechecked 2026-09-25; a real deployment needs its current applicable terms and legal assessment.

## Evidence boundary and release gate

The fictional security queue and five example cases are synthetic. The local tests do not call a provider, demonstrate refusal frequency, test a live ticketing system, exercise a real appeals process, or certify any legal conclusion. The next integration gate is a disposable queue fixture with an owner-labeled expected state and an independent readback of case status, actor authorization and side effects after each injected failure.

Eric approved the Week 06 article and overview editorially. The overview is recorded Public; publish this companion folder to the MIT repository only after its normal and negative controls and public links pass readback. The master article's remaining gate requires a verified companion URL and site readback. Do not add a root release entry or mark the master article live merely because these local files are ready.
