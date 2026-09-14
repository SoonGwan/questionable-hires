I’ll use the friday skill to review the rollout and rollback, then exercise the application entrypoints against a disposable local SQLite database. I’ll preserve the original files and separate observed failures from missing production evidence.


The migration copies existing quotas once, but neither writer synchronizes the two columns afterward. I’ll check how that affects acknowledged updates and inserts, then run the documented rollback to see which values survive.


**Blocked by evidence.** Local execution reproduced mixed-version visibility failures and rollback data loss.

Used the actual migrations and `application.write/read` on disposable project-local SQLite 3.51.0. Every write returned its success dictionary; both versions were read on fresh connections before the next write.

| Acknowledged operation after migration | Old reads | New reads | Result |
|---|---:|---:|---|
| Old update to 20 | 20 | 11 | Stale new read |
| New update to 30 | 12 | 30 | Stale old read |
| Old insert with 40 | 40 | `None` | Missing new quota |
| New insert with 50 | 50 | 50 | Compatible |

1. **Mixed-version writes violate the contract.** `002_up.sql` backfills once; subsequent updates change only the writer’s column, and old inserts leave `quota_limit` null. Initial backfill and new inserts are compatible. Require transactional synchronization covering both update directions and old inserts before allowing writes in the expanded schema.

2. **Documented rollback discards acknowledged new updates.** After draining new calls and executing `002_down.sql`, accounts whose latest acknowledged values were **30 and 45** read **12 and 40**. Latest old-written values **26 and 55** survived, as did all account rows. Old updates and inserts also worked afterward. Before dropping the column, preserve each account’s latest acknowledged value in `quota`; blindly copying either column is unsafe because alternating writers leave either column stale.

The first observed incompatibility was the first old update after expansion. The first destructive recovery step is `DROP COLUMN quota_limit`. Immediately after backfill, the tested data was safely reversible. After divergence, retain both columns and obtain reliable write-order evidence before reconciliation; the schema itself does not record which value is latest.

Production configuration and restore evidence remain **unknown**, as explicitly documented—not additional observed defects.

Original files were verified unchanged. Reproducible harness and full evidence: [check.py](project/review-local/check.py), [results.json](project/review-local/sqlite-djgdq3rm/results.json).
