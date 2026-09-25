# Week 12 companion: the missing context gate

This is a **synthetic, side-effect-free fixture** for [The agent missed the one fact that mattered](https://ericmacdougall.com/journal/the-agent-missed-the-one-fact-that-mattered/). It accompanies Eric-approved Week 12 editorial material; public repository and article release require their own readbacks.

The fictional migration has two required backfill cohorts. One is reconciled; the other is open. A specialist steward can send a source-linked packet, but the host resolves that packet against a protected current record. The cutover service checks every required cohort again before writing a target event. Suppressing the steward message therefore cannot make the service permit an unresolved cutover.

Run from this folder with Python 3.11+:

```sh
python packet_gate.py
python -m unittest -v test_packet_gate.py
```

To check the test can catch a broken service gate, run this **only in this disposable fixture**:

```sh
PACKET_GATE_TEST_MUTANT=1 python -m unittest -v test_packet_gate.py
```

The mutant intentionally bypasses the final check. The test run must fail, including `test_suppressed_steward_still_cannot_cutover`. On PowerShell, set the temporary environment variable for only that process and clear it after.

The example does not call a model, perform real retrieval, invoke an agent-to-agent transport, enforce production permissions or migrate customer data. Its passing tests establish only that this small Python fixture handles the named cases. Actual retrieval recall, delivery coverage, model behavior, human escalation and target-service integration require separate experiments on the intended system. See [ten-probes.md](ten-probes.md).

Sources: [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/), [LongMemEval](https://proceedings.iclr.cc/paper_files/paper/2025/hash/d813d324dbf0598bbdc9c8e79740ed01-Abstract-Conference.html), [OpenAI Agents SDK handoffs](https://openai.github.io/openai-agents-python/handoffs/), [Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval), [GraphRAG](https://arxiv.org/abs/2404.16130), and [A2A specification](https://github.com/a2aproject/A2A/blob/main/docs/specification.md). These support mechanisms and bounded studied tasks, not superiority of this architecture.
