I’ll review the release configuration, rollout checks, and rollback procedures in this project, then report any concrete blockers. I won’t run a deployment.

**Not ready for rollout or rollback.** Three concrete blockers:

- **Rollout breaks running instances.** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before instances are replaced, but [old_reader.py](project/old_reader.py#L1) still queries `name`. Old instances fail throughout the mixed-version rollout.
- **Rollback starts an incompatible binary.** [release.md](project/release.md#L1) restarts the old binary before restoring `name`, so its queries fail. Simply reversing the order also breaks any remaining new instances, which require `display_name`.
- **Staging validation is missing.** [release.md](project/release.md#L1) explicitly states this release has not run in staging.

Use an expand/contract migration that keeps both versions compatible, with backfill and write synchronization if applicable. Rehearse mixed-version rollout and rollback in staging before removing the old column.

Verified using an isolated, in-memory SQLite database: the old query fails after migration up; the new query fails after migration down. No deployment ran and no project files changed.
