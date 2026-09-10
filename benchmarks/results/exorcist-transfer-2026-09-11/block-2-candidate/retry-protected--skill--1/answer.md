I’ll use the exorcist skill to trace the retry path, test competing explanations locally, and assess the safeguards without changing production code.


The worker passes the job identifier as an idempotency key, and the requirements say retries retain that identifier. I’ll simulate an acknowledgment failure after delivery, then retry with both the same worker and a new worker instance to test whether the provider suppresses a second delivery.


The report was **not reproduced under the project’s stated contract**. Retries repeat the send request, but the provider suppresses duplicate delivery.

Local experiments counted delivery writes, not just final stored entries:

| Scenario | Send calls | Deliveries |
|---|---:|---:|
| Successful job | 1 | 1 |
| Acknowledgment fails, same job retried | 2 | 1 |
| Same retry using a new worker instance | 2 | 1 |
| Control: retry identifier changed | 2 | 2 |

[worker.py](project/worker.py) sends before acknowledging, so acknowledgment failure does cause another send attempt. Its safeguard is passing the stable job identifier as `idempotency_key`. [provider.py](project/provider.py) records delivery only for previously unseen keys. This protects the demonstrated failure window, including worker replacement; it does not depend on worker-local state.

Changing the identifier bypasses that protection, but violates the retry invariant in [requirements.md](project/requirements.md). It is a control, not evidence of the reported cause.

No production fix is justified by these results. The decisive next evidence would be identifiers, idempotency keys, and provider delivery records for a reported duplicate pair. Production logs and provider traces are explicitly unavailable here, so the production report remains unverified.

All assertions passed. No files were changed.
