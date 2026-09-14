I’ll use the Friday skill to inspect the release order and reader contracts, then execute the reachable forward and rollback states in disposable in-memory SQLite databases. I’ll preserve all supplied files and report the observed results and production unknowns.

The plan uses a maintenance window: old readers are drained before the rename, and rollback restores `name` before the old reader runs. I’ll check the active readers at each checkpoint and separately probe inactive readers so their expected incompatibilities don’t count as rollout failures.

**Ready for the scoped local SQL plan.** The exact `release.json` sequence passed on SQLite **3.51.0**, including new-version writes and rollback. This is not deployment approval.

Executed command: `python3 -B - <<'PY' … PY` with an inline standard-library harness that extracted the literal `QUERY` constants, executed each phase’s files and SQL in order on one `sqlite3.connect(':memory:')` database, and asserted exact reader columns and rows. Exit code: **0**.

Actual active-reader observations:

| Checkpoint | Columns | Rows |
|---|---|---|
| initial | `id, name` | `[(1, 'Ada'), (2, 'keep')]` |
| up after old drained | `id, label` | `[(1, 'Ada'), (2, 'keep')]` |
| new writes | `id, label` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |
| rollback starts | `id, name` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |
| rollback finishes | `id, name` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |

All supplied SQL succeeded. **No failing active-reader or SQL step was observed.** Rollback preserved the updated record, untouched record, inserted record, and all identities. No irreversible step was observed through final recovery.

Separate inactive-reader probes failed as expected:

- New reader before migration and after rollback: `OperationalError: no such column: label`.
- Old reader after migration, including after writes: `OperationalError: no such column: name`.

These are inactive incompatibilities under the documented maintenance order, not release blockers. Compatibility depends on enforcing that order.

Production application writers, locking/concurrency, maintenance orchestration, production runtime/configuration, and staging behavior remain unverified. No production recovery or backup restore was tested.

File-content hashes matched before and after execution. No scratch files were created; no dependencies, external services, or deployment actions were used.
