I’ll inspect the project artifacts to distinguish what they establish from the retry theory, then identify the next useful check.

The only supplied artifact, [incident.md](project/incident.md), establishes that two users **reported** receiving two emails and that the provider SDK exposes an optional `idempotency_key` argument.

It does **not** establish that retries caused the duplicates, that the worker supplies a key, or that the same key is reused across attempts. An optional SDK argument alone does not establish the provider’s deduplication behavior.

The next useful check is to trace one affected confirmation through its job and outbound send attempts: compare the logical confirmation ID, job IDs, attempt timestamps, actual idempotency keys, and provider message IDs. That would help distinguish a retried job from separately enqueued jobs and show whether duplicate requests used the same key. Provider key scope and retention would still need verification if identical keys produced separate sends.

No files changed or external services accessed.
