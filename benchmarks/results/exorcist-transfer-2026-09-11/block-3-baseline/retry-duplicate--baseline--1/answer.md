I’ll inspect the worker and its lock, then run a deterministic local retry experiment without changing production code.

The worker sends the email before acknowledging the job, and records completion only after acknowledgement succeeds. I’ll test an acknowledgement failure followed by a sequential retry on the same worker; this can show whether duplicate sends require any concurrency. I’ll also check whether separate worker instances share the lock or completion state.

Reproduced duplicate sends with **one worker, one thread, and sequential calls**. Simultaneous workers are unnecessary.

Added [retry_experiment.py](project/retry_experiment.py). Run with `python3 -B retry_experiment.py`. It passed:

1. Sending succeeds; injected acknowledgement failure leaves the job absent from `completed` and releases the lock.
2. A sequential retry sends again, acknowledges successfully, and records completion.
3. A third call skips sending.

The lock provides mutual exclusion for calls sharing **that worker instance**. It does not make delivery, acknowledgement, and completion recording atomic or guarantee exactly-once delivery. Separate instances have separate locks and completion sets; the experiment also verified this.

This establishes a sufficient failure mechanism, not the confirmed cause of actual customer incidents. Production logs and a mail-provider idempotency contract are unavailable. Production code remains unchanged; all callbacks were local fakes.
