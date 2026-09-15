I’ll use the supplied Friday skill to inspect the contracts, then run the SQL and both readers through all five checkpoints in one in-memory database. I’ll preserve the project files and assess consumer compatibility separately from query success.

## Blocked by evidence

**Step 2 is the first blocker.** OLD’s `SELECT *` succeeds, but returns `[id, title, payload]`; its contract requires exactly `[id, label, payload]`.

| Checkpoint | OLD — active throughout | NEW |
|---|---|---|
| 1. Initial schema | Pass | Inactive: `no such column: title` |
| 2. Up migration | **Column-contract failure** | Inactive: compatible |
| 3. New writes; coexistence | **Column-contract failure** | Active: pass |
| 4. Drain NEW, restart OLD | **Column-contract failure** | Inactive: compatible |
| 5. Down migration | Pass | Inactive: `no such column: title` |

Inactive-reader errors are observations, not blockers.

### Exact values and recovery

Every successful query returned the complete expected ordered rows, with actual Python `bytes` payloads:

```python
# Checkpoints 1–2
[(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]

# Checkpoints 3–5
[(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

Checkpoint 1 is the last compatible state before the blocker. Subsequent states remain recoverable through the supplied down migration: it restores OLD’s column contract without changing `items`. **Both the update and insert survive rollback**, including exact BLOB bytes. Restarting OLD alone at step 4 does not restore compatibility.

### Smallest compatible mitigation

With literal reader contracts fixed, use an exclusive cutover: drain OLD before applying up and activating NEW; drain NEW before applying down and restarting OLD. This removes coexistence and requires a service gap.

If coexistence is required, a consumer/query prerequisite is necessary, such as a separate versioned view for NEW. Adding `title` alongside `label` to the shared view would still violate OLD’s exact `SELECT *` column contract.

### Execution and limits

Executed a `python3 -B - <<'PY'` harness using the supplied Friday `sqlite_matrix.py` API: one disposable SQLite 3.51.0 in-memory sequence, actual scripts in order, both literal queries at all five checkpoints. All ten observations completed; assertions checked ordered columns, complete rows, BLOB types and bytes.

Project file hashes remained unchanged; no scratch files, dependencies, network, deployment or fixes. Evidence covers the specified SQL-only fixture, not concurrency, application runtimes or crash recovery.
