I’ll use the exorcist skill to separate the retry theory from what the local artifacts establish, then identify the next useful check. I’ll keep the investigation read-only and inside this project.


The artifacts establish only that two users reported receiving two emails and the provider SDK exposes an optional `idempotency_key` argument. They do **not** establish retries, duplicate jobs, or whether idempotency was enabled and effective. No worker code or request traces are available to test those explanations.

Provider support alone doesn’t prevent duplicates: repeated sends must use the same key within the provider’s applicable scope and retention window. Whether that happened is unknown.

The next useful check is a correlated trace for **one reported duplicate pair**: confirmation/event ID, job ID, attempt number, outbound idempotency key, and provider request/message IDs.

- Same job, multiple attempts, missing or different keys would support retries bypassing deduplication.
- Different jobs for the same confirmation would point toward duplicate job creation.
- Repeated requests with the same key would make the provider’s actual idempotency rules and responses the next check.

Retries remain plausible, not confirmed. No corrective change is justified yet. No files were changed or external services accessed.
