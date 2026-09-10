I’ll use the exorcist skill to trace the retry path and run a deterministic local experiment that distinguishes overlapping workers from a repeated email send across sequential attempts. I’ll leave production code unchanged.

The worker sends the email before acknowledging the job, and only records completion after acknowledgement succeeds. I’ll compare a successful acknowledgement with one that fails once, using sequential calls on the same worker. If that produces two sends, simultaneous workers aren’t necessary to explain the symptom.

The deterministic experiment reproduced two emails with **one worker and sequential calls**. Simultaneous workers are not required.

Run: `python3 diagnostics/retry_experiment.py`

- Successful acknowledgement: **1 delivery**.
- Acknowledgement fails once, then retries: **2 deliveries**.
- Replay after completion: no additional delivery.

In [worker.py](project/worker.py#L12), sending succeeds before acknowledgement raises. Completion is never recorded, the lock releases on exception, and the retry sends again.

The lock serializes calls sharing that worker instance. It does **not** make delivery and acknowledgement atomic, guarantee exactly-once delivery, or coordinate separate worker instances. The completion set is also instance-local and in memory.

The smallest corrective direction is idempotent delivery using a stable job identifier, backed by a durable delivery mechanism or provider guarantee. Moving the completion marker alone leaves crash-related failure windows.

This confirms a local failure mechanism, not the actual production incidents: production logs and the provider’s idempotency contract are unavailable. Production code is unchanged; the experiment is saved in [diagnostics/retry_experiment.py](project/diagnostics/retry_experiment.py).
