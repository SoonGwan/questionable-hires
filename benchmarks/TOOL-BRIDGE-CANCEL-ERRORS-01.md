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
