I’ll read the proposal and contracts, then run the supplied scripts and literal queries in one in-memory database sequence, checking column order and exact values at each checkpoint.

**The first blocker is step 2.** OLD remains active, but `002_up.sql` changes its returned column name from `label` to `title`. Its SELECT succeeds and returns correct values, yet violates the consumer contract.

Executed `python3 -B - <<'PY' … PY` using SQLite 3.44.0 and one `sqlite3.connect(':memory:')` connection. Each supplied SQL file was read directly into `executescript()` and committed in the specified sequence. Both literal queries ran at every checkpoint:

```sql
SELECT * FROM public_items ORDER BY id
SELECT id, title, payload FROM public_items ORDER BY id
```

Checked `cursor.description` for ordered labels, complete ordered rows for equality, and payloads for exact `bytes` values.

Expected columns: OLD `[id, label, payload]`; NEW `[id, title, payload]`.

| Checkpoint | OLD observed | NEW observed | Successful-query rows |
|---|---|---|---|
| 1 — schema | Active: compatible; `[id,label,payload]` | Inactive: `no such column: title` | A |
| 2 — up | **Active: incompatible**; `[id,title,payload]` | Inactive: compatible; `[id,title,payload]` | A |
| 3 — writes, coexistence | **Active: incompatible**; `[id,title,payload]` | Active: compatible; `[id,title,payload]` | B |
| 4 — restart OLD, unchanged schema | **Active: incompatible**; `[id,title,payload]` | Inactive: compatible; `[id,title,payload]` | B |
| 5 — down | Active: compatible; `[id,label,payload]` | Inactive: `no such column: title` | B |

Expected and observed full rows matched exactly for every successful query and the underlying table:

```python
A = [
    (1, '첫 항목', b'\x00\xff'),
    (2, 'keep', b''),
]
B = [
    (1, 'updated', b'\xfe\x00'),
    (2, 'keep', b''),
    (3, 'new', b'\x80'),
]
```

The NEW errors at steps 1 and 5 are inactive-reader observations, not blockers. OLD’s column mismatch at steps 2–4 is an active incompatibility.

**Recovery and write preservation:** Data remains intact throughout. Restarting OLD alone at step 4 does not restore compatibility; applying the down script at step 5 does. The committed update to row 1, inserted row 3, untouched row 2, and every BLOB byte survive rollback. This is recoverable through schema rollback, but the proposed rollback order exposes OLD before that recovery.

**Smallest compatible mitigation:** With both literal queries and contracts unchanged, remove coexistence and use a coordinated interruption: stop OLD before applying up, activate NEW afterward; on rollback, drain NEW, apply down, then restart OLD. One ordinary shared view cannot satisfy both contracts simultaneously: exposing `title` for NEW changes OLD’s exact `SELECT *` shape. Adding both aliases also fails OLD’s required three-column contract. Preserving coexistence requires a separately versioned view and a reader-query change.

All checks passed against the observed outcomes above. Supplied file hashes remained unchanged; no scratch files, dependencies, network access, fixes, or deployment were used. Results cover the supplied single-connection SQL sequence only; restart/drain was represented by reader activity, with concurrency, crash recovery, application writers, and other engines outside scope.
