I’m using the Friday skill to test the supplied SQL sequence and reader contracts in memory, then assess rollout and rollback without changing the proposal.

## Blocked by evidence

**Step 2 is the first blocker:** `002_up.sql` changes the view’s second column from `label` to `title` while OLD remains active. OLD’s `SELECT` succeeds, but its required ordered column names fail.

### Executed verification

Ran `python3 -B - <<'PY' … PY` using SQLite **3.51.0**, one disposable `sqlite3.connect(':memory:')`, and:

- `executescript(Path(script).read_text())` for all four supplied SQL scripts, in the specified order.
- Both literal queries extracted from `readers.py` at **all five checkpoints**, including the unchanged-schema restart.
- Exact comparisons of `cursor.description` column labels, complete ordered rows, and Python `bytes` payloads.

| Checkpoint | OLD observation | NEW observation |
|---|---|---|
| 1 — baseline | Active: compatible | Inactive: `no such column: title` |
| 2 — up | **Active: wrong column labels** | Inactive: compatible |
| 3 — new writes | **Active: wrong column labels** | Active: compatible |
| 4 — restart OLD | **Active: wrong column labels** | Inactive: compatible |
| 5 — down | Active: compatible | Inactive: `no such column: title` |

OLD expects `[id, label, payload]`; it receives `[id, title, payload]` at checkpoints 2–4. NEW expects and receives `[id, title, payload]` whenever its query succeeds. The inactive NEW errors at checkpoints 1 and 5 are **not blockers**.

### Exact values

Every successful query returned the expected complete rows below, in order. Payload notation denotes verified BLOB bytes, including the empty BLOB.

```text
Checkpoints 1–2:
(1, '첫 항목', X'00ff')
(2, 'keep',    X'')

Checkpoints 3–5:
(1, 'updated', X'fe00')
(2, 'keep',    X'')
(3, 'new',     X'80')
```

Matching values do not compensate for OLD’s incompatible column labels.

### Recovery and smallest mitigation

- **Last fully compatible checkpoint before failure: 1.** Subsequent states remain recoverable: the migrations change only the view.
- **Code rollback at step 4 fails to restore compatibility.** Step 5 restores OLD’s contract.
- **New writes survive rollback:** the update to row 1, inserted row 3, unchanged row 2, and all payload bytes remain exact after the down migration.
- **For the required coexistence:** retain the legacy view and adapt NEW to `SELECT id, label AS title, payload FROM public_items ORDER BY id`. This requires revising the proposal; adding both columns would break OLD’s exact `SELECT *` shape.
- **If reader contracts must remain fixed:** replace coexistence with a coordinated reader pause. Drain OLD before up, then start NEW; on rollback, drain NEW, apply down, then restart OLD.

Mitigations were assessed, not applied. All ten reader outcomes and five base-table states were checked. File hashes confirmed supplied files and skill resources were unchanged; no scratch files were created. Evidence covers the authored SQL-only sequence, not concurrency, crashes, application runtimes, or other database engines.
