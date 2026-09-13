I’ll use the Friday skill to check the documented release sequence, execute the reader checks across schema states, and inspect rollback data survival without changing release files or deploying.

The release renames a column before replacing the old instances, so the old reader appears incompatible with the first rollout step. Rollback also starts the old binary before restoring that column name. I’ll verify both failures and check whether inserted and updated values survive the reverse rename. No application writers are supplied, so those writes will be SQL fixtures only.

**Blocked by evidence:** the documented rollout and rollback orders both activate incompatible readers.

Executed the supplied queries against the actual migrations in in-memory SQLite; all checks completed.

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| After up migration | Missing `name` | Pass |
| After new-schema insert/update | Missing `name` | Pass |
| After down migration | Pass | Missing `display_name` |

- **Rollout blocker:** `002_up.sql` immediately breaks every active old reader, before instance replacement starts. The last compatible serving state is before that migration.
- **Rollback blocker:** restarting the old binary before `002_down.sql` fails with `no such column: name`. Running down while new instances serve would instead break their reads. Reverting the binary alone cannot recover service.

For rolling deployment, replace the rename with an expand/migrate/contract sequence that supports both column contracts and keeps writes consistent. Alternatively, authorize a maintenance window: stop all consumers, migrate, then start only the matching application version; reverse that sequence for rollback.

**Data survival verified:** before rollback, SQL fixtures updated row 1 to `Updated 사용자`, retained row 2 as `Untouched`, and inserted row 3 as `New 사용자`. All three survived down unchanged under `name`. The reverse rename preserves these values; it does not undo application data changes.

Application-writer compatibility and runtime/configuration readiness remain **unknown**: no writer implementations or runtime evidence were supplied. Staging explicitly has not run this release. Local SQL checks do not certify those missing checks.

Release-file hashes and Git status remained unchanged. No deployment or publishing occurred.
