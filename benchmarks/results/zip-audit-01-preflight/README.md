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
evidence. The six-cell runner still needs preparation/scheduling controls before
any model launch. Protocol and cases are fixed now; do not overwrite these records.
