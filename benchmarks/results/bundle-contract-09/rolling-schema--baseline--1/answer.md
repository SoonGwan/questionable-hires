I’ll inspect the release files and available local checks, exercise the supplied reader queries across the schema transitions, and test rollback with representative writes. I won’t deploy or modify release files.

**Blocked for rollout and rollback as documented.**

Executed both supplied reader queries using local SQLite 3.51.0:

| Schema state | Old reader | New reader |
|---|---|---|
| Initial, seeded | Pass | Fails: missing `display_name` |
| After up migration | Fails: missing `name` | Pass |
| After new-schema writes | Fails: missing `name` | Pass |
| After down migration | Pass | Fails: missing `display_name` |

Concrete blockers:

- **Rollout:** `002_up.sql` immediately removes `name`. The old instances still serving during the documented rolling replacement will fail.
- **Rollback:** Restarting the old binary before `002_down.sql` makes its reader fail until the migration completes. Any new instances remaining afterward will fail.
- **Staging:** `release.md` explicitly says staging has not run this release. That verification remains outstanding.

Rollback **preserved the tested data**: I committed an update to an existing row and an insert using `display_name`, then ran the supplied down migration. The updated Unicode value, inserted row, untouched row, and all IDs survived under `name`; integrity checking passed. These were synthetic SQL writes—no application-writer implementation was supplied or verified.

Before proceeding, provide a schema compatible with both versions during overlap, with an explicit write synchronization strategy, or revise the procedure to stop traffic and coordinate schema/application transitions. Validate the chosen rollout and rollback in staging with actual application writers.

All six release files remained unchanged. No deployment, publishing, dependency installation, or external services were used.
