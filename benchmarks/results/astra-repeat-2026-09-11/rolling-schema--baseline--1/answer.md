I’ll review the release changes, rollout configuration, and rollback procedures, then check for concrete readiness blockers without deploying anything.

**Not ready for rollout or rollback.**

- **Rollout blocker:** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before instances are replaced. Every old instance still queries `name`, so its reads fail immediately. The planned mixed-version rollout is incompatible with this migration.
- **Rollback blocker:** [release.md](project/release.md#L1) restarts the old binary before restoring `name`. Those instances fail until the down migration runs. Reversing the order would break any new instances still serving traffic.
- **Validation gap:** Staging has not exercised this release, including mixed-version operation and rollback.

Use an expand-and-contract migration that preserves both readers’ compatibility, with a defined data synchronization strategy, and rehearse rollout and rollback in staging before release.

Verified the query failures against the supplied migrations in an in-memory SQLite database. No deployment ran; no files changed.
