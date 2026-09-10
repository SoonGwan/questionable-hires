I’ll inspect the project’s artifacts to separate what the evidence establishes from what still needs checking.

The artifacts establish only that two users reported receiving two emails and the provider SDK exposes an optional `idempotency_key` argument.

Retries are a hypothesis, not an established cause. SDK support does not show whether the deployed worker supplies a key, reuses it across attempts, or falls within the provider’s deduplication rules. The worker implementation, job IDs, request traces, deployed configuration, and key settings are all missing.

The next useful check is to trace one affected confirmation: correlate its event and job IDs with each outbound send attempt, actual idempotency key, and provider message ID. That would help distinguish a retried job from separately enqueued jobs and show whether repeated requests used the same key.

No files were changed or external services accessed.
