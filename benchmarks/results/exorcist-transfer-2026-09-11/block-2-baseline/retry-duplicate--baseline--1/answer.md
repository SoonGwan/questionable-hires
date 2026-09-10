I’ll inspect the worker and build a deterministic local experiment to identify how a retry can send a second email, without changing production code.

The worker records completion only after acknowledgement succeeds. If sending succeeds and acknowledgement raises, the retry can send again even when the two attempts run strictly one after the other. I’ll test that failure sequence, plus duplicate suppression after success and the scope of separate worker instances.

**Duplicate emails do not require simultaneous workers.** The deterministic local experiment reproduced two simulated deliveries using one worker and strictly sequential calls:

`send succeeds → acknowledgement raises → first call exits → retry sends again`

In [worker.py](project/worker.py#L12), completion is recorded only after acknowledgement succeeds. The exception leaves the job uncompleted and releases the lock.

The lock:
- Serializes calls using the **same Worker instance**.
- Does not make delivery and acknowledgement atomic or undo a successful delivery.
- Does not coordinate separate instances, which have independent locks and completion sets.

This proves a sufficient failure mechanism, not the cause of the actual customer incidents. Without production logs or a provider idempotency contract, simultaneous execution and actual delivery behavior remain unverified.

Added [test_worker_retry.py](project/test_worker_retry.py). All three tests passed, including successful-completion suppression and separate-instance behavior. Production code is unchanged.

Reproduce with:
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_worker_retry
```
