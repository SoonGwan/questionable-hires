I’ll inspect the release files and local verification tools, then run the supplied readers across the initial, migrated, and rolled-back schemas. I’ll preserve the release files and check which representative new-schema data survives rollback.

**Blocked for the documented rollout and rollback.**

- **Rollout:** [002_up.sql](project/002_up.sql) renames `name` to `display_name`. Old instances immediately fail with `no such column: name` while the rolling replacement proceeds.
- **Rollback:** [release.md](project/release.md) restarts the old binary before running the down migration. Its reader fails until that migration completes. Any remaining new instances then fail after the down migration.
- **Staging remains unverified:** the release explicitly says staging has not run.

Executed both supplied reader queries using SQLite 3.51.0 against an in-memory database:

| Schema state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| Up | Missing `name` | Pass |
| Up, after insert/update | Missing `name` | Pass |
| Down, after insert/update | Pass | Missing `display_name` |

**Rollback preserved the tested data.** Before rollback, I updated ID 1 to `Updated Alice — 새 이름` and inserted ID 3 as `New Carol`. After rollback, both values survived under `name`, alongside unchanged ID 2. IDs were preserved, and the integrity check passed.

These were synthetic SQL writes; no application-writer implementation was supplied, so writer compatibility is unverified.

Before proceeding, replace the immediate rename with a compatibility migration supporting both application versions, including verified writer synchronization, or define a coordinated maintenance cutover. Rehearse rollout and rollback in staging.

No deployment ran. All six release files remained unchanged, verified by SHA-256.
