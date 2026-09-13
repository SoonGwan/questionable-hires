I’ll inspect the release files, run the supplied reader queries through the schema transitions, and test rollback with representative new-schema data. I’ll keep all work inside the project and preserve the release files.

The release renames a column that the old reader still uses. The rollout and rollback sequences both place the old binary against that renamed schema. I’ll verify those failures directly and check whether inserts and updates made after the migration survive rollback.

The queries confirm both compatibility failures: the old reader fails after `up`, and the new reader fails after `down`. Rollback preserved the inserted row and both updates under the restored `name` column. That establishes data survival for these probes; application-writer behavior and staging readiness remain unverified.

**Blocked for the documented rollout and rollback.**

- Migration-first rollout breaks the old reader: `no such column: name`.
- Old-binary-first rollback produces the same failure until down runs. Running down first would break any remaining new readers.
- Staging has not run, and no application-writer evidence was supplied.

Executed both supplied reader queries against initial, up, and down states. A new-schema insert and updates to existing/new rows all survived rollback under `name`; assertions passed.

[Full review](project/readiness_review.md) · [Results](project/readiness_results.json) · [Reproducible check](project/readiness_check.py)

Release files remain unchanged. No deployment or publishing occurred.
