I’ll use the friday skill to review the proposal, then run the supplied SQL and both readers in one disposable in-memory sequence and compare the results with the contracts.

The up migration removes the `label` column name that OLD requires while OLD is still active. I’ll verify that incompatibility at every checkpoint and check whether the supplied down migration restores OLD’s contract while preserving all new writes and BLOB bytes.

**Blocked at step 2.** The up migration changes OLD’s returned columns from `[id, label, payload]` to `[id, title, payload]` while OLD remains active. Its SELECT succeeds, but its consumer contract fails.

Executed `python3 -B - <<'PY' … PY` using Python’s existing `sqlite3` (SQLite 3.44.0), one `:memory:` connection, the actual SQL files via `executescript`, and both literal queries extracted from `readers.py`. All ten reader checks ran, including the unchanged-schema checkpoint 4.

| Checkpoint | OLD observed | NEW observed | Complete rows |
|---|---|---|---|
| 1. Schema | Active: compatible; `[id,label,payload]` | Inactive: `no such column: title` | A |
| 2. Up | **Active: incompatible**; `[id,title,payload]` | Inactive: compatible | A |
| 3. New writes | **Active: incompatible**; `[id,title,payload]` | Active: compatible | B |
| 4. Restart OLD | **Active: incompatible**; `[id,title,payload]` | Inactive: compatible | B |
| 5. Down | Active: compatible; `[id,label,payload]` | Inactive: `no such column: title` | B |

Every successful NEW query returned exactly `[id,title,payload]`. Expected and observed full ordered rows matched:

```python
A = [(1, '첫 항목', b'\x00\xff'), (2, 'keep', b'')]
B = [(1, 'updated', b'\xfe\x00'), (2, 'keep', b''), (3, 'new', b'\x80')]
```

Payloads were verified as actual `bytes`, including the empty BLOB. Inactive NEW errors at steps 1 and 5 are observations, not blockers.

Step 1 is the last compatible checkpoint before the failure. Data remains recoverable throughout: step 5 restores OLD’s column contract and preserves the committed update and insert exactly. Restarting OLD alone at step 4 does not restore compatibility.

The smallest mitigation with unchanged reader contracts is a coordinated cutover: stop OLD before applying up, then activate NEW; on rollback, drain NEW, apply down, then restart OLD. This removes the proposed coexistence phase. If coexistence is required, versioned views and a reader-query change are necessary. Adding both names to the shared view would violate OLD’s exact `SELECT *` column contract.

All project and skill file hashes remained unchanged; no scratch files, dependencies, network access, or deployment were used. Evidence covers the specified local SQL contracts only; concurrency, crash recovery, application runtimes, and other database engines were outside scope.
