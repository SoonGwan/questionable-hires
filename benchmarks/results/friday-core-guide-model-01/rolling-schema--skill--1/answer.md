I’m using the friday skill to check the documented rollout and rollback sequence, execute the supplied reader queries, and inspect data survival after rollback. I’ll keep the review inside this project and preserve the release files.

The rollout renames `name` while old instances still query it. Rollback also restarts the old binary before restoring that column. I’ll verify both failure points and check whether new-schema inserts and updates survive the reverse rename.

**Blocked by evidence.** The documented rollout and rollback orders both break active readers.

Executed both supplied queries against SQLite initial/up/down states, including an insert and update before rollback:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| Up | Missing `name` | Pass |
| Up, after insert/update | Missing `name` | Pass |
| Down, retaining changed data | Pass | Missing `display_name` |

- **Rollout blocker:** `002_up.sql` immediately removes the column old instances need, before their gradual replacement. The last compatible state for those instances is before migration. Preserve both contracts through an expand/migrate/contract transition, or use a coordinated maintenance cutover.
- **Rollback blocker:** Restarting the old binary before `002_down.sql` leaves it querying missing `name`. Running down while new readers remain active breaks those readers instead. Quiesce application access, reverse the migration, and start old instances; otherwise provide a schema compatible with both versions.
- **Data recovery:** The inserted row survived down, and the updated value survived under `name`. Untouched data also survived. The reverse rename restores the schema contract; it does **not** restore overwritten values.

All expected query outcomes, column labels, and surviving values were asserted. Application writers and runtime/configuration compatibility remain **unknown**: none were supplied. Staging explicitly has not run; local SQL does not certify it.

Release files and existing user changes were preserved. No deployment, installation, external services, or delegation occurred.
