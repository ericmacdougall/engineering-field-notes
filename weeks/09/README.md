# Week 09 — What computer-use agents can prove

**Article:** [What computer-use agents can prove](https://ericmacdougall.com/journal/what-computer-use-agents-can-prove/) · the link goes live after the separate public film, companion and site checks.  
**Overview film:** [What Computer-Use Agents Can Prove](https://www.youtube.com/watch?v=HpY2JdBaBGs) · Public 5:09 film with English captions and full transcript.

The field note's rule is to let an agent navigate while a separately specified harness proves the outcome. A final screenshot or optimistic “Saved” toast is useful journey evidence, but a consequential role change needs the correct subject, durable policy result, a fresh-session effect and a negative permission check.

This folder provides a small **synthetic** receipt for that distinction. Run from here:

```sh
python acceptance_receipt.py examples/contract.json examples/journey.json examples/authority.json examples/fresh-session.json examples/effects.json
python -m unittest discover -s tests -p test_acceptance_receipt.py -v
```

The example reports `PASS` only when the journey identity, authoritative commit, target role, fresh-session check and downstream notification count agree. Its tests make an optimistic green toast coexist with a rejected policy or unchanged role and require `FAIL`. Missing independent evidence yields `UNVERIFIED`. This is not a real access-control implementation: the JSON files are not authenticated, the code does not open a browser or call a model, and no actual employee or service is changed.

[Ten discriminating probes](ten-probes.md) describe the safe next steps in a resettable tenant or development VM. A real acceptance gate must protect the contract and readback source outside the agent's writable workspace and bind observations to an actual request ID.

**Release state:** staged locally; no Public GitHub readback is claimed here. Keep this notice current when the companion is published.
