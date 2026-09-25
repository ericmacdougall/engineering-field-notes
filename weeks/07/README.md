# Week 07 — Hire engineers for the decisions

The [field note](https://ericmacdougall.com/journal/hire-engineers-for-the-decisions/) proposes a short interview over an employer-supplied agent patch. The point is to hear a candidate's causal model, falsifying test, revised release decision, product judgment and handoff without asking for an unpaid multi-week build. The billing migration and meeting scheduler are fictional teaching examples. This exact interview format is Eric's proposal, not an externally validated hiring instrument.

## Companion material

- [Fictional interview packet](../../examples/hiring-interview-calibration/exercise.md): one short artifact, three open questions, strong-answer signals and a late consumer fact.
- [Pilot rubric](../../examples/hiring-interview-calibration/rubric.md): behavioral anchors for fundamentals, architecture, independent verification, priority, focus and handoff.
- [Reviewer calibration script](../../examples/hiring-interview-calibration/README.md): checks two synthetic scorecards for missing evidence and flags large disagreement. It never selects or ranks people.
- [Ten employer experiments](ten-probes.md): tests for the hiring team to run before applying a new interview to real applicants.

## Local test and boundary

From the repository root, run `python -m unittest discover -s examples/hiring-interview-calibration -p test_calibration.py -v` and `python examples/hiring-interview-calibration/calibrate_reviewers.py examples/hiring-interview-calibration/reviewer-example.json`. The test fixture is synthetic and contains one intentional reviewer disagreement. These results establish the script's parsing and flagging behavior only. They do not measure interview validity, predict job performance, or license an automated hiring decision.

The [U.S. Office of Personnel Management](https://www.opm.gov/policy-data-oversight/assessment-and-selection/structured-interviews/) describes common questions and rating standards; its [guide](https://www.opm.gov/policy-data-oversight/assessment-and-selection/structured-interviews/guide.pdf) includes behavioral anchors and interviewer calibration. OPM does not prescribe Eric's three prompts or a compensation policy for a practical exercise. Adapt the packet to the actual job analysis, protect candidate privacy, pilot reviewer agreement and compare ratings with later work outcomes before use.

**Release status:** this local folder is ready for publication after exact film, article, repository and live-site gates pass. A local test is not a public release readback.
