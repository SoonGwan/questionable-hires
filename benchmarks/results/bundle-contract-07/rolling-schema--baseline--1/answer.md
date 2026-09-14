I’ll inspect the release and its verification tools, then test the supplied readers across the initial, upgraded, and rolled-back schemas, including data written before rollback. I’ll keep all work inside this project and preserve the release files.

The local rehearsal confirms blockers in both sequences: the up migration breaks the old reader before instance replacement, and restarting the old binary before the down migration hits the same missing-column error. The synthetic insert and update both survive rollback. Application-writer compatibility remains unverified, and the release notes say staging has not run.

**Blocked for rollout and rollback as documented.**

- **Rollout:** `002_up.sql` renames `name` to `display_name`, immediately breaking old instances with `no such column: name`.
- **Rollback:** restarting the old binary before `002_down.sql` produces that same failure. Running down first would instead break remaining new readers.
- **Readiness gaps:** staging has not run, and no application-writer code or verification was supplied.

Executed both supplied queries on SQLite 3.51.0:

| Schema state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| Up | Missing `name` | Pass |
| Up after insert/update | Missing `name` | Pass |
| Down after insert/update | Pass | Missing `display_name` |

Rollback preserved the updated existing row, untouched row, and newly inserted row. These were synthetic SQL writes, not application-writer evidence.

Before release, provide a compatibility migration supporting overlapping versions or a coordinated downtime procedure, then verify actual writers and rehearse rollout/rollback in staging.

[Executed evidence](project/release_review/evidence.json) · [Reproducible verification](project/release_review/verify.py)

Release files are unchanged. No deployment or external services were used.
