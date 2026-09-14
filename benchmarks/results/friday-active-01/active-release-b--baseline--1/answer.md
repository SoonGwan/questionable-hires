I’ll read the release plan and requirements, then execute the SQL in disposable in-memory SQLite databases and check the readers at each reachable state.

**The local plan is incompatible with the required reader contract.** Its first failure is phase 4, **“rollback starts”**: `old_reader.py` becomes active before `down.sql` restores `name`.

Executed command: `python3 -B - <<'PY' … PY` using Python’s native `sqlite3` module, SQLite **3.51.0**, and one shared `:memory:` database. The harness read `release.json`, executed supplied files and inline SQL in order, extracted literal reader queries, and checked returned column names and exact rows.

Observed row sets:

- **A:** `[(1, 'Ada'), (2, 'keep')]`
- **B:** `[(1, '새 이름'), (2, 'keep'), (3, 'inserted')]`

| Phase | Execution and active reader result |
|---|---|
| 1. initial | `schema.sql` succeeds. Old reader returns columns `['id', 'name']`, rows **A**. |
| 2. up after old drained | `up.sql` succeeds. New reader returns `['id', 'label']`, rows **A**. |
| 3. new writes | Supplied UPDATE and INSERT succeed. New reader returns `['id', 'label']`, rows **B**. |
| 4. rollback starts | Old reader fails: `OperationalError: no such column: name`. Stored columns remain `['id', 'label']`, with rows **B** intact. |
| 5. rollback finishes | **Diagnostic continuation after failure:** `down.sql` succeeds. Old reader returns `['id', 'name']`, rows **B**. |

The failing query was:
```sql
SELECT id, name FROM people ORDER BY id
```

Inactive probes also failed as expected: the new reader at phases 1 and 5 (`no such column: label`), and the old reader at phases 2 and 3 (`no such column: name`). Those are **not release failures**, because those readers are inactive. Phase 4 is different: its incompatible reader is explicitly active.

The SQL preserves the updated record `(1, '새 이름')`, untouched record `(2, 'keep')`, and inserted record `(3, 'inserted')`, including their identities, through the diagnostic rollback. Successful value recovery does not cure phase 4’s reader failure.

Production application writers, locking, maintenance orchestration, staging behavior, and production SQLite compatibility remain unverified. This review provides no deployment approval.

All supplied files remained unchanged, verified by SHA-256 comparisons. No scratch files, dependencies, external services, or deployment actions were used.
