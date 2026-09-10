I’ll use the friday skill to inspect the release plan, compatibility changes, and rollback evidence within this project. I won’t run a deployment.

The migration renames a column that old instances still query, so the documented rollout appears to break them immediately. The rollback also restarts the old binary before restoring that column. I’ll check both query/schema combinations locally; staging validation is explicitly missing.

**Blocked: the documented rollout and rollback both break database reads.**

- **Rollout:** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before old instances stop. [old_reader.py](project/old_reader.py#L1) still selects `name`, so those instances fail throughout coexistence. Keep both columns through an expand/migrate/contract transition, with synchronized writes and a backfill, before removing `name`.
- **Rollback:** [release.md](project/release.md#L1) restarts the old binary before running the down migration. Its queries fail until the column is restored; afterward, any remaining new instances fail. Retain a schema compatible with both versions for the rollback window, or document a coordinated shutdown and schema/application switch if downtime is acceptable.
- **Readiness evidence is missing:** The release explicitly has not run in staging, and provides no health gates or concrete rollback trigger. Validate mixed-version reads and writes plus rollback on the intended database, and define observable stop/rollback criteria before release.

An in-memory SQLite check confirmed both missing-column failures. The down migration preserved sample data, including a row inserted after migration; it reverses the rename without dropping data. Actual database/version behavior and runtime configuration remain **unknown**.

No deployment ran, and no project files changed.
