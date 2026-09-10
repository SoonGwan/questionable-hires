I’ll use the exorcist skill to trace the retry path and run a deterministic local experiment that distinguishes overlapping workers from a repeated email send after failure. I’ll leave production code unchanged.

The worker records completion only after acknowledgement succeeds. If sending succeeds but acknowledgement raises, a retry can send again—even on the same worker, with no overlap. I’ll compare that failure path with a successful acknowledgement using local callbacks and two sequential calls.

The local experiment reproduced duplicate sends without overlapping workers. Production code is unchanged.

Run [diagnose_retry.py](project/diagnose_retry.py) with `python3 -B diagnose_retry.py`:

| Same job, two sequential calls | Deliveries |
|---|---:|
| Acknowledgement succeeds | 1 |
| First acknowledgement raises; then retry | 2 |

The causal chain is: `send` succeeds → `acknowledge` raises → completion is never recorded → the lock releases → retry sends again.

The lock serializes calls sharing **one Worker instance**. It does not make sending and acknowledgement atomic or guarantee exactly-once delivery. Separate Worker instances also have independent locks and completion sets; the experiment verified both locks can be held simultaneously.

Thus concurrency is unnecessary to explain the symptom. This establishes a deterministic failure path, not the cause of particular customer incidents: production logs and a provider idempotency contract are unavailable.

The smallest reliable corrective direction is idempotent sending keyed by a stable job ID, with durable deduplication at the delivery boundary. Moving the completion marker alone leaves failure windows and does not survive worker replacement.
