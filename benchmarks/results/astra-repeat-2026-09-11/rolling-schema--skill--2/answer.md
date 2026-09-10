I’ll use the friday skill to inspect the release plan, compatibility, and recovery paths using only this project. I won’t run a deployment or modify files.


The migration renames a column that old instances still query, so it appears to break both the migration-first rollout and the old-binary-first rollback. I’ll check the compatibility combinations in an in-memory database.


**Blocked: the documented rollout and rollback both break database compatibility.**

- **Rollout:** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before old instances are replaced. [old_reader.py](project/old_reader.py#L1) still selects `name`, so those instances fail immediately. Use an expand/migrate/contract sequence: retain `name`, add and backfill `display_name`, maintain compatible writes, and defer removing `name` until the rollback window closes.
- **Rollback:** [release.md](project/release.md#L1) restarts the old binary before running the down migration. That binary cannot query the upgraded schema. Running the down migration first would instead break any remaining new instances. Preserve a schema compatible with both versions, or document a coordinated shutdown and migration sequence.
- **Readiness remains unverified:** [release.md](project/release.md#L1) explicitly says staging has not run this release. No readiness checks or concrete rollback trigger are provided. Validate the corrected rollout and rollback in staging and define observable success criteria and a rollback threshold before release.

An in-memory SQLite check reproduced both missing-column failures. The down migration preserved sample data, but reversing the schema alone does not make the application transition safe. Actual runtime/database compatibility remains unknown.

No deployment, persistent migration, or file changes were performed.
