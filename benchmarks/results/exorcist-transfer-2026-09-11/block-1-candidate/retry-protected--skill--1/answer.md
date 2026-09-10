I’ll use the exorcist skill to trace the retry path, test the reported duplication locally, and assess which safeguards cover it. I’ll keep the investigation inside this project and leave production code unchanged.


The worker passes the stable job identifier as the provider’s idempotency key, and the local provider suppresses repeated keys. I’ll test the critical failure window—delivery succeeds, then acknowledgment fails—to see whether retrying produces a second delivery despite that safeguard.


The report was **not reproduced under the project’s stated contract**.

I injected an acknowledgment failure after a successful send, then retried the same job using a fresh worker:

| Scenario | Send calls | Deliveries |
|---|---:|---:|
| Normal processing | 1 | 1 |
| Retry after acknowledgment failure | 2 | 1 |
| Control: same body, different keys | 2 | 2 |

The safeguard addresses this failure window: [worker.py](project/worker.py#L3) uses the job identifier as the idempotency key, and [provider.py](project/provider.py#L5) suppresses repeat deliveries for that key. Retries repeat the send call, but do not duplicate delivery. The control confirms that distinct keys allow duplicates.

[requirements.md](project/requirements.md#L1) guarantees stable identifiers across retries. There are no production logs or provider traces, so actual incident frequency and cause remain unverified. The local model also cannot establish production idempotency retention or concurrency behavior.

No code correction is justified by these results. The next decisive evidence would be the reported duplicate’s job identifiers, outbound idempotency keys, and provider delivery records.

No files were modified; all experiments ran locally.
