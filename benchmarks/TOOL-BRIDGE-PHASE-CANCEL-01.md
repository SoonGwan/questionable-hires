# Direct tool phase cancellation01 — native prototype, 2026-09-28

Source parent `026a8312`. No model calls, ordinary skill edits or registration.
The [model approval failure](RECEIPT-BRIDGE-ROUTE-01-REVIEW.md) remains unresolved;
this local SDK lifecycle control neither changes nor bypasses that model gate.

Before execution: compare unchanged HTTP cancellation behavior against a launch
flag checking cancellation before/after each native `run_check`. Both arms use the
same isolated adapter with identical phase logging. The current subprocess drains
under existing native cleanup; the candidate unwinds through `compare`'s original
finally guards/copy cleanup before another version begins. It does not kill an
active subprocess or abandon its worker. Ordinary helper code is unchanged.

[AnyIO's worker cancellation API](https://anyio.readthedocs.io/en/stable/threads.html#reacting-to-cancellation-in-worker-threads)
supports cooperative checks inside workers. This motivates the prototype; actual
SDK cancellation and recovery, not documentation alone, must establish behavior.

Fixed four native cells: baseline active, candidate active, candidate queued,
baseline queued. Reuse the six-test Windows fixture with an explicit0.4-second
native setup delay. A real native marker must exist and no phase may have finished
before the actual cancellation notification. After cancellation error, use the
same session/server for complete before1/after0 recovery; retain all native outputs,
seven complete v3 observations/check, originals/modes and scratch removal. Inspect
actual phase starts/ends: canceled active baseline2 versus candidate1; queued
cancellation launches none, and both first/recovery comparisons run2 phases.
No timing threshold; cancellation-to-recovery includes the authored fixture delay
and recovery itself, not model efficiency. Existing SDK/client bounds remain.

[Server](results/tool-bridge-phase-cancel-01/server.py) and
[control](results/tool-bridge-phase-cancel-01/control.py) are isolated prototypes.
The launch-local serialized helper binding is wrapped; no global SDK patch.
Record every failure without overwriting prior results. No claim about arbitrary
thread interruption, larger batches, host deadlines, abrupt loss, SIGKILL or all8
performance. Inspect exception cleanup and incomplete-result handling before any
future adoption. The model approval gate remains a separate prerequisite.
