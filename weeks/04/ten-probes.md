# Week 04: ten discriminating probes

These are **proposed** experiments, not reported outcomes. Screen offers with specifications and sample evidence; reserve runtime probes for a scoped pilot or disposable fleet the operator controls. The expected result depends on the customer's workload and promise.

1. Run the real single-node or multi-node job on the offered placement class. Record accepted result, complete elapsed time and all billed attempts.
2. Capture GPU, NIC, NVLink and virtual topology for that allocation; compare it to the sold class.
3. Run local bandwidth, cross-node network and NCCL collective diagnostics, then test whether those differences explain *application* step time. A synthetic probe is a diagnostic, not the verdict.
4. Repeat at the intended concurrency and workload mix. Compare p50/p95 completion or inference latency with quiet-system results.
5. Submit a topology-sensitive large job while devices are idle but fragmented; read back admission, placement and actual start.
6. Fill a supported GPU with fractional profiles, then ask for a larger profile; observe shape fit, reconfiguration and any tenant interruption.
7. Lend reserved quota to an interruptible tenant, activate the reservation, and trace notice, preemption, checkpoint validity and restart cost.
8. Vary job-duration estimates under backfill; compare expected starts, actual starts and any external start promise.
9. In a disposable operator test, inject a node or fabric fault mid-run; check detection, valid checkpoint, replacement placement and accepted final result. A buyer should request an agreed fault exercise, not affect production tenants.
10. Join request, allocation, attempt, checkpoint, accepted-result and invoice IDs. Investigate every billed interval without corresponding customer progress or contracted reservation.

The [completed-run evidence packet](start-and-recovery-evidence-template.md) tells the operator or buyer what to retain. Primary design references: [NVIDIA NCCL diagnostics](https://docs.nvidia.com/deeplearning/nccl/archives/nccl_2307/user-guide/docs/troubleshooting/performance_and_tuning.html), [Kueue](https://kueue.sigs.k8s.io/docs/overview/), [Slurm backfill](https://slurm.schedmd.com/sched_config.html), and [NVIDIA DCGM job statistics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/core-services/process-and-job-statistics.html). These sources describe possible mechanisms; they do not measure a particular supplier.
