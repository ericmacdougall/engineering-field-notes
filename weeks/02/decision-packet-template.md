# Decision packet template — approval migration

Store a filled copy outside the worker's editable checkout. This template is not a policy decision by itself.

| Field | Record |
|---|---|
| Named policy owner and approving role |  |
| Policy version and effective interval |  |
| Authoritative state source and conflicting sources |  |
| Historical cohort and source provenance |  |
| Ambiguous and revoked record handling |  |
| Replay identity and crash boundary |  |
| Rejected alternative and reason |  |
| Expected result for the consequential counterexample |  |
| Protected fixture/test path and grader owner |  |
| Observed run ID, input sample hash and final readback |  |
| Condition that reopens this decision |  |

When a future agent changes the import, approval state machine, data source or replay identity, a supervising role should deliver this packet and ask the agent to predict the counterexample **before** implementation. The independent grader still runs, because possession of context does not prove that the agent used it correctly.
