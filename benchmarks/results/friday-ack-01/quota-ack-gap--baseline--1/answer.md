I’ll read the release procedure and supplied entrypoints, then test migration and rollback behavior on a disposable SQLite database inside the project, preserving the original files.

The local release contract fails in two observed ways:

- **Mixed-version visibility:** [002_up.sql](project/002_up.sql#L2) only backfills once. Acknowledged old updates leave new reads stale; acknowledged new updates leave old reads stale. An old insert of `60` returns `60` to old readers and `NULL` to new readers.
- **Rollback loses acknowledged updates:** [002_down.sql](project/002_down.sql#L4) drops `quota_limit` without reconciling values. After rollback, account 1 returned `40` instead of its latest acknowledged `50`; account 2 returned `60` instead of `80`.

Compatible behavior also passed: initial backfill, new inserts visible to both versions, retention of all inserted rows, and old updates/inserts after rollback. An untouched new insert retained its value through rollback.

Executed actual migration files and nine sequential mixed-version writes through `application.write`, checking both `application.read` versions on fresh connections after every acknowledgment. Production configuration and restore evidence remain **unverified**, not demonstrated defects.

[Full results](project/local_review/run-yg4vquep/results.json) · [Reproducible harness](project/local_review/exercise.py)

Original files were hash-verified unchanged. All work stayed inside the project; no installation, deployment, or external services.
