I’m using the Friday skill to execute the supplied SQL and readers in isolation, check each phase against its contracts, and assess rollback without changing the proposal or Git state.

**Blocked by evidence.** Step 3 first violates an active reader’s contract; step 2 is the last compatible checkpoint for the supplied data.

Executed the unchanged SQL using Python’s standard-library SQLite 3.51.0 in memory, and executed both literal constants from `readers.py` at every phase:

| Phase | OLD | NEW |
|---|---|---|
| 1 — `001.sql` | Pass, active | Inactive error: `no such column: reserved` |
| 2 — `002.sql` | Pass, active | Pass, inactive |
| 3 — `003.sql` | **Fail, active** | Pass, active |
| 4 — drain NEW/restart OLD, no SQL | **Fail, active** | Pass, inactive |
| 5 — `004.sql` | Pass, active | Pass, inactive |

All SQL succeeded. Every successful query returned the required ordered columns `[sku, units]`; comparisons checked complete ordered rows, including `('C', 0)`.

- **Decisive mismatch, phases 3–4:** OLD expected `[('A',12), ('B',4), ('C',0)]`, but observed `[('A',7), ('B',3), ('C',0)]`. Step 2 changes `legacy_stock` to subtract reservations; zero reservations conceal the incompatibility until step 3’s writes. Restarting OLD does not restore its semantics.
- **Rollback survival passes:** After step 5, stored `(sku, quantity, reserved)` rows remain `[('A',12,5), ('B',4,1), ('C',0,0)]`, exactly matching committed step 3 data. OLD recovers; NEW still passes. Phase 1’s inactive NEW error is not a blocker.

**Scoped mitigation:** Keep `legacy_stock.units` mapped to total quantity before step 3; NEW already calculates availability directly. For recovery from step 3, restore that view before restarting OLD. Neither change was applied or tested.

Reproduction uses `sqlite3.connect(':memory:')`, unchanged files via `executescript` in order `001 → 002 → 003 → no SQL → 004`, and `readers.py` constants `OLD` and `NEW` via `execute` at each phase, comparing cursor columns and complete fetched rows.

This establishes only the authored SQLite contract. File hashes and Git HEAD/status/diffs remained unchanged; no scratch, dependencies, external services, or deployment were used.
