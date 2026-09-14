I’ll use the Friday skill to review the rollout and rollback states, then execute the supplied SQL and reader checks in disposable in-memory SQLite databases. I’ll preserve all supplied files and keep the review local.

The plan uses a maintenance window: old readers are drained before the rename, and the down migration runs before old readers resume. I’ll check exact columns and values at every checkpoint, including all three records after the new writes, and probe inactive readers separately.

**Ready for the scoped local SQL contract.** The exact order in `release.json` passed on SQLite 3.51.0. This is not deployment approval.

Executed command: `python3 -B - <<'PY' … PY` using Python’s native `sqlite3.connect(':memory:')`. The inline runner read the supplied SQL and literal `QUERY` constants, executed all five phases on one database, and asserted exact column names and rows.

Actual observations:

| Checkpoint | Active reader | Columns | Exact rows |
|---|---|---|---|
| Initial | Old | `id, name` | `[(1, 'Ada'), (2, 'keep')]` |
| Up after old drained | New | `id, label` | `[(1, 'Ada'), (2, 'keep')]` |
| New writes | New | `id, label` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |
| Rollback starts, after down | Old | `id, name` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |
| Rollback finishes | Old | `id, name` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |

All supplied SQL succeeded. **First failing planned step: none.** Rollback preserved the updated, untouched and inserted records, including their identities and exact values. No irreversible step was observed; the final state retained all required data.

Separate inactive-reader probes produced these actual failures:

- New reader before up and after down: `OperationalError: no such column: label`.
- Old reader after up, including after new writes: `OperationalError: no such column: name`.

These are inactive incompatibilities, not rollout blockers under the documented maintenance-window ordering. That ordering must hold: old readers must remain drained while `label` exists, and new readers must be inactive after down.

Production application writers, locking, maintenance orchestration, runtime/configuration compatibility and staging remain unverified. No services were contacted or dependencies installed. All 13 non-git project files were hash-verified unchanged; no scratch files were created.
