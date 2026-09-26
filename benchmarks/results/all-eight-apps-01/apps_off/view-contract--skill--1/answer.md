I’ll use the Friday skill to check the supplied SQL, reader contracts, and rollback sequence in one disposable in-memory database, while preserving all project files.

**Blocked by evidence at step 2.** `002_up.sql` changes OLD’s returned column name from `label` to `title` while OLD remains active. Its SELECT succeeds, but its consumer contract fails.

Executed `python3 -B - <<'PY' … PY` using Python’s existing `sqlite3` module (SQLite 3.44.0), one `:memory:` connection, and the actual supplied scripts in order. Both literal queries from `readers.py` ran at every checkpoint, including the unchanged-schema restart.

| Checkpoint | OLD observation | NEW observation | Complete rows |
|---|---|---|---|
| 1: schema | Active: compatible | Inactive: `no such column: title` | A |
| 2: up | **Active: incompatible labels** | Inactive: compatible | A |
| 3: new writes | **Active: incompatible labels** | Active: compatible | B |
| 4: restart OLD | **Active: incompatible labels** | Inactive: compatible | B |
| 5: down | Active: compatible | Inactive: `no such column: title` | B |

Expected OLD labels: `[id, label, payload]`; observed at steps 2–4: `[id, title, payload]`. NEW’s successful results have its required `[id, title, payload]`. Inactive-reader errors at steps 1 and 5 are **not blockers**.

Expected and observed complete ordered rows matched exactly for every successful query and the underlying table:

```python
A = [(1, '첫 항목', b'\x00\xff'),
     (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

Payloads were also verified as Python `bytes`, including the empty BLOB.

Step 1 is the last compatible checkpoint before failure. Data remains recoverable throughout this sequence: step 4’s code-only rollback fails to restore OLD compatibility, but step 5’s down migration restores it **and preserves all representative committed updates/inserts and BLOB bytes**. No irreversible data loss was observed.

The smallest mitigation retaining both literal reader contracts is an exclusive cutover: drain OLD before the up migration, activate NEW afterward, and on rollback drain NEW, apply down, then restart OLD. This removes the proposed coexistence. If coexistence is required, use separate versioned views and change reader routing; adding a `title` column to the shared view would violate OLD’s exact `SELECT *` column contract.

All 11 project/resource files were hash-verified unchanged; no scratch files, dependencies, network access, or deployment. Evidence covers the specified SQL-only sequence, not concurrency, crash recovery, application runtime, or other database engines.
