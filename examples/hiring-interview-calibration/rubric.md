# Pilot rubric — score observed evidence, 1–4

Derive actual criteria and weights from the job analysis before using this in selection. This sample separates dimensions so articulate process talk cannot substitute for technical skill. Record concrete evidence and uncertainty for each score. Two assessors should score independently, then discuss disagreements.

| Dimension | 1 — weak evidence | 2 — partial evidence | 3 — strong evidence | 4 — exceptional evidence |
|---|---|---|---|---|
| Technical fundamentals | Cannot trace producer, queue, consumers and version effects. | Traces main path but misses replay or partial deployment. | Explains ordering, replay, compatibility and recovery coherently. | Tests causal assumptions and anticipates interactions between failure modes. |
| Architecture and ownership | Treats green producer tests as whole-system approval. | Notices consumers but leaves owner and cutover vague. | Names contract owners, compatibility plan and rollback authority. | Designs a reversible, observable transition across team boundaries. |
| Independent verification | Repeats agent claims or tests. | Adds tests but expected outcomes mirror the patch. | Proposes externally specified old-event replay and consumer readback. | Uses negative controls and explains what each oracle cannot prove. |
| Business priority | Builds by default without lifetime owner. | Mentions cost but not alternatives. | Compares buy/build/compose/wait with ownership and goal impact. | Makes the comparison explicit under changed constraints. |
| Focus and orchestration | Launches overlapping work with no review plan. | Splits tasks but no clear gate or priority. | Bounds independent streams and protects a decision window. | Adjusts orchestration when the production alert or consumer fact changes. |
| Handoff and revision | Says “done” without proof or owner; defends first answer. | Provides partial status and adjusts some details. | Gives source/change/proof/uncertainty/owner and revises on evidence. | Leaves a durable decision record another engineer can safely resume. |

This rubric does not define an automatic pass score. Ask a short technical fundamentals follow-up appropriate for the role; do not infer coding ability from polished process language alone. Pilot inter-rater agreement and compare the rubric with later job outcomes before treating it as a predictive selection instrument. A practical implementation test, if truly necessary, should be a separate bounded paid exercise under Eric's proposed fairness policy.
