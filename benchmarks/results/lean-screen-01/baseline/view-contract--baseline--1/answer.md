I’ll read the proposal and contracts, then run the supplied SQL and both reader queries in one disposable in-memory database. I’ll check column order and full values at each checkpoint without changing any files.

## Verdict

**Step 2 is the first blocker.** OLD remains active, but `002_up.sql` changes its returned columns from `[id, label, payload]` to `[id, title, payload]`. Its SELECT succeeds and returns correct values, yet violates the consumer contract.

### Executed verification

Ran `python3 -B - <<'PY' … PY` using existing SQLite **3.51.0**, one `sqlite3.connect(':memory:')` connection, and the actual unmodified scripts through `executescript()`, committing before checking readers:

`001_schema.sql → 002_up.sql → 003_new_writes.sql → no schema change → 002_down.sql`

Executed both literal queries at every checkpoint:

```sql
SELECT * FROM public_items ORDER BY id
SELECT id, title, payload FROM public_items ORDER BY id
```

Required ordered labels: OLD `[id, label, payload]`; NEW `[id, title, payload]`.

| Checkpoint | OLD observed | NEW observed |
|---|---|---|
| 1: Initial | Active, compatible; required labels, rows A | Inactive: `no such column: title` |
| 2: Up | **Active, incompatible**; `[id, title, payload]`, rows A | Inactive, compatible; required labels, rows A |
| 3: Writes/coexistence | **Active, incompatible**; `[id, title, payload]`, rows B | Active, compatible; required labels, rows B |
| 4: Restart OLD | **Active, incompatible**; `[id, title, payload]`, rows B | Inactive, compatible; required labels, rows B |
| 5: Down | Active, compatible; required labels, rows B | Inactive: `no such column: title` |

Expected and observed complete ordered rows matched for every successful query:

```python
A = [(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

All payloads were verified as Python `bytes`, including the empty BLOB. Base-table rows matched at all five checkpoints. NEW’s errors at steps 1 and 5 are **inactive-reader observations, not blockers**.

### Recovery and smallest mitigation

- **Data remains recoverable:** the migrations replace only the view. Applying down restores OLD compatibility.
- **New writes survive rollback:** step 5 preserves the update to id 1, unchanged id 2, and inserted id 3, with exact BLOB bytes.
- **Step 4 does not restore compatibility:** restarting OLD cannot restore the missing `label` column.
- **Smallest mitigation with unchanged SQL/readers:** replace coexistence with a coordinated cutover. Stop OLD before up, activate NEW afterward; on rollback, drain NEW, apply down, then restart OLD. This requires an interruption.
- If coexistence is mandatory, the proposal needs a reader/interface change. Adding both aliases to the view would give OLD’s `SELECT *` an extra column and still violate its exact contract.

Verification covered the supplied single-connection SQL sequence only; concurrent writers, crashes, other engines and deployment were outside scope. All supplied files remained byte-for-byte unchanged; no scratch files, dependencies or external services were used.
