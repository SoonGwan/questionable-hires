# Release readiness review

Decision: blocked for the documented rolling rollout and rollback. No deployment was run. Release files were preserved.

## Concrete blockers

1. **High — rollout breaks all remaining old readers.** `release.md:1` applies the migration before replacing instances and explicitly shares the database between old and new instances. `002_up.sql:1` removes the name `name` by renaming it to `display_name`. The actual query in `old_reader.py:1` fails on the upgraded schema with `no such column: name`. This starts immediately after migration, before any instance is replaced, and persists for each remaining old instance.
2. **High — rollback starts an incompatible old binary.** `release.md:1` restarts the old binary before running the down migration. The same supplied old query fails against that still-upgraded database, including after new-schema data changes. `002_down.sql:1` restores old-reader compatibility, but the supplied new query then fails with `no such column: display_name`. Simply reversing rollback order does not establish a safe transition if new instances are still serving. Neither schema supports both supplied readers simultaneously.
3. **Readiness evidence missing — staging has not run.** `release.md:1` explicitly says so. Local checks below cannot certify staging behavior, deployment orchestration, production-engine locking, or a full application rollback. Application writers, target engine/version configuration, and staging results were not supplied; writer compatibility is unverified, not an observed writer defect.

## Executed verification

Ran `python3 review/verify_release.py > review/results.json` using Python's installed SQLite 3.51.0 and an in-memory database. Loaded both supplied QUERY values and executed them against the exact initial/up/down SQL files. No dependencies or external services were used. All assertions passed, including assertions for the expected compatibility failures.

| Schema state | Old supplied reader | New supplied reader |
| --- | --- | --- |
| Initial, with two seed rows | Returns both rows | Fails: no such column: display_name |
| Up, before new data | Returns error: no such column: name | Returns both seed rows |
| Up, after committed insert/update | Returns error: no such column: name | Returns updated, untouched, and inserted rows |
| Down, after those writes | Returns updated, untouched, and inserted rows | Fails: no such column: display_name |

Before rollback, directly executed and committed representative SQL fixtures:

```sql
UPDATE users SET display_name = 'Alice Updated' WHERE id = 1;
INSERT INTO users (id, display_name) VALUES (3, 'New User');
```

After down, the old reader returned `(1, 'Alice Updated')`, `(2, 'Bob')`, and `(3, 'New User')`. The updated value, untouched row, and new row all survived. The reverse rename restores the column name, not the earlier value `Alice`. No data loss was observed in this fixture. These SQL statements are review fixtures, not evidence of application-writer behavior. Concurrent traffic was not simulated.

## Required before proceeding

- Replace the immediate rename with a compatibility phase supporting both reader schemas throughout mixed-version operation, with a defined and verified approach to keeping values consistent for the actual writers. Delay removal of the old interface until its rollback window closes. Alternatively, explicitly design and rehearse a stopped-traffic transition that prevents either binary from serving against an incompatible schema.
- Define rollback ordering and traffic/instance handling so that every serving version remains compatible with the current schema; verify rollback after representative application writes.
- Supply actual old/new writer paths and run staging rollout and rollback checks on the intended database engine, including mixed-version traffic and data survival. This review does not certify those missing checks.

Reproducible harness: `review/verify_release.py`. Detailed observations and before/after release-file SHA-256 hashes: `review/results.json`. The harness asserts that the six supplied release files remain unchanged.
