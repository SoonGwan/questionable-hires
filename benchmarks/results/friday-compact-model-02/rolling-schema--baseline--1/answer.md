I’ll inspect the release and its verification tools, then run the supplied readers across the initial, upgraded, and rolled-back schemas. I’ll also test what happens to representative new-schema data during rollback, without changing release files or deploying.

The migration immediately renames the column used by the old reader, but the rollout keeps old instances running against that schema. The rollback order also restarts the old binary before restoring its column. I’ll verify both failures and check whether inserts and updates survive the reverse rename.

**Blocked for the documented rollout and rollback.**

- **Rollout:** renaming `name` immediately breaks old readers while old instances are still serving.
- **Rollback:** restarting the old binary before restoring `name` causes the same failure. Running down breaks any remaining new readers.
- **Missing verification:** staging has not run; application-writer behavior remains unverified.

Executed both supplied readers against initial/up/down schemas. A committed new-schema insert and update both survived rollback; the update retained its new value.

[Full review](project/review/readiness.md) · [Executed results](project/review/results.json) · [Verification script](project/review/verify_release.py)

Release files remained unchanged. No deployment was run.
