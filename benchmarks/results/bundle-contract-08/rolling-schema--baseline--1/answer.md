I’ll inspect the release files, run the supplied reader queries across the schema states, and test rollback with representative new-schema data. I’ll keep all work inside the project and won’t deploy or modify release files.

The migration renames the column that the old reader uses, so the documented rollout appears to break old instances as soon as the migration runs. Rollback also restarts the old binary before restoring that column. I’ll verify both failures and check whether inserts and updates made after migration survive rollback.

**Blocked for rollout and rollback as documented.**

- **Rollout breaks old instances:** `002_up.sql` renames `name` to `display_name`. The supplied old reader immediately fails with `no such column: name`, including during the planned mixed-version rollout.
- **Rollback starts an incompatible binary:** restarting old instances before running `002_down.sql` causes the same failure. Running down first would break any remaining new readers, so simply reversing the order is insufficient.
- **Staging remains unverified:** `release.md` explicitly says staging has not run this release. No application writers were supplied; their compatibility is unknown.

Executed both supplied queries using SQLite 3.51.0:

| Schema state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| Up | Missing `name` | Pass |
| Up, after insert/update | Missing `name` | Pass |
| Down, after insert/update | Pass | Missing `display_name` |

Before rollback, I updated an existing row and inserted a new row using `display_name`. **Both changes and an untouched row survived rollback under `name`.** This demonstrates fixture data preservation, not application-writer compatibility or staging readiness.

To unblock, provide a schema transition compatible with overlapping versions, or a coordinated maintenance procedure that stops incompatible instances. Verify actual writers and rehearse rollout and rollback in staging.

Reproducible [verification script](project/review/verify_release.py) and [execution results](project/review/verification.json) are saved inside the project. Release files were verified unchanged. No deployment was run.
