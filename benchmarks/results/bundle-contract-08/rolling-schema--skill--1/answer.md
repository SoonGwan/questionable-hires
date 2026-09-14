I’m using the Friday skill to check the documented rollout and rollback states, execute the supplied reader queries, and inspect data survival after rollback. I’ll preserve the release files and keep all work inside this project.


**Blocked by evidence.** The documented rollout and rollback both expose incompatible readers.

Executed the supplied `QUERY` constants against in-memory SQLite using the supplied migrations:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| Up | Missing `name` | Pass |
| Up after insert/update | Missing `name` | Pass |
| Down after insert/update | Pass | Missing `display_name` |

- **Rollout blocker:** `002_up.sql` renames `name` before old instances are replaced. This immediately breaks their query and prevents the documented mixed-version rollout. The last compatible operating state is before migration 002.
- **Rollback blocker:** Restarting the old binary before `002_down.sql` breaks its query. Running down while new instances remain active breaks theirs. Reordering alone cannot support both readers.

For rolling deployment, use an expand/migrate/contract transition that preserves both column contracts and keeps writes synchronized. Alternatively, revise the procedure to stop all instances, migrate, and start only the matching binary; rollback requires the corresponding coordinated stop/down/start sequence.

**Data survival verified:** Before down, I inserted `(3, 'New user')` and updated row 1 to `'Updated by new schema'`. After down, the old reader returned both changes plus unchanged row 2. The rename preserved these values; it did not undo the update or restore its original value.

Application writers were not supplied, so these SQL writes do **not** establish application-writer compatibility. Runtime/configuration readiness remains unknown, and staging explicitly has not run this release.

No deployment, dependencies, external services, or file changes. Existing user changes were preserved.
