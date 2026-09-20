I’ll read the release instructions and supplied SQL, then run the phase checks locally without changing the proposal or Git state.

**Reject the exact sequence:** step 3 is the first active-reader failure; step 2 is the last compatible checkpoint. Step 5 restores compatibility, but step 4 remains broken.

Executed the supplied SQL unchanged in Python’s standard-library SQLite 3.51.0, in memory, and ran both literal constants from `readers.py` at every phase:

| Phase | OLD | NEW | Stored data |
|---|---|---|---|
| 1 — `001.sql` | Pass, active | Inactive error: `no such column: reserved` | Pass |
| 2 — `002.sql` | Pass, active | Pass, inactive | Pass |
| 3 — `003.sql` | **Fail, active** | Pass, active | Pass |
| 4 — no SQL | **Fail, active** | Pass, inactive | Pass |
| 5 — `004.sql` | Pass, active | Pass, inactive | Pass; committed writes survive |

Compared complete ordered columns and rows, including zero values. Every successful query returned exactly `[sku, units]` and retained `('C', 0)`.

The decisive mismatch at steps 3 and 4 is OLD:
- Expected: `[('A',12), ('B',4), ('C',0)]`
- Observed: `[('A',7), ('B',3), ('C',0)]`

`002.sql` changes OLD’s view to subtract reservations. Zero reservations mask that change until step 3. Draining NEW and restarting OLD does not repair the view. Step 1’s inactive NEW error is not a blocker.

After rollback via `004.sql`, stored `[sku, quantity, reserved]` remained exactly `[('A',12,5), ('B',4,1), ('C',0,0)]`, matching the committed step-3 state.

**Scoped mitigation, not applied:** retain `quantity AS units` in `legacy_stock` throughout coexistence. NEW already calculates availability directly from `stock`. For recovery from step 3, restore the view before restarting OLD.

Verification is reproducible with `python3 -B`, standard-library `sqlite3.connect(':memory:')`, and `exec` of `readers.py` to obtain `OLD` and `NEW`. Execute files using `executescript` and commit in order `001`, `002`, `003`, no SQL, `004`; after each phase compare cursor column names and `fetchall()` against the contracts.

All file hashes, including `.git`, and Git status were unchanged across verification. No scratch, dependencies, external services, fixes, or deployment. Findings cover only the authored SQLite sequence and literal readers; concurrency, application runtime, and crash recovery are outside scope.
