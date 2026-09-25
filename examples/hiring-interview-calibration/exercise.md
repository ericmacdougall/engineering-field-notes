# Fictional structured interview prompt: billing-event migration

**Purpose:** Practice and critique only. No real candidate or hiring decision is represented.

## One-page artifact prepared by the interviewer

A billing producer emits `InvoicePosted.v1`. The product team asks for `InvoicePosted.v2`, adding a new allocation breakdown. The interviewer supplies a short producer diff, its green local test summary and a simple producer/queue/consumer diagram. A coding agent drafted the patch; candidates do not build it. Two downstream consumers belong to other teams; their code and release dates are outside the packet. The brief does not define how long queued v1 events may replay, how long consumers may lag, or who can authorize a cutover.

Ask each candidate the same three open prompts in a bounded interview:

1. **What could make this green patch unsafe to release?** Listen for producer, queue, consumer, old-event replay, partial deployment, contract owner and rollback authority. A confident “ship” or generic “test more” is weak without a causal path.
2. **What smallest independent result would change your mind?** Listen for a saved v1 event, the exact consumer version, an expected business result and a deliberate incompatible variant that should fail. The candidate describes the check; the employer builds and runs it later.
3. **Given the late fact below, what do you decide and hand off?** Listen for a revised release recommendation, a possible dual-version path, an owner-approved compatibility window and a concise source/change/proof/uncertainty/owner record. The candidate must not invent evidence that has not been observed.

## Late fact for the assessor to reveal consistently

One downstream consumer cannot deploy for two weeks, and a replay job can re-deliver v1 events after the producer's deployment. Reveal this after the candidate's initial answer. Score the revision, not whether they guessed this exact fact earlier.

## Optional prioritization turn

Briefly describe a documentation cleanup request and a production alert of unknown customer impact. Ask what runs in parallel, what waits and which fact would change that decision. Assess whether bounded delegation protects human review capacity. No agent streams need to be operated in the interview.

The scenario intentionally omits a product policy; reviewers must not reward a single invented compatibility period as the “right” answer. The goal is to reveal reasoned ownership, not to trick the participant with a junior coding-pattern bug. This packet is interviewer preparation, not a request for free implementation or a production deliverable.
