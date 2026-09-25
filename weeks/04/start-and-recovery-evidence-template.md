# Completed-run evidence packet template

Fill one packet per representative request in a **scoped pilot** or on an operator-owned test fleet. Obtain a commercial description, placement class and sample evidence before a contract; run workload experiments when there is an agreed test allocation. This template is a decision aid, not a request for unrestricted access to another tenant's cluster.

| Field | Record or source receipt |
|---|---|
| Workload and acceptance owner | Model/version, data class, job size, expected result and who accepts it |
| Offer/contract version | SKU, price basis, reservation, sharing class, topology class, target p95 and exclusions |
| Identity chain | Customer request ID, scheduler job ID, attempt IDs, invoice line IDs and any checkpoint ID |
| “Start” definition | First allocation, pods ready, first useful step or other contract term; use one definition consistently |
| Submitted and first usable-start timestamps | UTC values, clock source, source logs and clock-skew uncertainty |
| Placement proof | Device IDs/profile, host/rack/fabric domain, topology receipt and isolation policy |
| Queue policy | Admission, borrow/reclaim, priority, preemption, reservation and notice decision trace |
| Application result | Throughput/step times or response latency plus the independent accepted-result receipt |
| Recovery | Failure time, detection, checkpoint validity, retry placement, lost work and restart time |
| Accounting | Allocated/billed GPU-minutes by attempt, rate, credits, idle/restart charges and invoice reconciliation |
| Diagnostic context | GPU/fabric health, bandwidth/collective probe and service version, with collection limits |
| Miss disposition | Exact breached term, customer impact, owner, correction and retest evidence |

**Do the calculation only after defining the boundary.** For first usable start, subtract the recorded request-submission timestamp from the recorded first usable-start timestamp and compare it to the contract's threshold. For completed-run cost, join **all** billed attempts to the same request and divide the completed cohort's spend by independent accepted results. Report unresolved/open requests separately. Queue intervals alone omit time spent running, failing and recovering, so they cannot establish a wall-clock start or completion promise.

Do not treat device activity as accepted application work. [DCGM job statistics](https://docs.nvidia.com/datacenter/dcgm/latest/learn/core-services/process-and-job-statistics.html) depend on watches and host-engine lifetime; persist the scheduler and billing identities independently. If a provider cannot share a raw trace, agree on a redacted packet with timestamps, policy decision and bill tied to your own request, then validate the workload in a scoped pilot.
