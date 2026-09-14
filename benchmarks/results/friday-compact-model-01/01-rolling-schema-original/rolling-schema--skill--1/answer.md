I’ll use the friday skill to review the documented release sequence, execute the supplied reader checks, and test rollback with new-schema data. I’ll keep all work inside this project and preserve the release files.


**Blocked by evidence:** the documented rollout and rollback both activate readers against incompatible schemas.

Executed the supplied reader queries in local, in-memory SQLite; all phases completed without truncated results.

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| After up migration | Missing `name` | Pass |
| After new-schema insert/update | Missing `name` | Pass |
| After down migration | Pass | Missing `display_name` |

- **Rollout blocker:** `002_up.sql` renames `name` while old instances still serve traffic. This is the first incompatible step; the last compatible state is the initial schema with old instances. Preserve both column contracts through an expand/migrate/contract transition, with verified write synchronization, or use a coordinated maintenance cutover.
- **Rollback blocker:** restarting the old binary before running `002_down.sql` immediately breaks its reader. Reversing that order would break any remaining new instances. Rollback needs compatible intermediate schemas or a coordinated stop, schema reversal, and restart.

**Data rollback passed for the exercised SQL writes.** Before rollback, I updated row 1 to `Renamed by new schema` and inserted row 3 as `New user`. After down migration, both survived under `name`; unchanged row 2 also survived. The down migration restores the column name, not previous data values.

Application writers were not supplied, so their compatibility remains **unknown**. Runtime/configuration readiness is unverified, and `release.md` explicitly says staging has not run this release. Local SQL results do not certify those checks.

Release files and existing user changes were preserved. No deployment or publishing occurred.
