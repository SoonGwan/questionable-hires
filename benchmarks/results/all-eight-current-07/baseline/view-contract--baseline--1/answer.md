I’ll read the proposal and contracts, then run the supplied SQL and both reader queries in one in-memory database through all five checkpoints. I’ll leave the files unchanged and check column order, full values, and BLOB bytes.


**Step 2 is the first blocker.** OLD’s `SELECT` succeeds, but returns `[id, title, payload]` instead of its required `[id, label, payload]`. Successful execution does not establish consumer compatibility.

Executed `python3 -B - <<'PY' … PY` using SQLite 3.44.0 and one disposable `sqlite3.connect(':memory:')` connection. The harness executed each supplied SQL file verbatim with `executescript`, committed, and ran both literal queries from `readers.py` at every checkpoint:

```sql
SELECT * FROM public_items ORDER BY id
SELECT id, title, payload FROM public_items ORDER BY id
```

| Checkpoint | OLD result | NEW result | Full rows |
|---|---|---|---|
| 1: schema | Active: compatible; `[id,label,payload]` | Inactive: `no such column: title` | A |
| 2: up | **Active: incompatible**; `[id,title,payload]` | Inactive: compatible | A |
| 3: new writes | **Active: incompatible**; `[id,title,payload]` | Active: compatible | B |
| 4: restart OLD, no schema change | **Active: incompatible**; `[id,title,payload]` | Inactive: compatible | B |
| 5: down | Active: compatible; `[id,label,payload]` | Inactive: `no such column: title` | B |

Every successful query returned exactly the expected complete ordered rows below. Payloads were verified as Python `bytes`, including the empty BLOB:

```python
# A: checkpoints 1–2
[(1, '첫 항목', b'\x00\xff'),
 (2, 'keep', b'')]

# B: checkpoints 3–5
[(1, 'updated', b'\xfe\x00'),
 (2, 'keep', b''),
 (3, 'new', b'\x80')]
```

NEW’s successful results always had its required `[id,title,payload]` labels. Its errors at checkpoints 1 and 5 are inactive-reader observations, not blockers. Base-table rows also matched the write contract at all five checkpoints.

**Recovery and mitigation:**

- Data remains recoverable throughout. The down script restores OLD’s interface.
- Both the committed update and inserted row survive rollback, with exact BLOB bytes. Rollback restores the view contract, not the original data values.
- Restarting OLD at step 4 does not restore compatibility; the schema must be rolled back before OLD resumes.
- With these fixed reader queries and exact column contracts, a shared view cannot support coexistence. Adding both `label` and `title` would make OLD’s `SELECT *` return an extra column.
- The smallest compatible operational change is a coordinated cutover: drain OLD before applying up, then activate NEW; on rollback, drain NEW, apply down, then restart OLD. Preserving coexistence requires changing the proposal to use separate reader interfaces or revised queries.

All ten reader outcomes and five base-row checks matched expectations. Supplied-file hashes remained unchanged; no scratch files, dependencies, network access, or deployment were used. Findings cover the specified single-connection SQL sequence only, not concurrency, crash recovery, application writers, or other database engines.
