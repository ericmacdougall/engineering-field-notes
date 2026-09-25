# Fleet-change canary: sellable capacity after an operator change

Use on an operator-owned disposable or designated canary pool before a driver upgrade, MIG geometry change or scheduler-policy release. The owner sets the thresholds for each actual SKU. This is a **proposed** test plan; no fleet change or live GPU test was run for this field note.

## Define the service before the change

| Field | Owner-supplied value |
|---|---|
| Change ID, version and rollback owner |  |
| Canary nodes and tenant isolation |  |
| Offered product classes | Whole device, exact MIG profile or time-sliced class; document limits separately |
| Representative jobs | One disposable job per placement/topology class, with independent accepted-result check |
| Expected start and completion envelope | p50/p95 and deadline method; set from customer terms, not a universal benchmark |
| Queue/reclaim policy | Reservation, borrowing, preemption, notice and checkpoint assumptions |
| Stop and rollback threshold | Specific miss count, unresolved job age, service error or affected tenant threshold |
| Evidence retention | Scheduler IDs, topology, job trace, health, configuration and bill-like allocation ledger |

## Read four capacities, then the application

1. **Discovered:** GPUs and advertised profiles are visible with the intended driver/device-plugin state. Count them by class; a green inventory row is only this first gate.
2. **Admitted:** submit a disposable workload for each sold class. Record Kueue/Slurm policy decisions, quota and reservation state; an admitted job may still lack a runnable physical placement or healthy application.
3. **Placed:** read back the actual device/profile and topology. Verify the claimed class, affinity/isolation and any borrow/reclaim result.
4. **Started and accepted:** record time to first useful step or valid response, completed result, tail latency and billed/restart intervals. Compare with the owner-set envelope.

Run the same receipts before and after the change under a stated workload mix. A canary passes only if the *service* holds: starts, progress, recovery and isolation for its promised classes. Preserve the failing request IDs and rollback the change when its predefined stop threshold fires. A driver or MIG component reporting `success` is a necessary infrastructure signal, not the whole acceptance verdict.

## Failure-specific probes

- A driver upgrade can cordon and remove GPU workloads; [NVIDIA documents that enabling a drain fallback can evict all pods on a node](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/26.3/gpu-driver-upgrades.html), including non-GPU services. On a canary, verify the exact eviction configuration and collateral workload impact before broad rollout.
- [MIG Manager reconfiguration](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/26.3/gpu-operator-mig.html) requires no user workloads on the target GPUs and may reboot a node in some settings. Test profile fit and recovery on a safely isolated node; do not alter a live tenant device just to prove a blog example.
- [DCGM passive health monitoring](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html) reports recent watched incidents, not a load test. [Active diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/reference/diagnostics/plugins/diagnostic.html) apply sustained load and belong on devices taken out of production service.
- Retain the billing/allocation ledger separately from transient DCGM job statistics. [DCGM's job-statistics guide](https://docs.nvidia.com/datacenter/dcgm/latest/learn/core-services/process-and-job-statistics.html) states that a host-engine restart loses in-memory watches and job records.

The smallest useful release packet is one before/after row per product class with the five evidence states above, a request ID, and a clear reason for every miss. Product owners can then repair or narrow the offer rather than hiding gaps behind aggregate fleet utilization.
