I’ll use the Friday skill to execute the supplied SQL and check both readers at every checkpoint, including rollback write survival, without changing any files.

**Blocked by evidence at step 2.** `002_up.sql` renames the returned `label` column to `title` while OLD remains active. OLD’s SELECT succeeds, but its consumer contract fails.

Executed `python3 -B - <<'PY' … PY` using the supplied Friday `sqlite_matrix.py` API: one disposable in-memory database, the actual SQL files in proposal order, a no-change checkpoint at step 4, and both literal queries from `readers.py` at every checkpoint. All five phases completed; results were untruncated. Assertions checked ordered columns, complete rows, and native BLOB bytes.

| Step | Observed columns for successful queries | Complete rows | OLD | NEW |
|---|---|---|---|---|
| 1: schema | `[id, label, payload]` | A | Active: pass | Inactive: `no such column: title` |
| 2: up | `[id, title, payload]` | A | **Active: incompatible** | Inactive: passes |
| 3: new writes | `[id, title, payload]` | B | **Active: incompatible** | Active: pass |
| 4: drain NEW, restart OLD | `[id, title, payload]` | B | **Active: incompatible** | Inactive: passes |
| 5: down | `[id, label, payload]` | B | Active: pass | Inactive: `no such column: title` |

Expected and observed full ordered rows matched exactly wherever SELECT succeeded:

```python
A = [(1, '첫 항목', b'\x00\xff'),
     (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

OLD requires `[id, label, payload]`; NEW requires `[id, title, payload]`. The failures at steps 2–4 are column-contract failures despite correct row values. NEW’s errors at steps 1 and 5 are inactive-reader observations, not rollout blockers.

Step 1 is the last compatible checkpoint before the blocker. The database remains recoverable through the supplied down migration: step 5 restores OLD compatibility and preserves the committed update and insert, including all BLOB bytes. Restarting OLD at step 4 alone does not restore compatibility. No destructive migration loss was observed; the update intentionally replaces row 1’s original values.

The smallest mitigation preserving both literal reader contracts is an **exclusive cutover**: drain OLD before up, activate NEW afterward; on rollback, drain NEW, apply down, then restart OLD. This requires removing the proposed coexistence period. If coexistence is required, a separate NEW view/query is necessary: adding `title` alongside `label` to the shared view would also break OLD’s exact `SELECT *` column contract.

All supplied files and skill resources were preserved; no scratch files, fixes, deployments, dependencies, or external services were used. Evidence covers the specified local SQL sequence only; concurrency, crash recovery, application runtimes, and other database engines remain outside scope.
