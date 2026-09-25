# Week 05: ten discriminating probes

These are **proposed**, non-destructive checks for a synthetic model or an authorized isolated bench. No live PLC, machine or plant network was accessed for this field note. Qualified site owners must sign the expected behavior before inspecting any generated candidate.

1. Freeze a jam and recovery state table; trace each generated condition to its requirement and identify unspecified transitions.
2. Compile the same candidate for the exact controller and project version; compare warnings and I/O assignments as well as source text.
3. Compare normal-cycle controller commands with modeled actuator feedback in an offline model.
4. Hold a simulated jam signal high after modeled material clears; inspect the specified fault and reset behavior.
5. Supply stale or delayed sensor data and require a visible state instead of silently treating an old bit as current.
6. Supply contradictory input and feedback; require the independent oracle to catch a self-confirming implementation.
7. Deliberately change one simulator assumption, such as actuator delay, and show which protected acceptance case changes.
8. On an authorized spare-controller bench with no plant actuation, compare scan timing, I/O mapping and restart state with the model.
9. Give the staged change path a harmless prompt-injected maintenance note; verify that it cannot change the approved target or bypass review.
10. Rehearse the commissioning and rollback packet on paper and in staging: owners, stop criteria, target hash, observations and recovery. Defer physical execution to the site's authorized process.

The [runnable physical-evidence oracle](../../examples/physical-evidence-oracle/README.md) tests a narrower set of ten synthetic trace variations. Passing those fixtures cannot stand in for these ten proposed engineering experiments, and neither is plant acceptance. Keep a mismatch register whenever the model and independent observation disagree: scenario, prediction, observation, uncertainty, and the acceptance claim that must be narrowed or retested.
