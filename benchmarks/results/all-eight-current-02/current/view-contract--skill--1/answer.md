I’ll use the supplied Friday skill to inspect the proposal and contracts, then run the SQL sequence in memory and compare both readers’ full results at every checkpoint.

**Blocked by evidence at step 2.** OLD’s `SELECT` succeeds but returns ordered columns `[id, title, payload]`; its consumer requires `[id, label, payload]`. Correct row values do not make this compatible.

Executed `python3 -B - <<'PY' … PY` using SQLite 3.51.0 and one disposable `sqlite3.connect(':memory:')` connection. The harness applied each supplied SQL file verbatim through `executescript`, committed writes, and executed both literal queries from `readers.py` at all five checkpoints:

```sql
SELECT * FROM public_items ORDER BY id
SELECT id, title, payload FROM public_items ORDER BY id
```

| Checkpoint | OLD observation | NEW observation | Complete rows |
|---|---|---|---|
| 1 — initial schema | Active: compatible | Inactive: `no such column: title` | A |
| 2 — up migration | **Active: wrong column labels** | Inactive: compatible | A |
| 3 — new writes, coexistence | **Active: wrong column labels** | Active: compatible | B |
| 4 — NEW drained, OLD restarted | **Active: wrong column labels** | Inactive: compatible | B |
| 5 — down migration | Active: compatible | Inactive: `no such column: title` | B |

Expected and observed complete ordered rows matched for every successful query:

```python
A = [(1, '첫 항목', b'\x00\xff'),
     (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

Payloads were verified as actual `bytes`, including the empty BLOB. OLD returned `[id, label, payload]` at checkpoints 1 and 5; both successful readers returned `[id, title, payload]` at checkpoints 2–4. NEW’s errors at checkpoints 1 and 5 are inactive-reader observations, not blockers.

Step 1 is the last compatible checkpoint before failure. Data remains recoverable throughout: the migrations only replace a view. At step 5, OLD sees every committed update and insert with exact BLOB bytes. **New writes survive rollback.** Restarting OLD at step 4 alone does not restore compatibility.

The smallest ordering mitigation, if coexistence can be removed, is to drain OLD before the up migration and activate NEW afterward; on rollback, drain NEW, apply the down migration, then restart OLD. If coexistence is required, these literal contracts cannot share this view: adding both names would also break OLD’s exact `SELECT *` column contract. A separate NEW view/query is needed while retaining OLD’s view.

All ten reader observations and five base-table states were checked. Supplied files and skill resources remained unchanged, verified by hashes; no scratch files, dependencies, network, or deployment were used. Evidence covers the supplied SQL-only SQLite sequence; concurrency, crash recovery, application runtimes, and other engines remain outside scope.
