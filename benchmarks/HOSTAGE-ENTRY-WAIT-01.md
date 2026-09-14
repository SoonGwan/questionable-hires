# Task-aware callback entry: avoid waiting after application settlement

2026-09-14, parent `11122f3`. Optional JavaScript runtime capability, not a model
benchmark. [Prior model replay](HOSTAGE-COPY-CHECK-MODEL-01-REVIEW.md) exposed eight
skipped-decode failures detected only after one-second deadlines.

## Capability and limits

`callback.startedBefore(task, timeoutMs = 1000)` waits for the next queued/observed
callback entry, but rejects when the supplied task settles first. Its error has
code `ERR_CALLBACK_NOT_ENTERED` and an `outcome` containing `status` and the exact
fulfilled `value` or rejected `reason`, including undefined/null. This diagnoses
a missing expected entry instead of spending the whole deadline on a finished
application task. Existing `started()` behavior and lifecycle ownership remain.

Use only when the selected callback is required before that task finishes. Queued
entries take precedence; this is observation order, not proof of callback/task
causality. The test chooses the right task and asserts actual arguments, state
and outcome. No task is cancelled or force-settled. A genuinely pending task still
needs the deadline. Promise settlement handlers cannot be detached from a pending
task; tests still own its eventual settlement/cleanup.

Six native tests exercise exact success/rejection identity, queued and future
entries, FIFO and waiter removal, pending-task deadline, scope closure and an
actual two-stage operation with/without its second callback. The missing-entry
control yields the structured early-settlement error, not a timer failure.
Five Python integration tests pass, including the earlier 17 native JS checks,
six new native checks, standalone execution and copy-integrity controls.
Full local suite: **483 tests passed in 67.999s**, no failures/skips.

## Retained-test adaptation — author evidence only

`probe_hostage_entry_wait.py` copies the prior model project without changing any
frozen evidence. It changes only `.started()` calls to `.startedBefore(task)` for
their corresponding application task and substitutes the new asset. All app
assertions stay unchanged. Original and adapted tests run against both final
code and the same deliberately skipped-stale-decode defect, in disposable copies.

The [first attempt](results/hostage-entry-wait-01/attempt-01.json) contains an
author transformation bug: substring replacement of `r.fetch` also changed
`br.fetch` to reference undefined `r.task`. Adapted final was 42/43, faulty 34/43;
that is not acceptable evidence of correct adaptation. It is retained in full.
The script now matches expression boundaries and explicitly maps `br.task`.

The [corrected attempt](results/hostage-entry-wait-01/attempt-02.json) records:

| Wait mode | Final pass/fail | Fault pass/fail | Final seconds | Fault seconds |
|---|---:|---:|---:|---:|
| Original deadline-only | 43 / 0 | 35 / 8 | 0.0958 | 8.1120 |
| Task-aware entry | 43 / 0 | 35 / 8 | 0.1004 | 0.1024 |

All 43 tests are discovered, zero skipped/cancelled. Eight missing-decode checks
now emit `ERR_CALLBACK_NOT_ENTERED`; original checks hit controlled-call deadlines.
The exact adapted source, source hashes and full outputs are retained. The source
project is unchanged. Process timeout is 30 seconds for each author run.

This corrected native probe overlapped the author full regression suite, not any
model timing; n=1 and host load prohibit precise speedup claims. It demonstrates
removal of eight unnecessary deadline waits, not a broad efficiency percentage.
Correct-code execution is not faster here. No new model has adopted this API yet,
and added asset size may have a token cost. Featured figures stay unchanged.
