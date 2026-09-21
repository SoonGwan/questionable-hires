# Receipt versions01: development comparison preparation

2026-09-22; implementation resource `e075bdb`, predecessor `efc1439`.
**Prepared fixtures only; no model calls or efficiency measurements.**

## Mechanism and limits

Receipt now optionally compares several historical implementations with one
current native run. Test whether that capability is useful in actual model work,
without requiring helper adoption. Two author-created scheduling-window tasks
share exactly the same three-commit project and six current unittest assertions.
The single task requests parent/current; the multiple task requests both old
versions/current. The only task difference is the requested revision list.
These are correlated development cases, not two independent holdouts. Their
small native suites may offer negligible time savings; no gain is assumed.

Planned conditions: no skill, predecessor Receipt, current Receipt; explicit
Receipt exposure for the two skill conditions, not automatic-routing evidence.
Planned order: single baseline/predecessor/current, then multiple
current/predecessor/baseline. One attempt per cell, six scheduled cells total,
GPT-6 Astra medium, one active session, 360-second cell limit. Freeze runner,
resource hashes, runtime, tasks and criteria before launch. No launch is yet
authorized by this preparation artifact alone; use the existing exclusive
scheduler and its frozen manifest, not an ad-hoc execution loop.

Compare total tokens including cached input and process elapsed time, retaining
every attempt, timeout and missing observation. Review each task's native
outcomes, copy-local same-process imports, full revisions, preservation and
cleanup before interpreting cost. Report per-task results and totals; no
confidence or general20–30% claim from n=1. Different valid implementation
strategies are allowed, including custom harnesses and repeated current checks.
Native process counts are descriptive, not a substitute for model costs.

## Author preflight

`tests/test_receipt_versions_cases.py`, Python3.11.16:

- Checkout:2 tests pass (0.931s).
- Fresh source archive plus the two new files:2 tests pass (0.906s), without
  repository history or local-run artifacts in that archive.
- Fresh public-module import succeeds using the same selected interpreter.
- Oldest native suite:6 tests,2 actual assertion failures (touching/nested).
- Parent native suite:6 tests,1 actual assertion failure (nested).
- Current native suite:6 tests,0 failures. Actual differing interval values are
  asserted in failure output; no support-code exception is accepted as a defect.
- Helper output identifies copy-local imports and full commits; each requested
  native check completes without truncation/timeout. Complete original tree
  bytes/modes remain identical, and comparison copies are removed.

These are author checks of the fixture/helper, not model observations.

## Exclusive runner validation

`run_receipt_versions_01.py` reuses the existing exclusive scheduler, with two
byte/mode-exact pinned Receipt snapshots and an empty baseline resource tree.
It freezes tasks, resource digests, settings, interpreter/dependencies and CLI
version. Preparation captures the native fixture test output and rejects a
working helper that differs from the pinned current helper. Execution rechecks
frozen inputs, retains completed cells, stops at a detected limit and rejects
restarts even when the first interrupted attempt produced no result.

Nine runner tests pass in checkout. Combined fixture/runner archive checks:
10 pass,1 historical-resource check skipped because the archive has no history.
Synthetic checks exercise all six scheduled calls, both resource mutations,
runtime/settings changes, mid-schedule changes, limits and stale restarts; they
do not call the model. Freeze the final manifest before execution. Existing
featured graphs and claims remain unchanged.
