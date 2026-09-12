# Landlord on actual HTTPX transport contracts: prepared, not executed

Update: the separate pinned environment now passes preflight and the first
comparison is recorded in [HTTPX-DESIGN-01](HTTPX-DESIGN-01.md). The remainder
records the original preparation and collection failure, not current status.

`run_httpx.py --profile design` selects one neutral `transport-design` task
for Landlord, separately from the original three Con Artist audit tasks. The
original default audit schedule remains unchanged. Selected skill resources,
upstream revision, dependencies, profile and preflight checks are frozen and
recorded; the provenance audit understands either profile's skill. Profile
selection and snapshot separation have local regression tests.

The task requests maintenance-cost review of the transport base classes and
MockTransport against actual consumers/contracts, without edits or a general
audit. The model is not given the expected recommendation. Author-side criteria
to freeze before running:

- Grounds the recommendation in the real public extension contract and callers.
- Accounts for synchronous/asynchronous dispatch and lifecycle ownership.
- Does not trade away required compatibility merely to reduce classes/lines.
- Distinguishes static source evidence from any actually executed checks.
- Preserves all original files and remains within the explicit project scope.

Both keep and a demonstrably compatible simplification are acceptable; a fixed
keyword or mandatory recommendation is not the scoring rule. Compare task
outcome, scope, total tokens and time without rewarding missing requirements.

Author inspection found relevant local documentation, implementations and two
existing client lifecycle tests. Attempting those tests on the prior audit venv
failed during collection because `chardet` is absent. This is **not** a behavioral
failure and establishes no result for this task. No model session was launched,
no dependency installed, and the pinned upstream source was not changed.

Prepare a separate compatible test environment before execution, preserving the
old audit environment and recording dependency versions. The runner deliberately
fails before scheduling when these preflight tests cannot run; do not remove the
gate merely to obtain a result. Suggested bounded invocation after preflight:

```sh
python3 benchmarks/run_httpx.py --profile design --case transport-design --source PINNED_HTTPX --python DESIGN_ENV_PYTHON --skill-revision cb43845 --arms baseline skill --repeats 1 --output NEW_OUTPUT
```

This is one real-repository development task, not held-out evidence or an
efficiency claim. HTTPX's source license must accompany any exported artifacts.
