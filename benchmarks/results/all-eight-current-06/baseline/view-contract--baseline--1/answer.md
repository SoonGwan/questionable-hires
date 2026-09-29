I’ll inspect the proposal and contracts, then run the supplied scripts and literal reader queries in one in-memory database sequence. I’ll check column order and full values, including BLOB bytes, without changing any files.

The upgrade changes the view’s column name from `label` to `title` while OLD is still active. OLD’s `SELECT *` may therefore succeed but violate its contract. I’ll test that at each checkpoint, then continue through the writes and rollback to check recovery and data preservation.

**The first blocker is checkpoint 2:** `002_up.sql` breaks active OLD’s column contract. Its SELECT succeeds and returns correct values, but returns `[id, title, payload]` instead of required `[id, label, payload]`.

I executed the four supplied SQL scripts unchanged, in order, using one disposable `sqlite3.connect(':memory:')` connection under `python3 -B` (SQLite 3.44.0). At checkpoint 4 I made no database changes. Both literal queries from `readers.py` ran at every checkpoint:

```sql
SELECT * FROM public_items ORDER BY id
SELECT id, title, payload FROM public_items ORDER BY id
```

| Checkpoint | OLD result | NEW result | Complete rows |
|---|---|---|---|
| 1: schema; OLD active | Compatible: `[id, label, payload]` | Inactive error: `no such column: title` | A |
| 2: upgrade; OLD active | **Incompatible:** `[id, title, payload]` | Compatible, inactive | A |
| 3: writes; both active | **Incompatible:** `[id, title, payload]` | Compatible, active | B |
| 4: drain NEW/restart OLD | **Incompatible:** `[id, title, payload]` | Compatible, inactive | B |
| 5: rollback; OLD active | Compatible: `[id, label, payload]` | Inactive error: `no such column: title` | B |

Expected and observed complete ordered rows matched for **every successful query**:

```python
# A — checkpoints 1–2
[(1, '첫 항목', b'\x00\xff'),
 (2, 'keep', b'')]

# B — checkpoints 3–5
[(1, 'updated', b'\xfe\x00'),
 (2, 'keep', b''),
 (3, 'new', b'\x80')]
```

Assertions checked ordered column labels, full row equality, and exact Python value types `(int, str, bytes)`. The empty BLOB remained `b''`. Base-table reads also matched the expected rows at every checkpoint. NEW’s errors at checkpoints 1 and 5 are inactive-reader observations, not blockers.

**Recovery and write preservation:** restarting OLD alone at checkpoint 4 does not restore compatibility. Applying `002_down.sql` at checkpoint 5 does: it restores the `label` alias without changing `items`. The committed update to row 1, unchanged row 2, and inserted row 3—including every BLOB byte—survive rollback. The down script restores the reader interface, not the original data snapshot.

**Smallest compatible mitigation:** with both literal reader contracts fixed, remove coexistence and use a quiesced cutover: stop OLD before upgrading, then activate NEW; on rollback, drain NEW, apply the down script, then restart OLD. This changes the proposed sequence and introduces an interruption.

If coexistence is required, retain OLD’s three-column view and give NEW a separate view, changing NEW’s query accordingly. Adding `title` alongside `label` in the shared view would give OLD’s `SELECT *` an extra column and still violate its exact contract.

The decisive execution used `con.executescript(Path(script).read_text())`, explicit commits, and `con.execute(query)` followed by `cursor.description` and `fetchall()` assertions. All ten query outcomes matched the results above.

All six supplied files passed unchanged SHA-256 checks; no scratch files, dependencies, network access, or deployment were involved. These results cover only the specified local SQL sequence—not concurrency, application writers, crash recovery, or other database engines.
