"""Flag gaps and disagreement in *synthetic* work-sample scorecards.

The output is for reviewer calibration, never an automatic hiring recommendation.
"""

import json
import sys
from pathlib import Path


DIMENSIONS = (
    "technical_fundamentals", "architecture_ownership", "independent_verification",
    "business_priority", "focus_orchestration", "handoff_revision",
)


def inspect(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("candidate") != "synthetic-example-only":
        raise ValueError("This demonstration accepts only the synthetic example")
    reviewers = data.get("reviewers", [])
    if len(reviewers) != 2 or len({r.get("id") for r in reviewers}) != 2:
        raise ValueError("Expected two distinct independent reviewer scorecards")
    for reviewer in reviewers:
        scores = reviewer.get("scores", {})
        if set(scores) != set(DIMENSIONS):
            raise ValueError(f"Incomplete dimensions for {reviewer.get('id')}")
        for dimension in DIMENSIONS:
            item = scores[dimension]
            if type(item.get("score")) is not int or item["score"] not in range(1, 5):
                raise ValueError(f"Score must be an integer 1–4: {dimension}")
            if len(item.get("evidence", "").strip()) < 20:
                raise ValueError(f"Observed evidence is missing or too vague: {dimension}")

    disagreements = []
    for dimension in DIMENSIONS:
        first, second = (r["scores"][dimension]["score"] for r in reviewers)
        if abs(first - second) > 1:
            disagreements.append(f"{dimension}: {first} versus {second}")
    return disagreements


if __name__ == "__main__":
    issues = inspect(Path(sys.argv[1]))
    print("Two complete synthetic reviewer scorecards validated")
    if issues:
        print("Human calibration required:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("No large dimension-level disagreement; no hiring verdict inferred")
