# Model follow-up: cleanup deadline adopted

Mother-in-law `d45a215`, execution HEAD `caed139`. One fresh Astra-medium skill
session on the existing protected-search development case. No retry, baseline
rerun or full-team screen. Raw evidence: ignored `local-runs/interaction-cleanup-02`.

Current: **68,299 tokens / 45.910 seconds**. Screen 05: **67,322 / 41.627**.
That is 1.5% more tokens and 10.3% more time. This is verified failure containment
with increased observed cost, not a performance win. Single separated samples
cannot isolate causality.

The retained test controls two overlapping requests in both completion orders,
asserts the actual result state, and reports no defect for the generation guard.
It releases outstanding controlled responses during cleanup and awaits tasks
through a one-second asyncio deadline. More importantly, the actual execution
command wraps unittest in `subprocess.run(..., timeout=5)` and maps its timeout
to exit 2 with an explicit INCOMPLETE message. It does not install or read another
skill/helper. No browser-rendering claim or production change.

Author fault check injects a no-dispatch, cancellation-resistant Search.run only
in memory. It runs the actual generated unittest through the generated wrapper's
same five-second deadline/error handling, changing the child entrypoint to inject
the fault. The wrapper terminates with exit 2 and the INCOMPLETE message, without
requiring the author's separate eight-second outer limit. This is containment of
an incomplete test, not a reproduced stale-result defect or a model-run fault test.

Separate author replay of the normal test passes. Original search.py and both
installed skill resources match fixture inputs and `d45a215`. The original model
trace contains the successful two-order test output, no rejected patch and no
capture diagnostic. The deadline is in the execution command, not the retained
test file: directly rerunning that file alone does not inherit it. This handoff
limitation remains; do not claim the artifact is self-bounding in every invocation.

Disposition: the conditional cleanup guidance is followed in this sample, with
honest failure status and no cross-skill dependency. Keep the observed cost increase
and artifact limitation. The broad efficiency objective remains unmet.
