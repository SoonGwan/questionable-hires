I’ll use the Friday skill to check the documented rollout and rollback states, execute the supplied reader queries, and inspect data survival after rollback. I’ll keep all work inside the project and preserve the release files.

**Blocked by evidence.** The documented rollout and rollback both activate readers against incompatible schemas.

- **Rollout blocker:** [002_up.sql](project/002_up.sql#L1) renames `name` before old instances stop. The supplied old query then fails with `no such column: name`, including throughout mixed-version rollout.
- **Rollback blocker:** [release.md](project/release.md#L1) restarts the old binary before running the down migration. Its reader fails until down completes. Running down while new instances remain active instead breaks their reader.

Executed both supplied queries using in-memory SQLite 3.51.0:

| Schema/data state | Old reader | New reader |
|---|---|---|
| Initial, seeded rows | Pass | Missing `display_name` |
| Up | Missing `name` | Pass |
| Up, after update and insert | Missing `name` | Pass |
| Down, retaining those writes | Pass | Missing `display_name` |

Rollback preserved the updated existing value (`Alice updated — 김`), an unchanged row, and a newly inserted row exactly. **No data loss was observed from the reverse rename.** These were representative SQL writes; no application writers were supplied, so writer compatibility remains unknown.

The first incompatible step is applying up with old instances active; the last demonstrated compatible pre-release state is the initial schema with the old reader. To retain rolling deployment, provide a schema and synchronization strategy supporting both versions before switching consumers. Alternatively, explicitly adopt downtime: stop all consumers before each schema change and start only the matching version afterward.

Staging has explicitly not run; runtime and configuration readiness remain unverified. All six release files were preserved. No deployment or external services were used.
