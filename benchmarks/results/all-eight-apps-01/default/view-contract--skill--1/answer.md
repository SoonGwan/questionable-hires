I’m using the Friday skill to check the five rollout and rollback states against the supplied contracts, with the actual SQL in one disposable in-memory sequence. I’ll preserve all files and report compatibility separately from query execution success.

**Blocked by evidence at step 2.** `002_up.sql` changes OLD’s returned column names from `[id, label, payload]` to `[id, title, payload]` while OLD remains active. Its SELECT succeeds, but its consumer contract fails.

Executed `python3 -B - <<'PY' … PY` using standard-library `sqlite3` (SQLite 3.44.0), one `:memory:` connection, the actual supplied SQL files in order, and both literal queries from `readers.py` at every checkpoint.

| Checkpoint | OLD observation | NEW observation | Complete rows |
|---|---|---|---|
| 1 — initial schema | Active: pass | Inactive: `no such column: title` | Initial values match |
| 2 — up migration | Active: wrong column labels | Inactive: pass | Initial values match |
| 3 — new writes | Active: wrong column labels | Active: pass | Updated values match |
| 4 — restart OLD | Active: wrong column labels | Inactive: pass | Updated values match |
| 5 — down migration | Active: pass | Inactive: `no such column: title` | Updated values match |

Expected and observed full ordered rows were identical, including actual `bytes` payloads:

```python
# Checkpoints 1–2
[(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]

# Checkpoints 3–5
[(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

OLD’s ordered labels matched only at checkpoints 1 and 5; NEW’s matched at checkpoints 2–4. NEW’s errors at 1 and 5 are inactive-reader observations, not blockers.

**Recovery remains possible throughout.** Step 1 is the last compatible checkpoint before the blocker. Restarting OLD alone at step 4 does not restore compatibility; the down migration at step 5 does. It changes only the view, preserving both the committed update and insert, including all BLOB bytes.

**Smallest compatible mitigation:** retain the original view and have NEW explicitly query `SELECT id, label AS title, payload FROM public_items ORDER BY id`. This requires a proposed NEW-query change, which I did not apply. Adding a `title` column to the shared view would break OLD’s exact `SELECT *` contract. With both literal queries frozen, the shared view cannot satisfy coexistence; separate versioned views/routing or a coordinated cutover is required. For a cutover, restore the old view before reactivating OLD during rollback.

All 10 reader observations were checked against ordered labels and complete values. All 11 project/skill file hashes remained unchanged; no scratch files, dependencies, network access, or deployment were used. Evidence covers the supplied SQL-only sequence, not concurrency, crash recovery, application runtimes, or other database engines.
