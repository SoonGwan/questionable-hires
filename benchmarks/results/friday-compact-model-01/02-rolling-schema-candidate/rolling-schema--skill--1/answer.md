I’ll use the Friday skill to review the release and run the requested schema and rollback checks in disposable local databases, preserving the release files.


The migration renames a column that the old reader still uses, so the planned migration-first rollout appears incompatible. I’ll check both readers before and after each migration, then insert and update representative new-schema data to see what survives rollback. No application writers are supplied, and staging has not run this release.


**Not ready for the planned rollout or rollback.** The first incompatible step is `002_up.sql`: renaming `name` immediately breaks old instances. The last compatible checkpoint is the initial schema with old instances, before migration. No irreversible data loss appeared in the exercised rollback.

Executed the supplied reader queries against in-memory SQLite:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial, seeded rows | Pass | Missing `display_name` |
| After up | Missing `name` | Pass |
| After new-schema insert/update | Missing `name` | Pass |
| After down | Pass | Missing `display_name` |

Concrete blockers:

- **Rollout order:** Migration first, then replacing instances individually, leaves old readers failing throughout coexistence. Application-first also fails against the initial schema. Use an expand/migrate/contract change with compatible readers and writers, or a coordinated maintenance cutover.
- **Rollback order:** Restarting the old binary before down makes it query a missing column. Running down while new instances remain active breaks those readers. A maintenance rollback must quiesce applications, run down, then start old instances.

Rollback preserved all tested current data: updating row 1 to `"Updated user"` and inserting row 3 as `"New user"` survived under `name`; unchanged row 2 also survived. Down reverses the column rename, **not the data updates**.

These were representative SQL writes, not application-writer verification: no writers were supplied. Runtime/configuration compatibility and staging readiness remain unverified; `release.md` explicitly says staging has not run.

Release files and existing user changes were preserved. No deployment, external service, or dependency installation was performed.
