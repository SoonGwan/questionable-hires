I’m using the Friday skill to test the supplied sequence in memory, checking reader contracts and rollback data preservation without changing the proposal.


## Blocked by evidence

**Step 2 is the first blocker.** OLD’s `SELECT` succeeds but returns `[id, title, payload]`; its contract requires `[id, label, payload]`. Correct row values do not compensate for incorrect column names.

### Observed checkpoints

| Step | OLD | NEW | Full rows |
|---|---|---|---|
| 1 — schema | Active: pass | Inactive: `no such column: title` | A |
| 2 — up | **Active: column contract fails** | Inactive: pass | A |
| 3 — new writes | **Active: column contract fails** | Active: pass | B |
| 4 — restart OLD | **Active: column contract fails** | Inactive: pass | B |
| 5 — down | Active: pass | Inactive: `no such column: title` | B |

Expected and observed complete ordered rows matched for every successful query:

```python
A = [(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]
B = [(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

OLD returned `[id, label, payload]` at steps 1/5 and `[id, title, payload]` at steps 2–4. Every successful NEW query returned its required `[id, title, payload]`. Inactive NEW errors at steps 1/5 are **not blockers**.

### Recovery and smallest mitigation

- **Step 1 is the last compatible checkpoint before failure.** Data remains recoverable throughout; neither view migration deletes table data.
- Restarting OLD at step 4 does not restore compatibility. Step 5 does.
- **New writes survive rollback:** OLD reads all of B after down, including the updated record, inserted record, empty BLOB and exact binary bytes.
- With both literal queries and contracts fixed, coexistence on this single view is incompatible. Adding a `title` column alongside `label` would also break OLD’s exact `SELECT *` column contract.
- The smallest compatible proposal change is a coordinated cutover: drain OLD before up, activate NEW afterward, and remove coexistence. For rollback, drain NEW, apply down, then restart OLD. If coexistence is required, a separate versioned view and corresponding reader change are prerequisites.

### Execution and limits

Ran `python3 -B - <<'PY'` using SQLite **3.51.0**, one `sqlite3.connect(':memory:')`, and `executescript()` on all four actual supplied SQL files in order. Executed both literal queries at **all five checkpoints**, including the unchanged-schema restart checkpoint.

Checks compared `cursor.description` column order, complete ordered tuples, Python `bytes`, and SQLite BLOB storage types. All verification assertions passed, confirming the incompatibilities above.

Project file hashes remained unchanged. No scratch files, dependencies, network, deployment or environment changes. Evidence covers the supplied SQL-only fixture; concurrency, crashes and other database engines remain outside scope.
