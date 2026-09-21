I’ll inspect the proposal and contracts, then run the supplied SQL and reader queries in one in-memory database through all five checkpoints, checking column order and full values, including BLOB bytes.

The upgrade changes OLD’s returned column name from `label` to `title`, so its query may succeed while violating its contract. I’ll check that at every checkpoint and verify whether the rollback preserves the later update and insert.

**The first blocker is step 2:** OLD’s SELECT succeeds, but returns `[id, title, payload]` instead of its required ordered labels `[id, label, payload]`.

Executed `python3 -B - <<'PY' … PY` using SQLite 3.51.0, one `sqlite3.connect(':memory:')`, and the actual scripts through `executescript`. Both literal queries from `readers.py` ran at every checkpoint. Assertions checked ordered labels, complete ordered rows, and Python `bytes` payloads.

| Checkpoint | OLD result | NEW result | Full row values |
|---|---|---|---|
| 1 — schema | Active: compatible | Inactive: `no such column: title` | Initial rows match |
| 2 — upgrade | **Active: incompatible labels** | Inactive: compatible | Initial rows match |
| 3 — writes/coexistence | **Active: incompatible labels** | Active: compatible | Updated rows match |
| 4 — restart OLD | **Active: incompatible labels** | Inactive: compatible | Updated rows match |
| 5 — downgrade | Active: compatible | Inactive: `no such column: title` | Updated rows match |

Expected and observed complete rows at checkpoints 1–2:
```python
[(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]
```

Expected and observed complete rows at checkpoints 3–5:
```python
[(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

The inactive NEW errors at steps 1 and 5 are not blockers. OLD’s label mismatch at steps 2–4 is an active consumer failure despite successful execution and correct values.

**Recovery remains possible:** the downgrade restores OLD compatibility. The committed update and insert survive with exact BLOB bytes, including the unchanged empty BLOB. Restarting OLD before downgrading does not recover compatibility.

**Smallest compatible mitigation:** change activation order: drain OLD before upgrading, activate NEW after upgrading, then drain NEW and downgrade before restarting OLD. This removes coexistence and requires a reader pause. If coexistence is mandatory, the fixed contracts need revision or separate versioned views and corresponding reader queries; adding `title` alongside `label` would break OLD’s exact `SELECT *` column contract.

No proposal changes or deployment occurred. Supplied file hashes remained unchanged; no scratch files, dependencies, network, or external services were used. Results cover the supplied sequential SQLite fixture only, excluding concurrency, crash recovery, application writers, and other engines.
