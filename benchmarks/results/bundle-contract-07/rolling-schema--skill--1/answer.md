I’m using the Friday skill to check the documented rollout and rollback sequence, execute the supplied reader queries, and inspect data survival after rollback. I’ll keep all work inside the project and preserve the release files.

**Blocked by evidence.** The documented rolling rollout and rollback both expose old instances to an incompatible schema.

Executed both supplied reader queries in in-memory SQLite using the supplied migrations. All phases completed without truncation.

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Fails: `no such column: display_name` |
| After up migration | Fails: `no such column: name` | Pass |
| After new-schema insert/update | Same failure | Pass |
| After down migration | Pass | Fails: `no such column: display_name` |

Concrete blockers:

- **Rollout:** `002_up.sql` renames `name` before old instances are replaced. This is the first incompatible step; existing readers immediately fail. The last compatible serving state is before the migration. Preserve rolling deployment by introducing an expand/migrate/contract transition with both column contracts and verified write synchronization.
- **Rollback:** Restarting the old binary before `002_down.sql` produces the same failure. Reordering alone cannot support mixed versions: after down, new readers fail. An alternative requires a coordinated maintenance window: stop traffic and all instances, migrate, start the matching binary, then resume traffic.

**Data recovery:** Before down, I inserted `(3, 'New user')` and updated ID 1 through `display_name`. After down, the old reader returned:
```text
1  Updated user
2  Unchanged user
3  New user
```
The rename preserved the inserted and updated values. It did **not** restore the prior value of ID 1; reversing the schema does not undo application data changes.

Application writers were not supplied, so these SQL fixtures do not establish writer compatibility. Staging has not run; runtime and configuration readiness remain unknown.

Release files and existing user changes were preserved. No deployment, installation, external service, or delegation was used.
