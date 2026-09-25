# Route registry and unfinished-work handoff

Store the approved registry and decision receipts outside the worker's editable prompt context. This template records decisions; a filled checkbox does not itself authorize a new provider or legal use.

| Field | Record |
|---|---|
| Workflow owner and consequence | Who owns each case and what happens if it is delayed or mishandled? |
| Intended task class | Exact model work and excluded task classes |
| Input data class and residency | Classification, export restriction, retention, deletion and agreement evidence |
| Provider/model route | Service, model/version, tool scope, account, expiry and change-notice path |
| Provider-policy review | Current terms version, permitted-use conclusion, owner and review date |
| Legal/compliance review | Applicable jurisdiction/use, qualified owner, decision/version and review date |
| Application action authority | Current actor, allowed target/action, least privilege and final recheck point |
| Upstream result taxonomy | Completed, refused, unavailable, uncertain; raw response ID and mapped category |
| Refusal owner | Named person/queue, appeal path, evidence retention and no automatic alternate dispatch |
| Outage fallback | Named alternate, its *own* terms/data review, owner, expiry, capacity and budget |
| Human continuity | Queue-age limit, on-call route, customer communication and stop-taking-work threshold |
| Reconciliation | Case ID, input/evidence hash, model request ID, decision version, target-state readback |

**On a refusal:** keep the case open, retain the original evidence under normal access rules, attach the provider response category and request ID where available, and hand it to the policy owner. Do not retry a list of providers until one answers. The owner decides whether appeal, a separately permitted route, deterministic handling or human review is appropriate.

**On an outage:** a registry match can propose a route, but dispatch must recheck active terms, data agreement, actor permission and target state. Bound retries; distinguish a timeout from a refusal. On an uncertain answer, demand evidence or review rather than fabricating a default category.

At recovery, reconcile every outstanding case: still open, reviewed, escalated, or completed by an explicitly authorized action. Record duplicate attempts and prove there was no silent closure. The [fictional fixture](route_loss.py) exercises only a fraction of this packet.
