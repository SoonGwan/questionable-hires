I’ll read the Friday skill and release proposal, then run the supplied SQL and literal readers in one in-memory sequence, checking the full results against the contracts at each checkpoint.

**Blocked at step 2.** Using the [Friday skill](.agents/skills/friday/SKILL.md), I verified that `002_up.sql` breaks active OLD’s column-name contract despite successful SELECT execution.

Executed `python3 -B - <<'PY' … PY` using SQLite 3.51.0 and one disposable `sqlite3.connect(':memory:')`. The harness applied the actual supplied scripts sequentially, committed them, and executed both literal queries from `readers.py` at all five checkpoints.

Expected ordered labels: OLD `[id, label, payload]`; NEW `[id, title, payload]`.

| Checkpoint | Observed labels on successful queries | OLD | NEW |
|---|---|---|---|
| 1. Initial schema | `[id, label, payload]` | Active: passes | Inactive: `no such column: title` |
| 2. Up migration | `[id, title, payload]` | **Active: incompatible labels** | Inactive: passes |
| 3. New writes | `[id, title, payload]` | **Active: incompatible labels** | Active: passes |
| 4. Drain NEW/restart OLD | `[id, title, payload]` | **Active: incompatible labels** | Inactive: passes |
| 5. Down migration | `[id, label, payload]` | Active: passes | Inactive: `no such column: title` |

The inactive-reader errors at steps 1 and 5 are observations, not blockers.

Every successful reader returned these complete ordered rows, exactly matching expected values:

```text
Steps 1–2:
(1, '첫 항목', BLOB x'00ff')
(2, 'keep',    BLOB x'')

Steps 3–5:
(1, 'updated', BLOB x'fe00')
(2, 'keep',    BLOB x'')
(3, 'new',     BLOB x'80')
```

Payloads were verified as Python `bytes`, including the empty BLOB. Base-table rows also matched at every checkpoint.

Step 1 is the last compatible rollout state. Steps 2–4 remain recoverable through the supplied down migration: it restores OLD’s labels without changing stored data. **All representative committed updates and inserts survive rollback**, including their exact BLOB bytes. Restarting OLD alone at step 4 does not restore compatibility.

The smallest mitigation with unchanged SQL and reader contracts is an exclusive cutover: drain OLD before the up migration, then activate NEW; on rollback, drain NEW, apply the down migration, then restart OLD. This requires removing the proposed coexistence phase. If coexistence is required, a reader/schema change is necessary; adding a `label` alias alongside `title` would still violate OLD’s exact `SELECT *` column contract.

Evidence is limited to the specified sequential, SQL-only SQLite fixture. No concurrency, crash recovery, application runtime, or other database engine was tested. All supplied files and skill resources remained unchanged, verified by SHA-256 manifests; no scratch files, dependencies, network access, or deployment were used.
