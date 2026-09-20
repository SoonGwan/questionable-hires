I’m using the Friday skill to run the supplied SQL and literal readers in isolation, compare each phase with its contracts, and check rollback survival without changing the project.


**Blocked by evidence:** OLD fails at phases 3 and 4. Phase 5 restores compatibility without losing committed data.

| Phase | OLD | NEW |
|---|---|---|
| 1 — `001.sql` | Pass, active | Inactive error: `no such column: reserved` |
| 2 — `002.sql` | Pass, active | Pass, inactive |
| 3 — `003.sql` | **Fail, active** | Pass, active |
| 4 — restart OLD, no SQL | **Fail, active** | Pass, inactive |
| 5 — `004.sql` | Pass, active | Pass, inactive |

At phases 3–4, OLD expects `[(A,12),(B,4),(C,0)]` but returns `[(A,7),(B,3),(C,0)]`. `002.sql` changes the legacy view to subtract reservations; zero reservations initially mask that semantic incompatibility. **Phase 3 is the first observed failure; phase 2 is the last compatible checkpoint for the supplied data.** Restarting OLD does not repair the view. Phase 1’s inactive NEW error is not a blocker.

All successful queries returned exactly ordered columns `[sku, units]`, with complete lexical rows including `(C,0)`. After phase 5, committed `(sku,quantity,reserved)` remained exactly `[(A,12,5),(B,4,1),(C,0,0)]`: recovery passes.

Scoped mitigation: preserve total-quantity semantics in `legacy_stock` before phase 3 writes and throughout OLD activity. NEW already computes availability directly. Moving restoration only before the phase 4 restart would leave phase 3 broken. No mitigation was applied.

Verification used Python’s standard-library SQLite **3.51.0**, one `:memory:` connection, unchanged SQL via `executescript` in order `001 → 002 → 003 → no SQL → 004`, and both literal **`readers.py:OLD` and `readers.py:NEW`** at every phase. Full column/row equality and committed base-table values were checked. Scope is the authored SQL-only contract; no runtime, concurrency, crash-recovery, or other-engine assurance.

Project hashes and Git status/diffs were unchanged; no scratch, dependencies, external services, or deployment.
