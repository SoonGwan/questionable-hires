I’m using the Friday skill to test the supplied rollout and rollback sequence against the reader and write contracts, without changing any project files.

**Blocked by evidence at step 2.** OLD’s query executes successfully, but its returned column names violate the consumer contract.

Executed `python3 -B - <<'PY' … PY` using SQLite 3.44.0 and one disposable `:memory:` connection. The harness loaded each supplied SQL script unchanged with `executescript`, extracted both literal queries from `readers.py`, and executed both at all five checkpoints—including a fresh check at step 4.

Expected ordered columns:

- OLD: `[id, label, payload]`
- NEW: `[id, title, payload]`

| Checkpoint | Observed columns for successful queries | OLD result | NEW result | Rows |
|---|---|---|---|---|
| 1. Schema | `[id, label, payload]` | Active: compatible | Inactive: `no such column: title` | A |
| 2. Up migration | `[id, title, payload]` | **Active: incompatible labels** | Inactive: compatible | A |
| 3. New writes | `[id, title, payload]` | **Active: incompatible labels** | Active: compatible | B |
| 4. Restart OLD | `[id, title, payload]` | **Active: incompatible labels** | Inactive: compatible | B |
| 5. Down migration | `[id, label, payload]` | Active: compatible | Inactive: `no such column: title` | B |

Expected and observed **complete ordered rows matched exactly** for every successful query and for the underlying table:

```python
A = [(1, '첫 항목', b'\x00\xff'),
     (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

Payloads were also verified to be Python `bytes`, including the empty BLOB. Correct row values do not compensate for OLD receiving `title` instead of `label`. NEW’s errors at steps 1 and 5 are inactive-reader observations, not active blockers.

Step 1 is the last compatible checkpoint before the failure. The failure remains recoverable: these migrations replace only the view. Step 4’s code rollback does **not** restore OLD compatibility; step 5 does. The committed update to row 1 and insertion of row 3 both survive the down migration exactly. No irreversible data loss was observed in this sequence.

The smallest compatible mitigation with the literal readers unchanged is an **exclusive cutover**: drain OLD before the up migration, then activate NEW; on rollback, drain NEW, apply the down migration, then restart OLD. This removes the proposed coexistence. If coexistence is required, a consumer/interface change is necessary: the shared view cannot expose exactly OLD’s three columns while also exposing `title` for NEW. Adding another column would itself break OLD’s exact `SELECT *` contract.

All assertions passed for the expected compatibility outcomes, write survival, and restored view. Project and skill file hashes were unchanged; no scratch files were created. Evidence is limited to the supplied SQL-only SQLite sequence; concurrency, application runtime, crash recovery, and other engines were outside scope. No fixes or deployment were performed.
