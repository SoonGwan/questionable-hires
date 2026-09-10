I’ll use the exorcist skill to trace the retry path and run a deterministic local experiment that distinguishes worker overlap from a retry repeating an already completed send. I’ll leave production code unchanged.

The worker sends the email before acknowledging the job, then records completion only after acknowledgement succeeds. I’ll compare two sequential attempts with successful acknowledgement against the same attempts with the first acknowledgement forced to fail. Both cases will use one worker and one thread, so overlap cannot explain any duplicate.

Reproduced duplicate sends with **one worker, one thread, and strictly sequential attempts**. Worker overlap is unnecessary.

Run the local experiment with `python3 diagnose_retry.py` ([script](project/diagnose_retry.py)). All assertions passed:

| First acknowledgement | Sends after two attempts |
|---|---:|
| Succeeds | 1 |
| Raises | 2 |

In [worker.py](project/worker.py#L12), sending succeeds before acknowledgement raises. The exception skips `completed.add(job)` and releases the lock. The retry finds no completion record and sends again.

The lock provides mutual exclusion for calls sharing that worker instance. It does **not** make sending and acknowledgement atomic or prevent sequential retries from repeating an external effect. Separate worker instances also have separate locks.

The smallest local correction is to record successful sending before acknowledgement; acknowledgement retries must still run for completed jobs. That in-memory correction would not cover crashes or new instances—those require durable deduplication or provider-supported idempotency.

This confirms a local failure mechanism, not the cause of every customer report: production logs and a provider idempotency contract are unavailable. Production code is unchanged.
