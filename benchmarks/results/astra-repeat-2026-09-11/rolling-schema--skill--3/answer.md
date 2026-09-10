I’ll use the friday skill to review the release’s rollout sequence, compatibility, and recovery paths using only this project. I won’t run a deployment or change files.

The migration renames a column that old instances still query, so the documented rollout has a compatibility gap. Rollback also restarts the old binary before restoring that column. I’ll check both readers against the pre-migration, migrated, and reverted schemas in an in-memory database.

**Blocked: the documented rollout and rollback both break active readers.**

- **Rollout:** [release.md](project/release.md#L1) runs the migration before replacing instances individually. [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name`, immediately breaking [old_reader.py](project/old_reader.py#L1). New readers also fail against the original schema. Use an expand/backfill/contract sequence that supports both versions, or explicitly adopt a coordinated maintenance cutover.
- **Rollback:** The plan restarts the old binary before [002_down.sql](project/002_down.sql#L1) restores `name`, so that binary fails. Reversing those steps alone would break any remaining new instances. Provide a coordinated stop/migrate/restart procedure or a schema compatible with both versions.
- **Readiness evidence is missing:** Staging has not run this release, and the plan specifies no readiness checks or concrete rollback trigger. Rehearse rollout and rollback on the intended database runtime, verify reader compatibility and data preservation, and define stop/rollback criteria before proceeding.

An in-memory SQLite check reproduced both missing-column failures. The down migration preserved sample rows inserted before and after the upgrade; it reverses the rename without demonstrated data loss, but does not solve application compatibility. The actual database runtime and recovery evidence remain unknown.

No deployment ran and no files changed.
