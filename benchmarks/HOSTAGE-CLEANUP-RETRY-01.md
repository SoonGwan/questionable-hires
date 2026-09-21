# Owned task cleanup retry — reproduced defect and correction

2026-09-21, parent `d04d40e`. Actual Python asset behavior, not a model performance
comparison. No benchmark task or existing assertion was weakened.

`OwnedTasks.close()` previously called `task.cancel()` on every unfinished task
on every invocation. When the first cancellation entered an asynchronous `finally`
block that awaited resource cleanup, a second close could inject another
`CancelledError` into that block. The task then terminated without completing its
cleanup; the second close returned because nothing remained pending.

Two new native asynchronous tests reproduce the issue: retry after the first
close times out, and a concurrent second close while the first is draining. Both
fail on the parent asset because the second close returns rather than retaining
the unfinished cleanup. Test-owned release gates prevent leaked pending work.

Correction: only the first close sends cancellations, atomically with marking
the owner closed before any await. Later/concurrent calls continue bounded waits
and exception retrieval on the same registered tasks. New starts remain rejected.
The tests verify continued pending state before release, actual completion of the
`finally` cleanup afterward and cancellation outcome. No cancellation-identity
requirement, global task sweep, task replacement or unbounded wait is added.

After correction, all11 ownership tests pass on Python3.9/3.11, including existing
standalone native tests and correct/faulty/valid-alternative application controls.
The16 controlled-call tests and4 source-archive/install tests pass on Python3.9.
English/Korean capability rows and complete asset usage block are synchronized.

This prevents helper-originated repeated cancellation; it cannot stop unrelated
external cancellations or guarantee successful application cleanup. A task that
ignores cancellation indefinitely still times out and remains unfinished. It is
not a process deadline, general speed gain or evidence that all eight skills beat
the baseline. Existing model artifacts/graphs remain frozen.
