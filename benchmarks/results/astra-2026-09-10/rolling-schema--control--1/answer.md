I’ll inspect the release configuration, rollout and rollback procedures, and supporting checks for concrete blockers. I won’t run a deployment.

This release is **not ready for rollout or rollback**.

- **Rollout blocker:** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before old instances are replaced. [old_reader.py](project/old_reader.py#L1) still queries `name`, so those instances fail immediately after migration.
- **Rollback blocker:** [release.md](project/release.md#L1) restarts the old binary before restoring `name`, so the restarted instances fail. Running the down migration first would instead break any remaining new instances.
- **Validation gap:** [release.md](project/release.md#L1) explicitly says staging has not run this release.

Use an expand/contract migration that keeps both readers compatible throughout rollout and rollback, then rehearse both procedures in staging before release.

Verified using the actual migrations and reader queries against in-memory SQLite: both documented failure windows produce `no such column` errors. The migration round trip preserves the sample row, but that does not make the deployment sequence safe.

No deployment ran; no files changed.
