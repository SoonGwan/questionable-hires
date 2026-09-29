I’ll use the Friday skill to trace the rollout and rollback, then execute the supplied SQL and both readers in one in-memory sequence and compare their results with the contracts.

**Blocked by evidence at step 2.** `002_up.sql` changes OLD’s returned columns from `[id, label, payload]` to `[id, title, payload]`. Its SELECT succeeds, but its consumer contract fails.

Executed `python3 -B - <<'PY' … PY`, calling the supplied Friday `sqlite_matrix.py` API once: all four actual SQL scripts, in proposal order, and both literal `readers.py` queries at all five checkpoints on one disposable in-memory SQLite 3.44.0 connection.

| Checkpoint | OLD | NEW |
|---|---|---|
| 1: schema | Active: passes | Inactive: `no such column: title` |
| 2: up | **Active: wrong column labels** | Inactive: passes |
| 3: new writes | **Active: wrong column labels** | Active: passes |
| 4: restart OLD | **Active: wrong column labels** | Inactive: passes |
| 5: down | Active: passes | Inactive: `no such column: title` |

The inactive-reader errors are observations, not blockers.

Expected and observed complete ordered rows matched for every successful query, with native BLOB bytes verified:

```python
# Steps 1–2
[(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]

# Steps 3–5
[(1, 'updated', b'\xfe\x00'), (2, 'keep', b''),
 (3, 'new', b'\x80')]
```

Step 1 is the last compatible checkpoint before the blocker. Later states remain recoverable: the down script restores OLD’s exact columns without changing stored data. **Both the new update and insert survive rollback**, including their complete payload bytes. Restarting OLD alone at step 4 does not restore compatibility.

The smallest mitigation with unchanged reader queries is an exclusive cutover: drain OLD before applying up and activating NEW; on rollback, drain NEW, apply down, then restart OLD. This requires removing the proposed coexistence interval. If coexistence is required, a reader contract must change or readers must use separate views. Adding `title` alongside `label` would still break OLD’s exact `SELECT *` column contract.

All ten observations were complete and untruncated. Project file inventory and content hashes remained unchanged. No fixes or deployment were performed. Evidence covers the specified SQL-only sequence; concurrency, application runtimes, crash recovery and other engines remain outside scope.
