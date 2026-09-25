# Physical-evidence oracle: synthetic conveyor case

This read-only Python example asks whether a fictional conveyor trace satisfies an owner-supplied jam and recovery contract. It deliberately distinguishes **the controller's stop command** from **independently observed motion**. It also refuses to call an offline model a plant acceptance when its fault coverage, target identity, motion reading or rollback record is missing.

From the repository root:

```powershell
python examples/physical-evidence-oracle/run_probes.py
```

The runner asserts ten local fixtures and prints their verdicts. The passing case says only that one invented trace meets the chosen synthetic checks. Faults produce `CANDIDATE_FAIL`; missing evidence produces `EVIDENCE_GAP`. Both reject an acceptance claim. You can change a fixture to test whether the oracle detects an omitted fault or unsafe restart.

`oracle.py` and `run_probes.py` use the Python standard library and contain no controller address, vendor connection, PLC language, machine command or network call. The thresholds and times are fictional. A qualified site owner must write actual requirements and choose independent measurements. A real safety function has its own specification, validation, change authority and qualified acceptance; none of that is certified by this example.

See the [Week 05 field-note companion](../../weeks/05/README.md) for the full evidence ladder and proposed offline/isolated-bench probes, and the [Public master article](https://ericmacdougall.com/journal/ai-in-industrial-control-needs-physical-evidence/) for the full argument and corrected overview film.
