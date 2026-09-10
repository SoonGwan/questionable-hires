I’ll use the exorcist skill to separate what the artifacts demonstrate from the retry hypothesis, then identify the next check. I’ll keep everything local and read-only.

The artifacts establish only that two users reported receiving two emails and that the provider SDK exposes an optional `idempotency_key` argument. **Retries are plausible, but unconfirmed.**

SDK support alone does not establish protection: we do not know whether the deployed worker supplies a key or reuses it across attempts. Even with provider deduplication, separate attempts with different keys could be treated as distinct sends. No implementation or traces are available to test this locally.

The next useful check is to correlate **one reported duplicate pair** with its logical confirmation event, job IDs, attempt numbers, outbound requests, idempotency keys, and provider message IDs:

- Same job, multiple attempts: supports the retry explanation; inspect whether keys were absent, changed, or reused.
- Different jobs for the same confirmation: supports duplicate enqueueing; retry-level protection may not cover separate jobs.
- One outbound request: shifts investigation toward provider or delivery behavior.

If repeated sends used the same key, the next evidence needed is the provider’s actual deduplication contract and request results. No corrective change is justified yet. No files were changed or external services accessed.
