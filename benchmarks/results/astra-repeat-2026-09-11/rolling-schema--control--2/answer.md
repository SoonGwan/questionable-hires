I’ll inspect the release configuration, rollout and rollback procedures, and relevant checks without running a deployment.

**Blocked for rollout and rollback as documented.**

- **Rollout breaks running instances.** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before old instances are replaced. [old_reader.py](project/old_reader.py#L1) immediately fails with `no such column: name`.
- **Rollback breaks restarted instances.** [release.md](project/release.md#L1) restarts the old binary before restoring `name`, causing the same failure. Running the down migration first would instead break any remaining new instances. Reordering alone cannot support mixed versions.
- **Staging validation is missing.** The release explicitly states it has not run in staging.

Use an expand/contract migration that supports both versions during rollout and rollback, or define a coordinated downtime procedure. Rehearse the chosen procedure in staging before proceeding.

Verified using the supplied SQL and reader queries in an in-memory SQLite database. Both compatibility failures reproduced; the up/down round trip preserved sample data, including a row inserted after migration. No deployment ran and no files changed.
