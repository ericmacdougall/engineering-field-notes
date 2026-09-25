# Week 04 — The GPU number is not the compute product

<!-- ARTICLE_START -->
**Article:** Eric-approved Week 04 field note; public master article link is added after its independent release readback. **Overview film:** [The GPU number is not the compute product](https://www.youtube.com/watch?v=wePsX_iWyT0), recorded Public in the campaign release manifest on 2026-09-25.
<!-- ARTICLE_END -->

## The claim

A GPU count and sticker rate do not tell a buyer whether a specific job will start, finish, recover and cost what the offer implies. A fleet operator must join placement, queue policy, sharing, application progress, recovery and billing evidence. This companion keeps those measurements distinct rather than giving a synthetic calculator authority over a real service.

## Runnable counterexample

[`contract_report.py`](contract_report.py) reconciles a small **fictional** attempt ledger in [`sample-runs.csv`](sample-runs.csv). `LowSticker` charges $2.00 per billed GPU-hour but spends $54.00 over retries for two accepted results: $27.00 per accepted result. `FitForJob` charges $2.80 and spends $35.00 for two accepted results: $17.50 each. The numbers are invented to expose a comparison error; they are not observed provider prices, performance or reliability.

From the repository root:

```text
python weeks/04/contract_report.py weeks/04/sample-runs.csv
python -m unittest discover -s weeks/04/tests -v
```

The CSV's `billed_gpu_minutes` is already the sum of billable device-minutes across the allocation. The script multiplies that by the per-GPU-hour price and divides by 60; it does **not** multiply by `gpu_count` again. Each `request_id` can have several `attempt_id` values. Every billed attempt, including an unsuccessful retry, contributes to the provider cohort's observed spend. A request has one consistent final state: `accepted`, `failed`, or `open`. An accepted request has exactly one accepted attempt. If any request is `open`, the code withholds `completed_cohort_cost_per_accepted_usd`; a partial cohort is not a comparable completed-run KPI.

`p95_sum_of_queue_intervals_minutes` is a diagnostic sum of entered queue intervals per request. It is **not** wall-clock time to a usable first allocation, a completion-time percentile, or an SLA verdict. A retry can spend time running and recovering between queue intervals. The code deliberately emits `first_start_sla_verdict: not_measured`. For an actual start-time promise, fill the separate [start and recovery evidence packet](start-and-recovery-evidence-template.md) with source timestamps, placement class and the contract's exact definition of “start.”

The negative controls reject duplicate attempt IDs, two accepted attempts for one request, contradictory request state/topology, and a unit-cost claim for an open cohort. One test changes queue time and checks that the script still refuses to infer a first-start SLA. The tests prove only these synthetic contract properties.

## Operator and buyer packet

- [Start and recovery evidence template](start-and-recovery-evidence-template.md): pin the offered SKU, placement class, scheduler trace, application progress, restart window and billed ledger on one request ID.
- [Fleet-change canary template](fleet-change-canary-template.md): measure discovered, admitted, placed and actually started capacity through driver, MIG and scheduler-policy changes on operator-owned test capacity.
- [Ten discriminating probes](ten-probes.md): scope a paid pilot or disposable operator environment. A buyer can ask for a representative report and proposed pilot before signing; no unrestricted production access is assumed.

The offer should distinguish whole-device, MIG-profile and time-sliced capacity. [NVIDIA's MIG guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html) gives finite H200 profile limits; it does not turn seven instances into seven complete H200s. [Kueue's overview](https://kueue.sigs.k8s.io/docs/overview/) separates admission and quota policy from Kubernetes pod placement, while its current topology-aware features can also validate some physical fit before admission when configured. Neither is a measured customer result. [Slurm's backfill guide](https://slurm.schedmd.com/sched_config.html) protects *expected* higher-priority starts according to estimates, which must still be compared with a customer's actual promise. [NVIDIA DCGM's job-statistics guide](https://docs.nvidia.com/datacenter/dcgm/latest/learn/core-services/process-and-job-statistics.html) explains why transient device telemetry is not a durable invoice ledger. Sources rechecked 2026-09-25.

## Evidence boundary and release gate

No real neocloud account, GPU, NCCL collective, Kubernetes/Slurm scheduler, fabric, invoice or customer workload was accessed for this kit. The synthetic price reversal is an arithmetic demonstration, not a vendor ranking. Before a production decision, align request and attempt IDs to authoritative allocation and billing records, reconcile credits and reserved charges, run the application on the exact placement class, and compare *observed* start/completion distributions with contractual terms.

Eric approved the Week 04 article and overview editorially. The overview is recorded Public; this local companion can be published with the MIT repository only after its files, tests and links pass public readback. The master article's remaining gate requires a verified companion URL and site readback. Do not add the Week 04 entry to the root release list or claim the master article is live merely because these files exist locally.
