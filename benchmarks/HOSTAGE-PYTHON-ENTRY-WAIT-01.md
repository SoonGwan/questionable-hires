# Python task-aware callback entry — 2026-09-14

Parent `4ca29d1`. The optional Python callback asset now supports
`await callback.started_before(task, timeout=1)`, matching the practical use case
of the [JavaScript capability](HOSTAGE-ENTRY-WAIT-01.md), not its cancellation API.
This is local behavioral validation, not a fresh model or efficiency benchmark.

## Demonstrated need and contract

A native reproducer finishes an application task without calling its callback.
The existing `started()` still waits until its deadline. The new method instead
raises `EntryNotObserved` when the selected task completes, fails or is cancelled
before entry is observed. Its outcome preserves exact returned object/exception
references, or a cancelled status. Original `started()` remains available.

The task must already be owned by the test, on the same event loop. Passing a
coroutine does not schedule it implicitly. The test still owns exception handling,
application assertions, task cancellation and draining. Queued entry wins; this
is not proof that a particular task caused that entry. Genuine pending work still
requires the deadline, and async deadlines cannot interrupt blocking code.

The implementation waits for an entry notification and only then consumes the
queue in the caller. Cancelling an internal queue-get task could otherwise lose
an entry already consumed before cancellation reaches the caller. The notification
task is always cancelled/drained; application tasks are never cancelled by this
method. Competing waiters recheck queue and task state after notification.

## Native verification

`tests/test_controlled_call_asset.py`: **16 tests passed in 0.241s**. New checks
cover the old deadline-only behavior, exact completed/failed/cancelled outcomes,
queued/future entry with argument/result identity, waiting-side cancellation and
timeout without cancelling the application, cancellation during entry wakeup,
competing consumers, invalid task/loop/deadline, and application-side cancellation.

A two-stage operation passes with correct payload/result identities; deliberately
skipping decode raises the early-entry assertion carrying the actual completed
payload, within a one-second outer bound despite a 30-second entry deadline.
The existing real Form guard/cleanup checks and old callback tests remain. The
standalone-copy test now exercises the new method without an installed skill.

The prior AST-equality test covered a historical documentation-only move and is
removed because this revision intentionally changes runtime behavior. It is not
a performance or compatibility oracle; existing observable behavior checks stay.
Frozen benchmark assets and measurements remain unchanged.

Full repository suite: **494 tests passed in 68.746s**, no failures/skips.
Skill validation, repository links/metadata and featured-language checks pass.

No Python model has adopted this new method yet. Added source can cost tokens;
no task-wide or 20–30% gain is claimed. No featured chart update.
