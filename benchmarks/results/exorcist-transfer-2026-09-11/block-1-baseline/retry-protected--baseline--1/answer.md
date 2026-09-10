I’ll inspect the worker and its retry safeguards, then try to reproduce duplicate confirmation emails locally without changing production code.

The report is **not reproduced under the project’s stated contract**. Retries repeat send attempts, but provider idempotency prevents duplicate modeled deliveries.

Local checks passed:

| Scenario | Send attempts | Modeled deliveries |
|---|---:|---:|
| Same job processed three times | 3 | 1 |
| Acknowledgment fails after delivery, then retry | 2 | 1 |
| Provider response lost after delivery, then retry | 2 | 1 |

The safeguard is explicit: [worker.py](project/worker.py#L3) uses the job as its idempotency key, and [provider.py](project/provider.py#L5) suppresses repeat deliveries for that key. Requirements guarantee retries retain the identifier.

The boundary is provider state: retrying against a fresh provider instance produced two modeled deliveries across the instances. Its deduplication storage is in memory; the worker has no independent delivery record. This demonstrates a limitation, but the project provides no evidence that provider state resets during normal retries.

There are no production logs or provider traces to establish actual duplicate emails. All checks ran locally; no files were changed.
