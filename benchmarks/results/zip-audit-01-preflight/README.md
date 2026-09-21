# ZIP audit01 — author fixture controls only

2026-09-21. [Frozen task/protocol](../../ZIP-AUDIT-01-PROTOCOL.md),
[generated model cases](../../zip-audit-01-cases.json),
[native observations](native-controls.json).

No model sessions have run. Three actual sources (normal, omitted permission
assignment, independently emptied payload) each pass a fresh public import.
Original native tests pass2/2on all sources; the stronger complete-record test
passes normal source and fails each fault with an actual record mismatch.
Bindings are checked in the native test processes and source preservation is
checked after each run. The stronger test is author-only, not in model cases.

Two fixture tests pass on Python3.9.6 and3.11.16. This is a newly authored,
author-inspected development project, not independent model quality/efficiency
evidence. Protocol and cases are fixed now; do not overwrite these records.

Runner checkpoint`47fe7cf`: checkout10tests pass in1.174s; fresh source archive
discovers10,9pass/1historical-resource skip in0.428s. Scheduling tests exercise
synthetic resources, including executable modes, without model calls. The separate
historical check verifies every pinned file/mode and that only the entrypoint and
native-batch reference differ between prior and candidate. Duplicate execution,
source/resource/settings drift, account-limit stop and interruption-before-return
are controlled. Both fixtures' real native preflight runs again during preparation.

The six-cell manifest and pinned resources are prepared in ignored
`benchmarks/local-runs/zip-audit-01`. At this checkpoint the execution marker is
absent and no model cell has started. Use the existing prepared directory once;
do not recreate it or resume a partial schedule. The frozen identities include
the actual builder, case JSON, runner, protocol, launcher and both test files.
