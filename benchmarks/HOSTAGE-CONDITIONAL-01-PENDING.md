# Conditional Hostage comparison — six sessions complete, full review pending

2026-09-21, launch `1b26f9d`, resources `a1f420e`.
[Frozen protocol](HOSTAGE-CONDITIONAL-01-PROTOCOL.md). All six original attempts
completed without timeout/account limit; runner is terminal. Do not restart.

| Task | Arm | Total tokens, cached input included | Wall seconds |
| --- | --- | ---: | ---: |
| Synchronous |Prior|90783|54.256|
| Synchronous |Baseline|62605|43.651|
| Synchronous |Candidate|88901|54.622|
| Async |Candidate|117980|107.225|
| Async |Baseline|122875|121.619|
| Async |Prior|123861|118.823|

These are process measurements, not final task-success scores. Candidate reads
the conditional guide for async work and not for the synchronous task. Async
candidate/prior each repair a test-harness retained-reference failure before a
passing suite; all work remains included. Initial synchronous review verifies
existing-test/scope preservation and original native6/7/7 passing counts for
baseline/prior/candidate; no supplementary rerun substitutes for those records.

## New supplementary finding, after all timed sessions

The task explicitly forbids caching completed results. A newly scheduled caller
can run after the fetch task completes but before its cleanup callback executes.
The candidate and prior only check whether an in-flight entry exists, returning
that completed result in this window. Baseline also checks `task.done()` and starts
a new fetch. The author preflight reference has the same omission as both skill
deliveries: its original green checks were not exhaustive.

[Separate native author observations](results/hostage-conditional-01-author-gap.json)
record1 fetch /same object for candidate, prior and author reference, versus2
fetches /distinct result for baseline. All verify that the original fetch is
already done at re-entry. The [probe](probe_completed_fetch_gap.py) runs copied
delivered modules, asserts local import binding, and records the actual assertion
failure. It is not a model-run test or new model attempt. Originals, frozen task,
preflight reference and schedule are unchanged. A regression test rejects that
reference and accepts only adding the completed-task check, on Python3.9/3.11.

This finding prevents claiming full async correctness for either skill delivery.
Do not silently fix the frozen reference, relabel the preflight, exclude this
boundary or rerun until favorable. The criterion existed before measurement;
the author probe is explicitly post-run evidence and must stay separate.

Outstanding: finish all native assertion/binding/capture/scope review, apply frozen
criteria to each original outcome with this supplementary limitation, and export
all redacted attempts. No candidate promotion, featured chart change or all-eight
efficiency claim. Two authored tasks,n=1,fixed order/shared host/cache remain limits.
