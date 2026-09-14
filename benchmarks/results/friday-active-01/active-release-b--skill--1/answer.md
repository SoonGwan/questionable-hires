I’ll use the Friday skill to review the rollout and rollback order, then run the supplied SQL and reader queries in disposable in-memory SQLite databases. I’ll preserve all supplied files and report observed results separately from production unknowns.

**Blocked by evidence:** the exact order in `release.json` is locally incompatible. At **“rollback starts,”** the old reader becomes active before `down.sql` restores `name`, causing `OperationalError: no such column: name`.

I executed `python3 -B -` with an inline script using Python’s native `sqlite3` (**SQLite 3.51.0**) and one disposable `:memory:` database. The script loaded the literal `QUERY` constants using `ast`, executed each phase’s files and SQL in the specified order, and checked returned column names and exact rows. No dependencies, services, or scratch files were used.

Observed row sets:

```text
A = [(1, 'Ada'), (2, 'keep')]
B = [(1, '새 이름'), (2, 'keep'), (3, 'inserted')]
```

| Checkpoint | Execution result | Active reader: actual columns and rows |
|---|---|---|
| initial | `schema.sql` succeeded | Old: `['id', 'name']`, A — PASS |
| up after old drained | `up.sql` succeeded | New: `['id', 'label']`, A — PASS |
| new writes | Supplied UPDATE and INSERT succeeded | New: `['id', 'label']`, B — PASS |
| rollback starts | No schema/data change | Old: **FAIL**, `no such column: name` |
| rollback finishes | `down.sql` succeeded | Old: `['id', 'name']`, B — PASS |

The supplied writes executed exactly:

```sql
UPDATE people SET label='새 이름' WHERE id=1;
INSERT INTO people VALUES(3,'inserted');
```

At the failing checkpoint, a direct table query still returned `['id', 'label']` and B. I continued to the listed `down.sql` after recording the reader failure to assess recovery; this demonstrates SQL recovery, not that an actual release runner would continue after an error.

The final old-reader result proves preservation of the updated record `(1, '새 이름')`, untouched record `(2, 'keep')`, and inserted record `(3, 'inserted')`, including all identities and the required column names. No data-loss step was observed.

Inactive-reader probes also produced expected incompatibilities: the new reader failed with `no such column: label` initially and after rollback; the old reader failed with `no such column: name` after upgrade and new writes. Those are **not active-reader blockers** under the documented maintenance window. The old reader’s failure at “rollback starts” is an actual blocker because that reader is explicitly active.

The last compatible checkpoint before the failure is **“new writes.”** Data remains recoverable at the failure. The smallest ordering correction would be to keep readers drained during rollback, complete `down.sql`, then activate the old reader. That alternative was neither applied nor executed.

Production application writers, locking/concurrency, maintenance orchestration, runtime/configuration readiness, and staging remain unknown because evidence was not supplied. This review grants no deployment approval.

All project file hashes were unchanged after execution; no supplied files were modified.
