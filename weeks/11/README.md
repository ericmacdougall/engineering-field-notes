# Week 11 companion: the schema is green, the action is wrong

This synthetic, standard-library example accompanies [The schema is green. The action is wrong](https://ericmacdougall.com/journal/where-jev-and-model-control-actually-live/). It asks a narrow question: can a host reject a well-formed but unauthorized proposal before a fictional evidence transfer? It does not invoke Jev, a model, a partner API, or a production permission service.

The local checker binds a proposal to a source record, digest, current policy version, scoped permit, expiry, and optional recipient-side observation. Its outcomes separate `FORMAT_REJECTED`, `EVIDENCE_MISSING`, `AUTHORITY_REJECTED`, and `READY_FOR_SEPARATE_DISPATCH`. Even a ready proposal without independent readback reports `UNKNOWN`, not success. The code never dispatches a transfer.

From this folder, run:

```sh
python control_gate.py examples/blocked.json
python control_gate.py examples/allowed-unobserved.json
python -m unittest discover -s tests -v
```

The first fixture is valid JSON yet proposes a forbidden transfer. The second is eligible for a separate dispatch, but no target observation exists. The local test suite exercises both and deliberately malformed, stale, forged, expired, or conflicting variants. See [ten proposed probes](ten-probes.md) for experiments needed before applying the design to a real system.

**Boundary:** the JSON policy, digest, and permit are owner-labeled fixture data, not authenticated authority. A real implementation needs a protected current source, caller identity bound to a permit, narrow credentials, a service-level check on every reachable route, idempotent dispatch, and independent target readback. The fixture cannot prove a hosted model's grammar behavior, Jev calibration, or a live business outcome.

The article cites the [XGrammar engine integration guide](https://xgrammar.mlc.ai/docs/latest/using_xgrammar/engine_integration.html), [vLLM structured outputs](https://docs.vllm.ai/en/latest/features/structured_outputs/), and [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs/) for their respective control surfaces. These sources support mechanism claims, not a claim that this small fixture exercised those runtimes.
