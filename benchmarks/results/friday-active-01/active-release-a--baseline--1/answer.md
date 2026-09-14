I’ll read the release plan and requirements, then run the supplied SQL and reader queries in disposable in-memory SQLite databases. I’ll preserve all supplied files and report observed failures separately from production unknowns.

The local SQL plan is **compatible** with `release.json` and `requirements.md`. All five phases were reachable; no supplied SQL or active reader failed.

Executed command: `python3 -B - <<'PY' … PY` using Python’s native `sqlite3` module, SQLite **3.51.0**, and one shared `:memory:` database. The harness executed each phase’s files, then SQL, then literal reader `QUERY` constants in the declared order, asserting exact column names and rows.

Actual observations:

| Phase | Active reader | Exact columns | Exact rows |
|---|---|---|---|
| initial | old | `['id', 'name']` | `[(1, 'Ada'), (2, 'keep')]` |
| up after old drained | new | `['id', 'label']` | `[(1, 'Ada'), (2, 'keep')]` |
| new writes | new | `['id', 'label']` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |
| rollback starts | old | `['id', 'name']` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |
| rollback finishes | old | `['id', 'name']` | `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]` |

The supplied update and insert succeeded. Rollback preserved the updated record, untouched record, inserted record, and all three identities.

Additional inactive-reader probes produced actual failures:

- New reader before migration and after rollback: `OperationalError: no such column: label`.
- Old reader after migration, including after new writes: `OperationalError: no such column: name`.

These are **inactive incompatibilities**, not failures of the documented maintenance-window plan. Every listed active reader passed. **First failing planned step: none.**

Production remains uncertified: actual application writers, production SQLite environment, locking, maintenance orchestration/draining, and staging were not tested. This result is not deployment approval.

All project file paths and SHA-256 contents were unchanged. No scratch files were created; the in-memory database was closed.
