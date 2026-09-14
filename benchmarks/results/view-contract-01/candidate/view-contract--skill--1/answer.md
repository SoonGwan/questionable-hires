I’m using the Friday skill to review the proposal and run the supplied SQL and reader queries through all five checkpoints in one disposable in-memory database. I’ll compare the results with the consumer and write contracts and leave the supplied files unchanged.


## Blocked by evidence

**Step 2 is the first blocker.** `002_up.sql` changes the returned column name from `label` to `title` while OLD remains active. OLD’s SELECT succeeds, but its name-based consumer contract fails.

### Five-checkpoint results

Both literal queries were executed at every checkpoint in **one disposable SQLite in-memory sequence**, including after the confirmed blocker.

| Checkpoint | OLD observation | NEW observation | Complete rows |
|---|---|---|---|
| 1. Initial schema | Compatible: `[id, label, payload]` | Inactive error: `no such column: title` | A |
| 2. Up migration | **Active incompatibility:** `[id, title, payload]` | Compatible, inactive | A |
| 3. New writes; coexistence | **Active incompatibility:** `[id, title, payload]` | Compatible, active | B |
| 4. NEW drained; OLD restarted | **Active incompatibility:** `[id, title, payload]` | Compatible, inactive | B |
| 5. Down migration | Compatible: `[id, label, payload]` | Inactive error: `no such column: title` | B |

Expected and observed full ordered rows matched for **every successful query**:

```python
A = [(1, '첫 항목', b'\x00\xff'),
     (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

Payloads were verified as actual `bytes`, including the empty BLOB. Correct values do not compensate for OLD’s incorrect column labels. NEW’s errors at checkpoints 1 and 5 are inactive-reader observations, not blockers.

### Recovery and smallest mitigation

- **Last compatible checkpoint before failure:** step 1.
- **Recovery remains possible:** the migrations only replace the view; the underlying data remains intact. The executed down migration restores OLD compatibility.
- **New writes survive rollback:** step 5 retains the updated row 1, unchanged row 2, and inserted row 3 with exact BLOB bytes.
- **Step 4 is insufficient:** restarting OLD without restoring the view leaves its contract broken until step 5.

The smallest mitigation preserving the supplied SQL and reader contracts is a **non-overlapping cutover**: drain OLD before the up migration, then activate NEW. On rollback, drain NEW, apply the down migration, **then** restart OLD. This changes the proposed coexistence strategy.

If coexistence is required, a prerequisite consumer/schema change is necessary, such as separate versioned views. Adding both names to the current view would also violate OLD’s exact three-column `SELECT *` contract.

### Execution and limits

Executed a `python3 -B - <<'PY'` harness using existing `sqlite3` (SQLite **3.51.0**): `connect(':memory:')`, unchanged supplied scripts via `executescript`, and both literal queries extracted from `readers.py`. Assertions checked `cursor.description`, complete ordered rows, BLOB types/bytes, committed underlying data, and expected compatibility outcomes. All assertions passed; final `integrity_check` returned `ok`.

All **11 project non-Git files**, including skill resources, remained unchanged by SHA-256 comparison. No scratch files, dependencies, network access, deployments, or fixes. Evidence covers the specified SQL-only fixture; concurrency, application runtimes, crash recovery, and other engines remain outside scope.
