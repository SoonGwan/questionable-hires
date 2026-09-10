I’ll inspect the release artifacts, rollout and rollback procedures, and relevant checks in this project. I won’t run a deployment.

The migration renames a column that the old binary still reads. That appears to break both the rolling rollout and the documented rollback order. I’ll check both readers against each schema and verify that the reverse migration preserves the data.

**Not ready for rollout or rollback.**

- **Rollout blocker:** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before replacing instances. Every remaining [old reader](project/old_reader.py#L1) then fails with `no such column: name`.
- **Rollback blocker:** [release.md](project/release.md#L1) restarts the old binary before reversing the migration, producing the same failure. Reversing the order would break any remaining new instances instead.
- **Validation gap:** [release.md](project/release.md#L1) explicitly says staging has not run this release.

Verified both readers against the initial, migrated, and reverted schemas using an in-memory SQLite database. The reverse migration preserves seeded data, but neither schema supports both binaries.

Before release, use an additive migration with a defined data synchronization strategy and retain both columns through the rollback window, or document a coordinated downtime procedure. Rehearse rollout and rollback in staging.

No deployment run; no files changed.
