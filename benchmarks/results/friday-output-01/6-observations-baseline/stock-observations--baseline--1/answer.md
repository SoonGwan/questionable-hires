I’ll read the release instructions and supplied SQL, run each phase with both literal readers, and print the full JSON observation record. I’ll preserve the supplied files and Git state.

The contract makes both readers active at step 3 and requires quantity and reservation writes to survive step 5’s view rollback. I’ll use an in-memory SQLite database, compare full ordered results at all five phases, and record the readers’ source lines, exact SQL, and hashes.

The proposal first fails at **step 3**. OLD returns `A=7, B=3, C=0`, but requires `A=12, B=4, C=0`. Step 4 remains incompatible.

- **Last compatible checkpoint:** step 2. Its changed view is only temporarily compatible because reservations are zero.
- **Inactive error:** NEW at step 1 reports `no such column: reserved`; this is not a blocker.
- **Rollback:** step 5 restores OLD’s contract. Committed `(sku, quantity, reserved)` rows survive exactly: `(A,12,5), (B,4,1), (C,0,0)`.
- **Scoped mitigation:** keep `legacy_stock` exposing `quantity AS units` in `002.sql`; NEW already subtracts reservations itself. Not applied.

Executed all supplied SQL and both literal readers at all five phases. The complete, untruncated JSON record is in command output **`d9aff4`**, including ordered columns/full rows, actual errors, contracts, provenance, hashes, and completion information.

Files and Git state remained unchanged; no scratch, dependencies, external services, fixes, or deployment. Verification covers the specified SQL-only in-memory SQLite scope, excluding concurrency and crash recovery.
