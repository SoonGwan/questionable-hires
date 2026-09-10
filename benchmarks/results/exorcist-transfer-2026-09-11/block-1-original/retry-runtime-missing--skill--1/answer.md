I’ll use the exorcist skill to separate what the artifacts show from the retry hypothesis, then identify the next check that would distinguish the likely causes. I’ll stay inside this project and leave files unchanged.


The artifacts establish that two users **reported** receiving two emails and that the provider SDK exposes an optional `idempotency_key` argument. They do not establish that retries occurred, that the application supplies that argument, or that the provider deduplicated requests. Frequency, timing, and a known-good comparison are unavailable.

Retries are plausible, but duplicate job creation or multiple send paths also fit the evidence. There is no basis to rank these causes or confirm a root cause.

The next useful check is to trace **one reported duplicate pair**: correlate its confirmation event, job IDs, attempt numbers, outbound requests, actual idempotency keys, and provider message IDs.

- Same job with multiple send attempts supports the retry hypothesis.
- Different jobs for the same event supports duplicate enqueueing.
- Missing or different keys across attempts would explain why SDK support alone provides no protection.
- Matching keys with distinct provider messages would warrant checking the deployed provider’s key scope and expiry semantics.

Those traces and settings are absent, so no corrective change is justified yet. No external services were accessed or files changed.
