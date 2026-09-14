# Keyed import contract transfer — screen 01

2026-09-14, resources `c0aa9a1`. One explicit-skill Astra medium session,
one job, seed 20260911, 240 seconds; no favorable retry. New authored task
`hostage-keyed-import-cases.json`, SHA-256
`b3e35518b205ffb535c15bec6b03ccfe896c2af70094cf41c79fd27918e29880`.
No model session has previously received this task. It is nevertheless an
author-designed transfer check, not an independent real-developer trial.

The prior Python form result invented a duplicate None-return assertion. The
candidate instruction distinguishes existing/specified outputs from new
suppression paths. This task changes the owner to a keyed, two-stage importer:
two distinct keys may proceed concurrently, but same-key overlap during either
phase must be suppressed. Exact active result/error/payload semantics remain.
The task explicitly leaves duplicate results unspecified to avoid an ambiguous
test contract. Success therefore cannot isolate the skill sentence's causal
effect from the task clarification; no baseline or efficiency claim is planned.

Preflight: `tests/test_hostage_keyed_import_fixture.py` executes the supplied two
native tests against the actual original and a deliberately discarded persist
result. Original: two pass. Fault: one pass/one intended identity failure,
`None is not <object ...>`, not a support exception. Scratch is project-local and
removed. Serialized fixture matches generator. No custom assertion helpers.

Review every stated transition and frozen criterion, not just test totals.
Check actual key equality/ownership, duplicate timing, separate instances,
arguments/results/errors, synchronous/async failures and cancellation in both
phases, retry, bounded waits and owned cleanup. Record actual API use and copied
asset identity. Preserve initial failures, tool errors, full reads and capture
gaps. Reconcile raw usage, resources, original files and complete project inventory.
Do not alter resources/tasks or run author test workloads during model timing.

After completion replay generated tests unchanged against the final code, original
code, a valid alternate duplicate result and narrow missing-guard/missing-cleanup/
global-key-blocking faults when transformations match the actual implementation.
All replays use disposable project-local copies and 20-second process bounds.
Retain each actual result, intended failure and discrepancy; author output cannot
replace original model evidence. Broad quality or efficiency remains unproven.
No featured graph or historical result changes.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-keyed-import-cases.json --output benchmarks/local-runs/hostage-keyed-import-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
