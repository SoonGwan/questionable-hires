I’ll read the Friday skill and release proposal, then run the supplied SQL and literal reader queries in one in-memory sequence, checking their full results against the contracts at each checkpoint.

**Blocked at step 2.** OLD’s `SELECT` succeeds, but the returned column changes from `label` to `title`, violating its consumer contract.

Using the Friday skill, I ran `python3 -B - <<'PY'` with SQLite 3.44.0 and one disposable `sqlite3.connect(':memory:')` connection. The harness executed each supplied SQL file verbatim using `executescript`, committed each transition, and ran both literal queries from `readers.py` at all five checkpoints:

```sql
SELECT * FROM public_items ORDER BY id
SELECT id, title, payload FROM public_items ORDER BY id
```

| Checkpoint | Observed ordered columns for successful queries | OLD | NEW |
|---|---|---|---|
| 1: schema | `[id, label, payload]` | Active: compatible | Inactive: `no such column: title` |
| 2: up | `[id, title, payload]` | **Active: incompatible** | Inactive: compatible |
| 3: new writes | `[id, title, payload]` | **Active: incompatible** | Active: compatible |
| 4: drain NEW/restart OLD | `[id, title, payload]` | **Active: incompatible** | Inactive: compatible |
| 5: down | `[id, label, payload]` | Active: compatible | Inactive: `no such column: title` |

OLD requires exactly `[id, label, payload]`; NEW requires exactly `[id, title, payload]`. The inactive NEW errors at steps 1 and 5 are observations, not blockers.

Expected and observed complete ordered rows matched for **every successful query**, with payloads verified as Python `bytes`:

```python
# Checkpoints 1–2
[(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]

# Checkpoints 3–5
[(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

The underlying table matched these values at every checkpoint too. Thus, correct row values and successful execution do **not** establish OLD compatibility at steps 2–4.

Step 1 is the last compatible checkpoint before the blocker. Subsequent completed states remain recoverable through the supplied down migration, which changes only the view. **The committed update and insert survive rollback**, including all BLOB bytes. Step 4’s reader restart alone does not restore compatibility; step 5 does.

The smallest mitigation is an ordering change that removes coexistence: drain OLD before applying up, then activate NEW; on rollback, drain NEW, apply down, then restart OLD. This requires accepting a reader interruption. If coexistence is mandatory, these unchanged queries cannot share a compatible view: adding both aliases would give OLD an extra column through `SELECT *`. Separate versioned interfaces and a reader change would be required.

All 10 reader executions were checked. Project and skill file hashes remained unchanged; no scratch files, dependencies, network access, or deployment were used. Evidence covers the supplied SQL-only sequence; application restarts were represented by active-reader roles, and concurrency, crash recovery, and other database engines remain outside scope.
