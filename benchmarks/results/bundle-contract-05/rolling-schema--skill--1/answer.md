I’m using the friday skill to check the documented rollout and rollback states, execute the supplied SQL checks, and inspect rollback data survival without changing release files or deploying.


The migration renames the column that the old reader still uses, so the documented migration-first rollout appears incompatible. I’ll verify both readers before and after migration, then add an insert and update under the new schema and check what survives rollback. These writes are SQL probes; no application writer code was supplied.


**Blocked by evidence.** The rollout and rollback orders in [release.md](project/release.md) both expose incompatible readers.

Executed the supplied queries against SQLite in memory; all phases completed:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| After up migration | Missing `name` | Pass |
| After new-schema insert/update | Missing `name` | Pass |
| After down migration | Pass | Missing `display_name` |

- **Rollout blocker:** `002_up.sql` immediately breaks active old instances. The last compatible state is before migration. Replacing applications first also fails because the new reader requires `display_name`.
- **Rollback blocker:** Restarting the old binary before `002_down.sql` breaks its reads. Running down while new instances remain active breaks their reads instead.
- **Mitigation:** Use an expand/migrate/contract transition supporting both versions, with a verified write-synchronization contract. Alternatively, explicitly adopt downtime: stop all instances, migrate, then start only the matching version; reverse this sequence for rollback.

**Rollback preserved the tested data.** Before down, I inserted `(2, 'New user')` and updated existing row 1 to `'Updated existing'`. After down, both survived under `name`. Down reverses the column rename; it does **not** restore the original value `'Original'`.

Application writer behavior and runtime/configuration compatibility remain **unknown**: no writer implementation or supporting evidence was supplied. Staging explicitly has not run; these local checks do not certify it.

Release files and existing user changes were preserved. No deployment, publishing, dependency installation, or external access occurred.
