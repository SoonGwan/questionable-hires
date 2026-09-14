I’m using the friday skill to check the release order, execute the supplied reader queries across schema states, and inspect rollback data survival. I’ll keep the review inside this project and preserve the release files.

**Blocked by evidence.** The documented rollout and rollback orders both break active readers.

Executed the supplied `QUERY` constants against SQLite initial/up/down states; all phases completed without truncated results.

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| After up | Missing `name` | Pass |
| After new-schema insert/update | Missing `name` | Pass |
| After down | Pass | Missing `display_name` |

- **Rollout blocker:** `002_up.sql` immediately renames `name`, breaking old instances before replacement begins. The last compatible state for the running old application is before this migration. Preserve both contracts through an expand/migrate/contract change, with verified writer synchronization, or use a coordinated maintenance cutover.
- **Rollback blocker:** Restarting the old binary before `002_down.sql` leaves it querying a missing column. Running down while new instances remain active breaks those instances instead. A maintenance rollback must stop/drain new instances, run down, then start old instances; mixed-version operation requires a compatible schema.

**Data recovery:** Before down, I updated row 1 through `display_name` and inserted row 3. After down, the old reader returned all three rows with the updated value, unchanged control row, and new insert intact under `name`. The tested reversal preserves current data; it does **not** restore the overwritten original value.

Application writer compatibility and runtime/configuration readiness remain **unknown**: no writer implementations or supporting evidence were supplied. Staging explicitly has not run.

Release files and existing user changes were preserved. No deployment, publishing, dependency installation, or external services were used.
