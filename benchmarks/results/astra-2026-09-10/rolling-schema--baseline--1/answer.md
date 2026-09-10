I’ll inspect the release artifacts, rollout checks, and rollback procedures, then report concrete blockers without deploying anything.

The migration renames a column that the old application still queries, so the proposed mixed-version rollout appears incompatible. I’ll check both release sequences in an isolated, in-memory database.

**Blocked for rollout and rollback as documented.**

- **Rollout breaks existing instances.** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name`, but [old_reader.py](project/old_reader.py#L1) still selects `name`. Running the migration first immediately breaks old instances throughout the rolling replacement.
- **Rollback starts an incompatible binary.** [release.md](project/release.md#L1) restarts the old binary before restoring `name`, causing query failures. Reversing the order would instead break any remaining new instances, which require `display_name`.
- **Staging validation is missing.** [release.md](project/release.md#L1) explicitly says this release has not run in staging. Rehearse rollout overlap and rollback before proceeding.

Use an expand/contract migration that keeps both versions compatible during rollout and the rollback window, with synchronized values if writes occur. Alternatively, define a coordinated maintenance-window procedure.

Verified using the supplied SQL and queries in an isolated, in-memory SQLite database: old queries fail after the up migration; new queries fail after the down migration. No deployment ran and no project files changed.
