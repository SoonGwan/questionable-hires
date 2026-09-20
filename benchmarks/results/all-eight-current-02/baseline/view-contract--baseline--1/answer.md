I’ll inspect the proposal and contracts, then run the supplied SQL and both reader queries through all five checkpoints in one in-memory database, checking labels, values, and BLOB bytes.

**The first blocker is step 2:** `002_up.sql` replaces `label` with `title` while OLD remains active. OLD’s SELECT succeeds and returns correct values, but its ordered column contract fails.

Executed using `python3 -B - <<'PY' ... PY`, SQLite 3.51.0, and one `sqlite3.connect(':memory:')` connection. The harness applied each supplied SQL file verbatim with `executescript()`, committed, and executed both literal queries from `readers.py` at every checkpoint. Step 4 made no schema change.

Expected ordered labels:

- OLD: `[id, label, payload]`
- NEW: `[id, title, payload]`

| Checkpoint | OLD observed | NEW observed |
|---|---|---|
| 1 — baseline; OLD active | Compatible: `[id, label, payload]`, rows A | Inactive error: `no such column: title` |
| 2 — upgrade; OLD active | **Incompatible:** `[id, title, payload]`, rows A | Inactive but compatible; rows A |
| 3 — writes; both active | **Incompatible:** `[id, title, payload]`, rows B | Compatible; rows B |
| 4 — NEW drained, OLD restarted | **Still incompatible:** `[id, title, payload]`, rows B | Inactive but compatible; rows B |
| 5 — schema rollback; OLD active | Compatible: `[id, label, payload]`, rows B | Inactive error: `no such column: title` |

Complete expected and observed rows matched on every successful query:

```python
# A: checkpoints 1–2
[(1, '첫 항목', b'\x00\xff'),
 (2, 'keep', b'')]

# B: checkpoints 3–5
[(1, 'updated', b'\xfe\x00'),
 (2, 'keep', b''),
 (3, 'new', b'\x80')]
```

Payloads were verified as Python `bytes`, including the empty BLOB. The inactive NEW errors at checkpoints 1 and 5 are observations, not blockers under the release contract.

**Recovery and write survival:** restarting OLD alone at step 4 does not restore compatibility. Applying `002_down.sql` does. The committed update to row 1 and insertion of row 3 survive rollback exactly, including BLOB bytes; row 2 remains unchanged. The final base-table query also matched rows B. Thus consumer compatibility is recoverable, and the supplied write-preservation requirement passes despite the rollout failure.

**Smallest compatible mitigation:** no ordinary view-column change supports both fixed reader contracts during coexistence. Adding both `label` and `title` would give OLD’s `SELECT *` an extra column and still violate its exact contract. For coexistence, preserve the original `public_items` and revise NEW’s query to:

```sql
SELECT id, label AS title, payload FROM public_items ORDER BY id
```

That requires an explicitly revised proposal; it was not applied. If reader queries must remain fixed, coexistence must be removed and readers stopped around schema switches, with the down migration completed before restarting OLD.

All checkpoint assertions passed against these expected outcomes—not against rollout compatibility. Supplied-file hashes remained unchanged; no scratch files, dependencies, network calls, or deployment actions were used. Results cover only the specified single-connection SQL sequence, not application writers, concurrency, crash recovery, or other engines.
