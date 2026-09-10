I’ll use the exorcist skill to trace the retry path and design a deterministic local experiment that tests whether duplicate emails require overlapping workers. I’ll leave production code unchanged.

The worker sends the email before acknowledging the job and marking it complete. If acknowledgement raises, a retry can send again even when calls run sequentially. I’ll compare a successful acknowledgement with a forced failure followed by a retry on the same worker, checking that its lock is held during both sends.

Reproduced duplicate sends deterministically with **one worker and no overlapping calls**.

Added [diagnose_retry.py](project/diagnose_retry.py). Run with `PYTHONDONTWRITEBYTECODE=1 python3 diagnose_retry.py`. All assertions passed:

| Experiment | Sends |
|---|---:|
| Successful acknowledgement | 1 |
| First acknowledgement raises, then sequential retry | 2 |
| Replay after completion | No additional sends |

The causal chain is: `send` succeeds → `acknowledge` raises → `completed.add(job)` is skipped → the lock releases → retry sends again.

The lock was held during both sends. It serializes calls sharing that worker instance; it does **not** make delivery and acknowledgement atomic or prevent sequential duplicate delivery. Separate worker instances also have separate locks.

Simultaneous workers are therefore unnecessary to explain this reproduction. Production logs are unavailable, so this does not establish the cause of every customer report.

The smallest corrective direction is idempotent delivery keyed by a stable job identifier, with a verified provider or delivery-system contract. Moving the completion marker alone leaves crash/restart gaps. Production code remains unchanged.
