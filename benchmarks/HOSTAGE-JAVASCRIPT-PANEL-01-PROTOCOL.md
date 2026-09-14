# JavaScript SubmitPanel development screen

Candidate resource `8ca9e70` (JavaScript controlled-call asset plus runtime routing).
Freeze hostage-javascript-panel-cases.json SHA-256
`20545c1e08faf86c67f228c935dce74e947fb1faf983dcce0becbe99290c199c`.
One authored ES-module task, not an independent holdout or browser benchmark.

The model receives the existing panel implementation, two native tests and an
explicit contract. It must preserve signal/result/error identity and the existing
tests, while adding pending state, same-instance duplicate suppression, independent
instances and cleanup/retry after success, sync/async failures and abort-triggered
callback rejection. Cancellation belongs to the supplied callback; no requirement
or permission to invent a new cancellation API or abort the caller's controller.
The requested verification and scope are explicit in the model-visible task.

Author-only tests/fixtures/panel_contract.mjs is not part of model input. Native
preflight verifies both original and corrected code pass the two existing tests;
the complete new contract passes correct code. Removing guard, cleanup or signal
forwarding produces native AssertionErrors, not a timeout/support exception.
Three preflight tests pass in 0.326s on installed Node v24.16.0. New JS helper's
seven native tests, independent-copy test and installer checks were previously
validated. Full local preflight: 469 tests pass in 70.708s, no failures/skips.
Repository validation and featured-language synchronization checks pass.

Schedule two fresh serial Astra medium sessions, baseline and explicit skill,
n=1 per arm, seed20260911, jobs1, 240 seconds/cell. This is a small adoption/
correctness/cost screen, not general proof of a gain. No helper is injected into
the no-skill project. Preserve every attempt, timeout, unknown usage, output gap,
scope issue and extra verification; no favorable-result retry or exclusions.
No resource/task edits or author test workloads during model timing.

After timing: review actual implementation and retained native test assertions,
both original tests unchanged, bounds, cleanup and original test output. Model
completion alone is not success. Reconcile raw usage/resources and complete file
inventories; use separate bounded copies for regression/fault replay. Replay
cannot fill original output gaps. Report differing extra work and shared host/
cache limitations. Update EN/KO status; existing charts stay fixed.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-javascript-panel-cases.json --output benchmarks/local-runs/hostage-javascript-panel-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
