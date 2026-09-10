I’ll use the exorcist skill to trace the retry path and run a deterministic local experiment that distinguishes overlapping workers from repeated work after a failure. I’ll leave production code unchanged.

The worker sends the email before acknowledging the job, and only then records completion. I’ll compare a successful acknowledgement with an injected acknowledgement failure, using the same worker and sequential retries. That will test whether duplicates require any worker overlap.

Reproduced duplicate sends with **one worker and strictly sequential calls**. Simultaneous workers are unnecessary.

The deterministic experiment in [diagnose_retry.py](project/diagnose_retry.py) passed:

- Successful acknowledgement followed by replay: **1 send**.
- Send succeeds, acknowledgement raises, then retry: **2 sends**.

In [worker.py](project/worker.py#L12), acknowledgement failure skips `completed.add(job)`. The lock releases when the exception exits the block; the retry finds no completion record and sends again.

The lock serializes calls sharing that worker instance. It does **not** make delivery and acknowledgement atomic, prevent sequential retries, or coordinate separate instances/processes. Completion tracking is also only in memory.

The corrective direction is delivery deduplication using a stable job identifier and a verified idempotent delivery mechanism. Moving completion before acknowledgement would close this local failure window but would not protect against crashes or new worker instances.

Run with `PYTHONDONTWRITEBYTECODE=1 python3 diagnose_retry.py`. Production code is unchanged. This confirms a local causal mechanism; production incidence and provider guarantees remain unverified because neither logs nor an idempotency contract are available.
