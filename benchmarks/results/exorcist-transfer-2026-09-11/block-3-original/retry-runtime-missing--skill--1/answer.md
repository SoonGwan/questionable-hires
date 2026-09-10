I’ll use the exorcist skill to separate the retry theory from what the local artifacts establish, then identify the next check. I’ll stay inside this project and leave files unchanged.


The artifacts do **not establish retries as the cause**.

[incident.md](project/incident.md#L1) records two users reporting two emails and says the SDK exposes an optional `idempotency_key` argument. That does not establish that the deployed worker supplies a key, reuses it on retries, or that the provider deduplicated these requests. No implementation, job IDs, request traces, deployed configuration, or key settings are available. Frequency and a known-good comparison are also unknown.

Retries, two independently created jobs, and duplication after a single send remain plausible; the evidence cannot rank them.

The next useful check is to correlate **one reported duplicate pair** with its confirmation event, job IDs, send attempts, actual idempotency keys, and provider message IDs:

- Same job, multiple attempts, missing or different keys: supports a retry-related explanation.
- Different jobs for the same confirmation: supports duplicate job creation.
- Multiple attempts with the same key: requires checking the provider’s deduplication scope, retention window, and responses.
- One send attempt: shifts investigation toward provider or downstream delivery duplication.

No corrective change is justified yet. The missing correlation evidence is the stopping point for this local diagnosis. No files were changed or external services accessed.
