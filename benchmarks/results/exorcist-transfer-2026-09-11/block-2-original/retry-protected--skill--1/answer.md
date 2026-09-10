I’ll use the exorcist skill to trace the retry path, test the reported duplication locally, and assess the safeguards without changing production code. I’ll stay within this project and won’t delegate.



The worker sends before acknowledging, so an acknowledgement failure can cause another send attempt. However, it uses the job identifier as an idempotency key, and the local provider records only one delivery per key. The project specifies that retries retain the identifier. I’ll test failures after acceptance to see whether retries produce duplicate deliveries or just repeated calls.



The report was **not reproduced under this project’s stated contract**. Retries repeat send calls, but the provider suppresses duplicate deliveries.

| Local experiment | Send calls | Modeled deliveries |
|---|---:|---:|
| Normal processing | 1 | 1 |
| Same job replayed | 2 | 1 |
| Acknowledgement fails after sending | 2 | 1 |
| Response lost after provider acceptance | 2 | 1 |
| 100 retries with fresh workers | 101 | 1 |
| Two distinct jobs | 2 | 2 |

The safeguard is explicit: [worker.py](project/worker.py#L3) passes the job identifier as the idempotency key, and [provider.py](project/provider.py#L5) records a delivery only for an unseen key. [requirements.md](project/requirements.md#L1) guarantees that retries retain their identifier.

Sending before acknowledging creates a retry window, but that alone does **not** establish duplicate emails. The experiments exercised that window successfully.

These results cover the local model; there are no production logs or provider traces to validate the reported incident. The next decisive evidence would be the job identifiers, submitted idempotency keys, and provider delivery records for a reported duplicate pair.

No production-code correction is justified by the available evidence. No files were changed.
