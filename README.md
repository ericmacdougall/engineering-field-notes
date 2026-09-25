# Engineering Field Notes

Working examples and decision records for [Eric MacDougall's forthcoming field notes](https://ericmacdougall.com/). Each note starts with a problem encountered in agentic software work, then shows a small control or experiment you can inspect. This repository keeps the scripts and their limits in one place.

## Weekly field notes

The article link and the week's tested additions are entered here **when that article is publicly released**. The same release updates its companion folder and links the repo from the article.

<!-- RELEASES_START -->
No field note has been publicly released yet. The first article and field kit are being prepared.
<!-- RELEASES_END -->

## Start with the first field kit

[Week 01 — Agents need an independent exam](weeks/01/README.md) connects the argument to two small, runnable examples:

- [Agent harness](examples/agent-harness/README.md): a worktree launcher, a narrow PreToolUse path guard, a PostToolUse write receipt, and a CI verifier that rejects missing or vacuous evidence.
- [Commerce acceptance contract](examples/commerce-harness/README.md): one-stock-unit and payment-retry examples with deliberate broken variants that the contract catches.

Run the hook tests with `python -m unittest discover -s examples/agent-harness -p test_harness.py -v`. Run the commerce negative control with `python examples/commerce-harness/run_contract.py` after installing `pytest`.

The commerce example uses SQLite and a fake provider. The hook example tests the Python script directly. Neither result establishes production PostgreSQL/Stripe behavior, nor that a particular agent product invoked a hook in every local, cloud, or delegated route. Those are separate integration tests.

## How this repo grows

Each weekly article gets a folder under `weeks/NN/` with its claim, examples, sources, test evidence and untested boundary. We add an entry above only on the corresponding article's live release. Code changes that alter an example's claimed behavior need a new normal run and a deliberately failing counterexample. We retain old limits rather than silently turning an illustrative fixture into a production claim.

Everything here is authored for these field notes. External references are cited; third-party project code and scripts are not imported to make the examples appear more complete.

The scripts and documentation in this repository are available under the [MIT License](LICENSE), copyright 2026 Eric MacDougall.
