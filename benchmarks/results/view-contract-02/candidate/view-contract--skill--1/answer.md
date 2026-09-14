I’ll use the friday skill to check the five states, execute the supplied SQL in memory, and compare both readers’ full results with the contracts.



## Blocked by evidence

**Step 2 is the first blocker.** OLD’s `SELECT *` succeeds, but returns `[id, title, payload]`; its contract requires `[id, label, payload]`. Correct values do not compensate for incorrect column names.

| Checkpoint | OLD — active throughout | NEW | Full rows |
|---|---|---|---|
| 1. Schema | Pass | Inactive: `no such column: title` | A |
| 2. Up | **Column contract fails** | Inactive: passes | A |
| 3. New writes; coexistence | **Column contract fails** | Active: passes | B |
| 4. Drain NEW; restart OLD | **Column contract fails** | Inactive: passes | B |
| 5. Down | Pass | Inactive: `no such column: title` | B |

NEW’s errors at steps 1 and 5 are inactive-reader observations, not blockers.

### Exact expected and observed values

Every successful query returned the complete expected ordered rows:

```python
A = [(1, '첫 항목', b'\x00\xff'),
     (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

Payloads were verified as native `bytes`, including the empty BLOB. Successful NEW results had its required `[id, title, payload]` labels.

### Recovery and smallest mitigation

- **Last compatible checkpoint before failure: step 1.** No irreversible data loss was observed; later states remain recoverable through the supplied down script.
- Restarting OLD at step 4 does not restore compatibility. Step 5 restores the view’s `label` alias.
- **New writes survive rollback:** the updated row 1, unchanged row 2, and inserted row 3 remain exactly B after down.
- **Ordering alone cannot support the stipulated coexistence with these literal readers.** Adding `title` beside `label` would also break OLD’s exact `SELECT *` column contract.
- The smallest compatibility prerequisite is an OLD reader using explicit projection, `SELECT id, label, payload FROM public_items ORDER BY id`, followed by a transitional view exposing both aliases. Drain NEW and restore the OLD-compatible view before restarting the original OLD reader. This mitigation was assessed, not implemented or executed.

### Execution and limits

Ran `python3 -B - <<'PY'` using friday’s `sqlite_matrix.py` API: **one disposable in-memory SQLite 3.51.0 sequence**, executing `001_schema.sql → 002_up.sql → 003_new_writes.sql → unchanged checkpoint → 002_down.sql`. Both literal queries from `readers.py` ran at every checkpoint.

All 10 observations were checked for errors, ordered labels, complete rows and exact BLOB bytes; no truncation occurred. Project file hashes remained unchanged; no scratch files, dependencies, network access or deployment were used.

Evidence covers the specified SQL-only fixture. Concurrency, crash recovery, application runtimes and other database engines remain outside scope.
