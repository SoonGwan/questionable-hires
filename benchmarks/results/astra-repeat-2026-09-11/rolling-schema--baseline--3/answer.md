I’ll inspect the release configuration, rollout and rollback procedures, and available checks for concrete blockers. I won’t run a deployment.

**Not ready for rollout or rollback.** Two compatibility blockers are confirmed:

- **Rollout breaks running instances.** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before replacing instances. The [old reader](project/old_reader.py#L1) still queries `name`, so it fails immediately after migration and throughout mixed-version operation.
- **Rollback starts an incompatible binary.** [release.md](project/release.md#L1) restarts the old binary before restoring `name`. It fails until the down migration completes. Running the down migration first would instead break any remaining [new readers](project/new_reader.py#L1).

An isolated, in-memory SQLite check reproduced both missing-column failures. Neither schema supports both readers.

Use an expand/contract migration: retain both columns, backfill and synchronize values, and defer removing `name` until the rollback window closes. Then rehearse mixed-version rollout and rollback in staging; [release.md](project/release.md#L1) confirms staging has not run this release.

No deployment was run or project files changed.
