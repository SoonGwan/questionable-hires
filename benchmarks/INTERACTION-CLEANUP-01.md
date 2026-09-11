# Interaction cleanup: cancellation is not termination

Author fault check of the actual retained protected-search test from screen 05.
No new model benchmark, fixture edits or production changes. The original test
bounds its dispatch waits but cancels then awaits tasks indefinitely in cleanup.

In a fresh subprocess, replace `Search.run` in memory with an implementation that
does not dispatch and catches CancelledError while continuing to wait. Invoke the
actual `test_search` unittest module. Its one-second dispatch deadline fires, but
cleanup waits forever: the author's three-second subprocess limit must terminate
it. Captured output confirms cancellation was requested while the task stayed live.

Running the same injected test with the existing author-side process wrapper and
a two-second deadline returns CLI 124, child -9, timed_out true, 2.007 seconds.
This demonstrates containment of the stalled check, not a stale-result defect and
not a model's successful fault handling. The helper is used only for author
verification here; Mother-in-law gains no cross-skill dependency.

The instruction change narrowly clarifies that cancellation is not termination,
cleanup must be covered by a process deadline when cancellation can be ignored,
and timeout is incomplete evidence. Existing local/browser runners remain the
preferred facilities. No universal harness or mandatory extra process is added.

The task criteria in screen 05 remain satisfied for the original implementation.
This adversarial check exposes a robustness limit beyond those criteria. The new
instruction has not been model-tested and establishes no token/time improvement.
