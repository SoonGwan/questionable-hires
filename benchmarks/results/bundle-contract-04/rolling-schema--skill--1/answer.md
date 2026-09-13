I’m using the Friday skill to check the rollout sequence, execute the supplied readers across schema states, and inspect rollback data survival. I’ll keep all work inside this project and preserve the release files.


The migration renames the column before old instances are replaced, so the documented rollout exposes old readers to the new schema. Rollback also starts old code before restoring the old column name. I’ll verify both failures and check whether inserted and updated values survive the down migration.


**Blocked by evidence.** The documented rollout and rollback orders both break active readers.

Executed the supplied queries in local SQLite against all relevant states:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| After up | Missing `name` | Pass |
| After new-schema insert/update | Missing `name` | Pass |
| After down | Pass | Missing `display_name` |

- **Rollout blocker:** `002_up.sql` immediately breaks old instances, before replacement begins. The last compatible state for the active old application is immediately before this migration.
- **Rollback blocker:** Restarting the old binary before `002_down.sql` leaves it querying a missing column. Running down while new instances remain active breaks their readers too.

For the documented rolling strategy, use an expand/migrate/contract transition that supports both column contracts, with verified writer synchronization. Alternatively, require a coordinated maintenance window: stop all application access, migrate, then start the matching binary; reverse that sequence for rollback.

**Data survival verified:** Before down, I updated an existing value and inserted a new row through `display_name`. After down, the old reader returned both changed values and the untouched row under `name`. The rename preserved this data; it did not restore the original value overwritten by the update.

Application writers were not supplied, so these SQL fixtures do **not** establish writer compatibility. Runtime/configuration readiness remains unknown; `release.md` explicitly says staging has not run.

Release-file hashes remained unchanged, and existing user changes were preserved. No deployment, publishing, dependency installation, or external services were used.
