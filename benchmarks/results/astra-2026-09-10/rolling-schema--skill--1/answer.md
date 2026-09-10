I’ll use the friday skill to inspect the release plan, compatibility changes, and recovery path within this project. I won’t run a deployment.

The migration renames a column that old instances still query, so they would fail during the documented rolling rollout. The rollback order has the same problem: it starts the old binary before restoring the column name. I’ll check both paths with a disposable in-memory database.

**Blocked: the documented rollout and rollback both break database reads.**

- **Rollout:** [release.md](project/release.md#L1) runs the migration before replacing instances. [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name`, immediately breaking [old_reader.py](project/old_reader.py#L1). Old and new instances cannot share either schema successfully. Use an expand/migrate/contract transition that preserves both columns and keeps values synchronized during coexistence, then backfills and removes the old column only after the rollback window closes.
- **Rollback:** The plan starts the old binary before [002_down.sql](project/002_down.sql#L1) restores `name`, so old reads fail. Running the down migration first would instead break remaining new instances. Use a compatible schema transition, or explicitly adopt a coordinated maintenance outage with all readers stopped during the schema/binary switch.
- **Readiness evidence is missing:** [release.md](project/release.md#L1) states staging has not run this release and provides no readiness checks or rollback trigger. Verify the revised sequence in staging, including mixed-version reads and preservation of newly written data through rollback. Define observable checks and a concrete stop/rollback threshold before release.

Local in-memory SQLite checks reproduced both missing-column failures. The down migration preserved existing and newly inserted values in that check; it reverses the rename without demonstrated data loss. Actual runtime database compatibility remains **unknown**.

No deployment ran, and no files were changed.
