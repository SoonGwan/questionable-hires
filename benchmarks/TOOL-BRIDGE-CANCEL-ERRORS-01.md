# Direct tool cancellation errors01 — fixed native controls, 2026-09-28

Parent`48f837fc`; unchanged [phase-cancellation candidate](TOOL-BRIDGE-PHASE-CANCEL-01.md).
No model/permission/ordinary skill changes. Inspect two previously unverified
intersections: actual cancellation while the native first phase times out, and
actual cancellation while the native test modifies an original watched source.
All sources/faults are in author-owned disposable projects, not user code.

[Control](results/tool-bridge-cancel-errors-01/control.py) keeps the same HTTP/SDK,
current helper, module invocation and six-test Windows fixture. A native PID marker
must confirm live execution before canceling. Timeout uses1-second native bound
against10-second setup; guard case waits0.4 seconds then appends a known comment
to its owned original `windows.py`. Wait for native PID termination and copy removal,
record actual phases and changed originals, require a visible guard failure for the
mutation case, and perform same-session recovery after explicit **author reset**
of the intentionally faulty test/source fixture. This is not adapter restoration.

Recovery must retain actual before1/after0, six tests/no skips, seven complete v3
argument observations, preserved originals and cleanup. Keep all initial errors,
including unavailable recovery, without overwriting or replaying the same outcomes.
Record listener termination. Cancellation acknowledgement alone is not cleanup,
original preservation, a native result, or a successful repair. The separate model
approval boundary remains unchanged; this does not certify full RPC deadlines,
abrupt client loss, hard kills, cross-instance ownership or all8 efficiency.

## Actual first execution — guard case fails

Frozen control **`07ca4ddb`**, unchanged adapter from`915d7f81`.
[Results](results/tool-bridge-cancel-errors-01/results.json) and
[control log](results/tool-bridge-cancel-errors-01/control-reading.txt) retain both
scheduled cases. Timeout passes: native process exits−9 at the1-second bound,
copies are removed, no original changes, then the explicitly reset fixture has a
complete same-session native1/0 recovery. This is not a result for the canceled call.

Guard case **fails**. The native process and owned copies are gone before author
intervention; original `windows.py` contains the intended controlled change.
The original-change diagnostic is not visible. Instead the retained
[server log](results/tool-bridge-cancel-errors-01/guard-server-reading.txt) shows
`Request already responded to`, the HTTP session crashes and later session
termination receives404. No recovery call was made: the diagnostic assertion
failed first. The owned fixture is removed by author cleanup, not restored by the
adapter. Both listeners are awaited terminal with exit−15. No child remains live
at the recorded cleanup check.

The worker raises cancellation after native completion, but `compare`'s finally
can raise a guard error instead. Unlike the normal-return path, the adapter has
no cancellation checkpoint for that error path. The SDK attempts an error response
after it already sent cancellation. This source reading plus actual double-response
trace motivates an error-path checkpoint; it is not proof that a fix works.
Preserve this failed candidate and validate a changed adapter separately. Do not
weaken the guard or claim that source corruption was repaired automatically.
