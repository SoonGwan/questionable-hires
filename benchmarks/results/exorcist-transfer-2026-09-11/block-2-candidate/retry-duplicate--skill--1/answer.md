I’ll use the exorcist skill to trace the retry path and run a deterministic local experiment that tests whether duplicate emails require overlapping workers. I’ll leave production code unchanged.

The worker sends the email before acknowledging the job, and records completion only after acknowledgement succeeds. I’ll compare two sequential runs with the same job: one with successful acknowledgement, and one where the first acknowledgement raises. This will test whether retries alone can produce duplicates without concurrent workers.

Reproduced duplicate sends deterministically with **one worker, one thread, and sequential calls**. Production code is unchanged.

Run the local experiment with `python3 -B diagnose_retry.py` ([script](project/diagnose_retry.py)).

- **Control:** acknowledgement succeeds; the second call skips delivery. One email.
- **Injected failure:** sending succeeds, acknowledgement raises, and `completed` remains empty. The retry sends again. Two emails.

The lock serializes calls sharing the **same Worker instance** and releases when acknowledgement raises. It does not roll back the email, make sending and acknowledgement atomic, or prevent sequential retries. Separate Worker instances also have separate locks.

Thus, simultaneous workers are **unnecessary to explain this reproduction**. Production concurrency remains unverified; no production logs are available.

The smallest corrective direction is idempotent delivery keyed by a stable job ID, enforced durably at the delivery boundary. Merely moving the completion marker introduces crash/restart gaps. The provider’s idempotency contract would need verification before choosing a fix.
