I’ll use the Friday skill to check the proposal’s five states in one in-memory SQL sequence, comparing both readers’ labels and values with the contracts. I’ll preserve the supplied files and won’t change or deploy the proposal.


The up migration changes the view’s second column from `label` to `title` while OLD is still active. OLD’s `SELECT *` can therefore succeed but fail its column-name contract. I’ll execute all five checkpoints to verify that failure and whether rollback preserves the new writes and exact BLOB bytes.


**Blocked by evidence at step 2.** `002_up.sql` changes OLD’s returned columns from `[id, label, payload]` to `[id, title, payload]`. Its SELECT succeeds, but its consumer contract fails.

Executed `python3 -B - <<'PY' … PY` using SQLite 3.44.0 and one disposable `:memory:` connection. The harness executed the supplied SQL scripts unchanged, committed each transition, and ran both literal queries from `readers.py` at all five checkpoints.

| Checkpoint | OLD observation | NEW observation |
|---|---|---|
| 1 — initial schema | Active: compatible | Inactive: `no such column: title` |
| 2 — up migration | Active: wrong column labels | Inactive: compatible |
| 3 — new writes | Active: wrong column labels | Active: compatible |
| 4 — restart OLD | Active: wrong column labels | Inactive: compatible |
| 5 — down migration | Active: compatible | Inactive: `no such column: title` |

The inactive NEW errors at steps 1 and 5 are not blockers.

Expected and observed complete ordered rows matched for every successful query, with payloads verified as Python `bytes`:

```text
Steps 1–2:
[(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]

Steps 3–5:
[(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

Step 1 is the last compatible checkpoint before the blocker. Subsequent states remain recoverable: the down migration restores OLD’s labels without losing the committed update or insert, including their exact BLOB bytes. Restarting OLD alone at step 4 does not restore compatibility.

The smallest compatible mitigation with the literal readers unchanged is an **exclusive cutover**: stop OLD before applying up, then activate NEW; on rollback, drain NEW, apply down, then restart OLD. That changes the proposed coexistence requirement. If coexistence must remain, separate versioned views and a corresponding reader change are required; adding a column would violate OLD’s exact `SELECT *` shape.

All ten reader checks and preservation assertions passed with these expected outcomes. Supplied files and skill resources remained unchanged; no scratch files were created. Evidence covers the specified SQL-only fixture, not concurrency, application runtime, crash recovery, or other engines.
