I’ll use the exorcist skill to trace the retry path, test competing explanations locally, and assess the safeguards without changing production code.

The worker sends before acknowledging, so an acknowledgment failure can cause another send attempt. It also reuses the job identifier as an idempotency key, which the local provider deduplicates. I’ll test whether retries produce duplicate deliveries, including when an error occurs after the provider accepts the send.

**The duplicate-email report was not reproduced under this project’s stated retry contract.** Retries repeat send attempts, but the local provider deduplicates deliveries.

Local experiments passed:

| Scenario | Send attempts | Modeled deliveries |
|---|---:|---:|
| Normal processing | 1 | 1 |
| Acknowledgment failure, then five retries using fresh workers | 6 | 1 |
| Provider accepts, then throws a timeout; worker retries | 2 | 1 |

The safeguard is explicit: [worker.py](project/worker.py) passes the stable job identifier as the idempotency key. [provider.py](project/provider.py) records only the first delivery for that key. Worker recreation does not bypass this protection.

Controls produced two modeled deliveries when the identifier changed or provider state was replaced. These establish protection boundaries, not evidence that either caused the reported incident.

[requirements.md](project/requirements.md) specifies stable retry identifiers and provides no production logs or provider traces. Thus, actual duplicate emails remain unverified. The next decisive evidence would be two deliveries for one logical job, with their idempotency keys and provider deduplication scope.

No production-code correction is supported by these findings. No files were changed.
