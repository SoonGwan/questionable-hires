I’ll inspect the release files, run the supplied reader queries across the initial, upgraded, and rolled-back schemas, and test what happens to new-schema data during rollback. I’ll keep all work inside the project and leave release files unchanged.

The queries confirm blockers in both sequences: migrating first breaks old readers during rollout, and restarting the old binary before rollback leaves it querying a missing column. The test update and insert both survive the down migration. Application-writer compatibility remains unverified, and the release notes say staging has not run.

**Block the documented rollout and rollback.**

- **Rollout:** migration removes `name`, so old instances fail during replacement.
- **Rollback:** restarting the old binary before down migration fails for the same reason. After down, remaining new readers fail.
- **Validation:** staging has not run; application writers were not supplied and remain unverified.

Executed both supplied reader queries against initial, up, up-after-writes, and down schemas. A committed update and new row both survived rollback, readable through `name`.

Saved the findings, reproducible verifier, and results in `readiness_review/`.

Release files remain unchanged. No deployment was run.
