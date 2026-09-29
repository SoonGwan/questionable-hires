I’ll use the Friday skill to check the supplied rollout and rollback sequence, including exact reader results and write preservation, without changing the proposal.


**Blocked by evidence at step 2.** `002_up.sql` changes OLD’s returned column names while OLD remains active. Its SELECT succeeds, but its consumer contract fails.

Executed `python3 -B - <<'PY' … PY` using Python’s existing `sqlite3` (SQLite 3.44.0), one disposable `:memory:` connection, the actual supplied scripts in order, and both literal queries from `readers.py` at every checkpoint. Checked `cursor.description`, complete ordered rows, and Python `bytes` payload types.

| Checkpoint | OLD result | NEW result | Complete rows |
|---|---|---|---|
| 1. Schema; OLD active | Pass | Inactive: `no such column: title` | A |
| 2. Up; OLD active | **Fail: column labels** | Inactive: pass | A |
| 3. Writes; both active | **Fail: column labels** | Pass | B |
| 4. Restart OLD; no schema change | **Fail: column labels** | Inactive: pass | B |
| 5. Down; OLD active | Pass | Inactive: `no such column: title` | B |

Expected and observed complete rows matched at every successful query and direct table check:

```python
A = [(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]
B = [(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

OLD requires `[id, label, payload]`; steps 2–4 return `[id, title, payload]`. NEW requires and receives `[id, title, payload]` wherever its query succeeds. Inactive NEW errors at steps 1 and 5 are not blockers.

Step 1 is the last compatible checkpoint before the blocker. Data remains recoverable throughout this sequence: the down script only replaces the view. **Both the new update and insert survive rollback**, including exact BLOB bytes. Step 4 alone does not restore OLD compatibility; step 5 does.

The smallest mitigation preserving both literal reader contracts is a coordinated cutover: drain OLD before applying up, activate NEW afterward, then drain NEW and apply down before restarting OLD. This removes coexistence. If coexistence is required, a prerequisite consumer/query change or separate versioned view is necessary: adding both names to this view would also violate OLD’s exact `SELECT *` column contract.

No files or skill resources were changed; no scratch files, dependencies, external services, or deployment were used. Evidence covers the specified sequential SQL-only fixture, not concurrency, crash recovery, application runtimes, or other database engines.
