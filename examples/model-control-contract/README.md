# Model control contract

This small, **synthetic** exercise accompanies [Week 03](../../weeks/03/README.md). It demonstrates two boundaries from the article, without claiming to integrate Jev, a decoder mask, a coding-agent hook, or a real payment system.

Run `python examples/model-control-contract/run_contract.py` from the repository root. The runner checks three owner-labeled refund cases, then requires two deliberate faults to turn red: a type-valid, high-confidence choice that ignores settlement state, and a route selected before a registry permission change. The expected output contains two `PASS` lines and two `REJECTED` lines; any surviving fault exits with an error.

The worker proposal in `candidate.py` is replaceable. The owner rule and final dispatch check in `trusted_contract.py` are separate. The `confidence` number is deliberately ignored by the permission gate. In a real system, the protected cases must come from policy owners, the current registry must be read at the actual dispatch point, and side effects need independent readback. This file tests none of those integrations. It also does not compare Jev, Haiku, or Qwen latency or quality; that requires a matched end-to-end workload.
