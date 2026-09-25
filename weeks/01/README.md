# Week 01 — Agents need an independent exam

<!-- ARTICLE_START -->
**Article:** Eric authorized immediate journal publication of approved Week 01 material on 2026-09-25. Add the public article link here and to the root README after its live site readback.
<!-- ARTICLE_END -->

## The claim

A coding agent can write implementation, tests and summary in one run. The release decision needs an acceptance condition and outcome readback that the worker did not author or control. Ordinary bugs such as a missing guarded stock update or unstable payment retry key are not exotic agent failures; a fast worker or junior developer can miss them. Encode those patterns in shared gateways and independent contracts.

## The runnable examples

1. [Agent harness](../../examples/agent-harness/README.md) shows a covered tool denial, a post-tool write receipt and a verifier that rejects empty tests and a surviving deliberate fault.
2. [Commerce acceptance contract](../../examples/commerce-harness/README.md) simulates one-unit allocation and a lost payment acknowledgment, then deliberately breaks each behavior to show the contract turns red.

## What was really checked

- The standalone Python hook guard denied an out-of-root write and shell call; six local unit tests passed on 2026-09-24.
- The commerce runner passed two normal contracts and observed both deliberate faults fail on 2026-09-24.
- This does **not** prove the hooks are installed in Claude Code, Cursor, Codex or any hosted agent surface. It does **not** exercise a real provider charge or PostgreSQL race.

## The next experiment

Run a harmless forbidden action against each intended agent runtime, record whether its actual tool path reached the guard, and read the filesystem or service state afterward. Run the commerce contract against the actual transaction gateway and a provider sandbox before calling it a deployed control.
