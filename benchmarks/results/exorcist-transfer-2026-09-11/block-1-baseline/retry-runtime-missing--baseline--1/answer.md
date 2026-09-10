I’ll inspect the project’s email flow and retry evidence, then separate what the artifacts establish from what still needs checking.

The artifact establishes only that two users **reported receiving two emails** and the provider SDK exposes an optional `idempotency_key` argument. ([incident.md](project/incident.md#L1))

Retries are a hypothesis, not an established cause. An optional SDK argument does not prove the deployed worker supplies it, reuses the same key across retries, or receives effective deduplication.

The next useful check is to trace **one affected confirmation event**: correlate its job IDs, send attempts, actual idempotency keys, and provider responses/message IDs. That would help distinguish duplicate jobs from retries of one job and show whether repeated requests shared a key. Provider deduplication semantics would still need verification.

Those artifacts are absent, so the root cause cannot be established here. No external services were accessed or files changed.
