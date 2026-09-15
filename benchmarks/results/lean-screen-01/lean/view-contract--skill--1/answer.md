I’ll use the friday skill to review the sequence and run the supplied SQL and literal readers in one in-memory database, checking labels and full values against the contracts. I’ll preserve all project files.



## Blocked at step 2

`002_up.sql` changes the returned columns from `[id, label, payload]` to `[id, title, payload]` while OLD remains active. OLD’s `SELECT` succeeds and returns correct values, but its name-based consumer contract fails.

### Executed evidence

Ran `python3 -B - <<'PY' … PY` using local SQLite **3.51.0**, one disposable `:memory:` connection, the actual supplied scripts via `executescript`, and both literal queries extracted from `readers.py`. Checked ordered column labels, complete ordered rows, and Python `bytes` payloads at every checkpoint.

| Checkpoint | OLD result | NEW result | Complete rows |
|---|---|---|---|
| 1. Schema; OLD active | Compatible | Inactive: `no such column: title` | A |
| 2. Up; OLD active | **Incompatible labels** | Inactive: compatible | A |
| 3. Writes; both active | **Incompatible labels** | Compatible | B |
| 4. Restart OLD; unchanged schema | **Incompatible labels** | Inactive: compatible | B |
| 5. Down; OLD active | Compatible | Inactive: `no such column: title` | B |

Expected and observed complete rows matched exactly wherever queries executed:

```text
A = [(1, '첫 항목', b'\x00\xff'),
     (2, 'keep', b'')]

B = [(1, 'updated', b'\xfe\x00'),
     (2, 'keep', b''),
     (3, 'new', b'\x80')]
```

OLD requires `[id, label, payload]`; it observes `[id, title, payload]` at steps 2–4. NEW requires and receives `[id, title, payload]` wherever it executes. Inactive NEW errors at steps 1 and 5 are **not blockers**.

### Recovery and smallest mitigation

- **Last compatible checkpoint:** step 1. Subsequent states remain data-recoverable using the supplied down script.
- **Code rollback alone fails:** restarting OLD at step 4 leaves incompatible view labels.
- **New writes survive schema rollback:** step 5 preserves the updated row, unchanged empty BLOB row, and inserted row with exact bytes. The down script only recreates the view.
- **Coexistence requires separate reader interfaces:** preserve the original three-column `public_items` view for OLD and give NEW a separate view/query target exposing `title`. Adding `title` to the existing view would also violate OLD’s exact `SELECT *` column contract. With both literal queries frozen, the proposed shared-view coexistence cannot be compatible.
- For rollback ordering, drain NEW, apply down, then restart OLD. This addresses step 4, but does not fix rollout coexistence.

All ten reader executions were checked, including checkpoints after the first blocker. File hashes confirmed project and skill resources unchanged; no scratch files, dependencies, network, or deployment were used. Evidence covers the supplied SQL-only fixture; concurrency, crashes, application writers, and other engines remain outside scope.
