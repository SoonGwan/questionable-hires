I’ll use the Friday skill to review the release order and run local schema and reader checks, including new-schema writes before rollback. I’ll preserve release files and won’t deploy anything.

The migration renames the column that old readers use. That appears incompatible with both the migration-first rollout and the old-binary-first rollback. I’ll execute both supplied queries in each schema state and check whether inserted and updated data survives the down migration.

**Blocked by evidence.** The documented rollout and rollback orders both break active readers.

Executed both supplied queries using in-memory SQLite 3.51.0:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| Up migration | Missing `name` | Pass |
| Up, after insert/update | Missing `name` | Pass |
| Down, after insert/update | Pass | Missing `display_name` |

- **Rollout blocker:** [002_up.sql](project/002_up.sql#L1) immediately removes `name` while old instances remain active under [release.md](project/release.md#L1). This is the first incompatible step; the last compatible state is before migration. Preserve both column contracts with an expand/migrate/contract release, or explicitly adopt a coordinated maintenance cutover.
- **Rollback blocker:** Restarting the old binary before running down leaves its query broken. For these artifacts, quiesce all instances, run down, then start old instances. Running down while new instances remain active breaks their query.
- **Readiness gap:** Staging explicitly has not run. Application writers and runtime/configuration evidence were not supplied, so their compatibility remains unknown.

**Data recovery check:** Before rollback, I updated row 1 to `Updated — 새 이름` and inserted row 3 as `Inserted — 새 사용자`. Both values, their IDs, and unchanged row 2 survived down exactly. The rename reverses the schema without losing these tested writes; it does not undo their values. These were representative SQL writes, not application-writer verification.

Release files remained unchanged. No deployment or external services were used.
