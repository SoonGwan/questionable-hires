I’ll read the proposal and contracts, then run the supplied SQL and reader queries in a single in-memory sequence and compare the full results at each checkpoint.

**The first blocking step is checkpoint 2.** `002_up.sql` changes OLD’s returned column name from `label` to `title` while OLD remains active. Its SELECT succeeds, but its consumer contract fails.

Executed with `python3 -B - <<'PY'` using existing `sqlite3` (SQLite 3.51.0), one `sqlite3.connect(':memory:')`, and the actual script contents through `executescript(...)`, committing each script. Loaded both literal queries from `readers.py` and executed both at every checkpoint:

```sql
SELECT * FROM public_items ORDER BY id
SELECT id, title, payload FROM public_items ORDER BY id
```

Expected ordered labels: OLD `[id, label, payload]`; NEW `[id, title, payload]`.

| Checkpoint | Observed successful-query labels | OLD result | NEW result | Full rows |
|---|---|---|---|---|
| 1: schema | `[id, label, payload]` | Active: compatible | Inactive: `no such column: title` | A |
| 2: up | `[id, title, payload]` | **Active: incompatible** | Inactive: compatible | A |
| 3: writes | `[id, title, payload]` | **Active: incompatible** | Active: compatible | B |
| 4: restart OLD, unchanged schema | `[id, title, payload]` | **Active: incompatible** | Inactive: compatible | B |
| 5: down | `[id, label, payload]` | Active: compatible | Inactive: `no such column: title` | B |

Every successful query returned these complete ordered rows, matching expected values exactly; payloads were verified as Python `bytes`:

```python
A = [(1, '첫 항목', b'\x00\xff'),
     (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

The inactive NEW errors at checkpoints 1 and 5 are observations, not blockers. OLD’s active incompatibilities at 2–4 are blockers despite correct row values.

**Recovery and write survival:** Restarting OLD alone at checkpoint 4 does not restore compatibility. Applying the down script at checkpoint 5 does. The committed update, inserted row, unchanged row, and all BLOB bytes survive rollback exactly: the scripts replace only the view. Continued execution beyond checkpoint 2 was diagnostic.

**Smallest compatible mitigation:** Preserve the original view and change NEW’s query to:

```sql
SELECT id, label AS title, payload FROM public_items ORDER BY id
```

This preserves both consumers’ required output shapes without replacing the view. It requires revising the supplied literal NEW query; with both queries fixed, the shared ordinary view cannot satisfy both contracts. Adding `title` alongside `label` would also break OLD’s exact `SELECT *` column contract. For rollback recovery alone, restore the old view after draining NEW and before restarting OLD.

No changes or deployments were made. Supplied-file hashes remained unchanged; no scratch files, dependencies, network access, or other skills were used. Results cover the specified single-connection SQL sequence, not application lifecycle behavior, concurrency, crash recovery, or other engines.
