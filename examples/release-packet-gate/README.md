# Three-rail release packet, synthetic local example

This accompanies [Week 08](../../weeks/08/README.md). It compares a source decision file, exact artifact file and three dated evidence reports. A passing outcome requires `intent` and `behavior` for `prelaunch`, plus `operation` for `promotion`. Missing, stale, mismatched and wrong-cohort evidence returns `UNVERIFIED`; an explicit measured failure returns `FAIL`.

From the repository root:

```text
python examples/release-packet-gate/release_packet.py examples/release-packet-gate/examples/valid.json
python -m unittest discover -s examples/release-packet-gate/tests -p test_release_packet.py -v
```

The eight tests include wrong-artifact, stale-report, wrong-cohort, missing-report and unrecognized-issuer negative controls. The fixture's `as_of` time is fixed, so the demonstration remains repeatable. The script has no network calls or deployment effects.

**Boundary:** an `issuer` field in local JSON is just a string. A production check needs a platform-authenticated origin, protected test contract, observed target state and actual customer cohort. [GitHub's ruleset source control](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) and [Argo's inconclusive analysis state](https://argoproj.github.io/argo-rollouts/features/analysis/) illustrate parts of that design. The source article's tenant is fictional, and local green output is not evidence of a live customer release.
