# Hiring interview calibration, synthetic example

This is a small interviewer-preparation tool for [Week 07](../../weeks/07/README.md). It checks a fictional pair of independently written reviewer scorecards for complete behavioral evidence and flags dimension scores more than one point apart. It does not score a candidate automatically, decide whom to hire or claim validated predictive power.

Run from the repository root:

```text
python examples/hiring-interview-calibration/calibrate_reviewers.py examples/hiring-interview-calibration/reviewer-example.json
python -m unittest discover -s examples/hiring-interview-calibration -p test_calibration.py -v
```

The [fictional interview packet](exercise.md) includes three short open questions, a consistent late fact and strong-answer signals. The [pilot rubric](rubric.md) covers six dimensions with observable anchors. The [fixture](reviewer-example.json) intentionally disagrees on independent verification; the script should request human calibration. All files are for employer-side pilot preparation, not candidate homework. The script rejects candidate identifiers other than `synthetic-example-only` so this demonstration cannot accidentally process a real applicant file.

Before using a similar process in hiring, derive criteria from the role, use identical questions and time, document review evidence, and study disagreement and later job outcomes. The [OPM structured-interview guidance](https://www.opm.gov/policy-data-oversight/assessment-and-selection/structured-interviews/) describes consistent questions and ratings; this specific packet is Eric's design.
