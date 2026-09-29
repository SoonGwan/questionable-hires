I’ll use the Friday skill to inspect the proposal and contracts, then run the supplied SQL and both reader queries through all five checkpoints in one in-memory database. I’ll preserve the files and make no deployment changes.

The up migration changes `public_items` from `label` to `title`, while OLD requires the `label` column name. I’ll check that mismatch alongside exact row values and BLOB bytes, then continue through rollback to see whether the new writes survive.

**Blocked by evidence at step 2.** OLD’s `SELECT` succeeds, but its returned column names violate the consumer contract.

Executed `python3 -B - <<'PY' … PY` using SQLite 3.44.0 and one disposable `:memory:` connection. The harness executed each supplied SQL script unchanged, ran both literal queries at all five checkpoints, and checked `cursor.description`, complete ordered rows, and Python `bytes` payload types.

| Checkpoint | OLD: expects `[id, label, payload]` | NEW: expects `[id, title, payload]` |
|---|---|---|
| 1 — schema | Active: compatible | Inactive: `no such column: title` |
| 2 — up | **Active: incompatible**, receives `[id, title, payload]` | Inactive: compatible |
| 3 — new writes | **Active: incompatible**, same labels | Active: compatible |
| 4 — restart OLD | **Active: incompatible**, same labels | Inactive: compatible |
| 5 — down | Active: compatible | Inactive: `no such column: title` |

The inactive NEW errors at steps 1 and 5 are not blockers.

Expected and observed complete rows matched for every successful query:

```python
# Steps 1–2
[(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]

# Steps 3–5
[(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

All payloads remained BLOB bytes, including the empty BLOB. Correct values do not compensate for OLD’s incorrect column labels.

Step 1 is the last compatible checkpoint before the blocker. The later states remain data-recoverable: the down migration only restores the view alias. Step 4’s code-only rollback does **not** restore OLD compatibility; step 5 does. Both the committed update and inserted row survive rollback exactly.

The smallest mitigation retaining the literal queries is a coordinated cutover: drain OLD before applying up, then activate NEW; on rollback, drain NEW, apply down, then restart OLD. This removes coexistence. If coexistence is required, a reader/view contract change is necessary: adding both names to this view would also break OLD’s exact `SELECT *` column contract.

No files were changed; before/after project file hashes matched. No scratch files, dependencies, network access, or deployment were used. Evidence covers the authored SQL-only sequence; concurrency, crash recovery, application runtimes, and other database engines remain outside scope.
