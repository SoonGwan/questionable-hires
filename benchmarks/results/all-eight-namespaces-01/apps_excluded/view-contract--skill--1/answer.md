I’ll use the Friday skill to check the five states in one in-memory sequence, comparing both readers’ full results with their contracts and testing whether rollback preserves new writes.

**Blocked by evidence at step 2.** `002_up.sql` changes OLD’s returned column names while OLD remains active. Its SELECT succeeds, but its consumer contract fails.

Executed with `python3 -B - <<'PY'`, using SQLite 3.44.0 and one disposable `:memory:` connection. The harness loaded each supplied SQL script unchanged with `executescript()`, committed the writes, and executed both literal queries from `readers.py` at every checkpoint:

```sql
-- OLD requires ordered labels [id, label, payload]
SELECT * FROM public_items ORDER BY id
-- NEW requires ordered labels [id, title, payload]
SELECT id, title, payload FROM public_items ORDER BY id
```

| Checkpoint | OLD observation | NEW observation | Complete rows |
|---|---|---|---|
| 1. Initial schema | Active: passes | Inactive: `no such column: title` | A |
| 2. Up migration | **Active: incompatible labels** | Inactive: passes | A |
| 3. New writes | **Active: incompatible labels** | Active: passes | B |
| 4. Restart OLD | **Active: incompatible labels** | Inactive: passes | B |
| 5. Down migration | Active: passes | Inactive: `no such column: title` | B |

Expected and observed complete ordered rows matched exactly for every successful query:

```python
A = [(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]
B = [(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

All payloads were actual binary `bytes`, including the empty BLOB. At steps 2–4, OLD received `[id, title, payload]` instead of `[id, label, payload]`. Correct values do not compensate for incorrect labels. NEW’s errors at steps 1 and 5 are inactive-reader observations, not blockers.

Step 1 is the last compatible checkpoint before the failure. The later states remain data-recoverable: the down migration restores OLD’s contract, preserving the committed update to row 1 and insertion of row 3, including exact BLOB bytes. Restarting OLD alone at step 4 does not restore compatibility.

The smallest compatible mitigation **with both literal queries fixed** is an exclusive cutover: drain OLD before the up migration, run NEW alone, then drain NEW and apply down **before** restarting OLD. If coexistence is required, a reader contract must change—for example, preserve the original view and have NEW select `label AS title`. Adding a fourth alias column would break OLD’s exact `SELECT *` shape.

All 11 project/skill files were hash-checked unchanged; no scratch files or fixes were created. Evidence covers the specified sequential SQL-only SQLite contracts, not concurrency, application runtime, crash recovery, staging, or other database engines.
