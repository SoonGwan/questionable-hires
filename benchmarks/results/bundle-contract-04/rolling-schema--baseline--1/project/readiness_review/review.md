# Release readiness review

**Decision: block the documented rollout and rollback.** No deployment was run.

## Concrete blockers

1. **Rollout breaks running old instances.** `release.md:1` migrates first and then replaces instances one at a time against a shared database. `002_up.sql:1` immediately renames `name` to `display_name`. The exact query from `old_reader.py:1` fails after migration with `no such column: name`, throughout the period old instances remain. Replacing the application first also fails: the new query needs a column absent from the initial schema.
2. **Rollback starts an incompatible old binary.** `release.md:1` restarts the old binary before applying `002_down.sql:1`. The old query fails on that still-upgraded schema, including after new-schema writes. The down migration restores old-reader compatibility, but any remaining new instances then fail with `no such column: display_name`. Reversing the order alone does not establish a safe live transition.
3. **Staging validation is outstanding.** `release.md:1` explicitly says staging has not run this release. These local SQL results cannot certify staging, mixed-instance operation, or a production rollback rehearsal.

## Executed verification

Ran `python3 readiness_review/verify.py` using installed Python and SQLite 3.51.0, with an in-memory database. The script executes the supplied migration SQL and extracts and executes both supplied reader queries unchanged. Full results, schemas, rows, errors, and release-file SHA-256 hashes are in `results.json`.

| Schema state | Old reader | New reader |
| --- | --- | --- |
| Initial, seeded | Pass | Fail: no such column: display_name |
| Up, before writes | Fail: no such column: name | Pass |
| Up, after committed insert/update | Fail: no such column: name | Pass |
| Down, after those writes | Pass | Fail: no such column: display_name |

Seeded `(1, 'Alice')` and `(2, 'Bob')`. On the upgraded schema, committed an update of ID 1 to `display_name = 'Alice updated'` and inserted `(3, 'Carol new')`. After down, the old reader returned:

```text
id  name
1   Alice updated
2   Bob
3   Carol new
```

The updated value, untouched row, new row, and IDs all survived. Down renames the column back; it does not restore the original value of Alice. The schema again has `id INTEGER PRIMARY KEY` and `name TEXT NOT NULL`. No data loss was observed in this representative probe.

These are synthetic SQL writes. No application writer code was supplied, so actual old/new writer compatibility, synchronization behavior, and full application behavior are unverified. The target database/runtime is not specified; local SQLite success establishes only the tested behavior. No concurrency, operational migration locking, or staging checks were performed.

## Required before approval

- Replace the immediate rename with a reviewed compatibility transition that supports both readers while instances overlap. An additive column/backfill approach also needs an explicit, tested writer synchronization strategy; adding a column alone is insufficient. Alternatively, define and rehearse an approved maintenance window with traffic and workers stopped while schema and binary versions are aligned.
- Revise rollback to ensure each serving binary sees a compatible schema, and rehearse it after representative new-version writes. Account for remaining new instances before restoring the old schema.
- Supply actual application writers and verify their insert/update paths during transitions. Run staging rollout and rollback checks on the intended database/runtime, including mixed versions if rolling deployment remains the plan.

All six supplied release files were preserved byte-for-byte during verification. Initial Git status was clean. Only local review artifacts were added; no dependencies, external services, publishing, or deployment were used.
