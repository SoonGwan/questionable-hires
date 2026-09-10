I’ll inspect the worker and retry path, then run a deterministic local experiment to test whether duplicate emails require concurrent workers. I’ll leave production code unchanged.

The worker sends the email before acknowledging the job, and only records completion after acknowledgement succeeds. I’ll make acknowledgement fail once after a simulated delivery, then retry on the same worker sequentially. I’ll also check whether separate worker instances share a lock or completion state.

Reproduced duplicate deliveries with **one worker and strictly sequential calls**. Simultaneous workers are not required.

The deterministic experiment showed:

1. Email delivery succeeds.
2. Acknowledgement raises.
3. The call exits, releasing the lock without recording completion.
4. A retry sends the email again, then acknowledges and records completion.

The lock serializes calls using **the same worker instance**. It does not make delivery and acknowledgement atomic, undo a delivered email, or guarantee exactly-once delivery. Separate worker instances also have separate locks and completion sets.

Added [experiment_worker_retry.py](project/experiment_worker_retry.py). All three tests passed, including successful-completion deduplication and separate-instance behavior. Run with `PYTHONDONTWRITEBYTECODE=1 python3 experiment_worker_retry.py`.

Production code is unchanged. This establishes a sufficient failure mechanism; without production logs or a provider idempotency contract, it does not prove which mechanism caused the customer incidents.
