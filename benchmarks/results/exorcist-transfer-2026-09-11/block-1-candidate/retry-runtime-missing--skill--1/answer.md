I’ll use the exorcist skill to trace the email path and compare the retry explanation with the available evidence. I’ll stay inside the project and leave files unchanged.


The artifacts establish only that two users reported receiving two emails and that the provider SDK exposes an optional `idempotency_key` argument. [incident.md](project/incident.md#L1)

Retries are plausible, but unproven. Duplicate jobs or separate send paths also fit the reports. There are no implementation details, traces, job identifiers, or deployed settings to distinguish them—or establish frequency or a known-good comparison.

Provider idempotency support alone does not establish protection: retries would need to use the same key, and the provider would need to honor it under the applicable conditions. Neither is evidenced here.

The next useful check is a trace of **one reported duplicate pair**, correlating the confirmation event, job IDs, attempt numbers, outbound idempotency keys, and provider message IDs:

- Same job, multiple attempts: supports retries as the source of repeated requests.
- Different jobs for one event: supports duplicate enqueueing or separate send paths.
- Missing or changing keys: would explain why provider idempotency did not deduplicate repeated requests.
- Same key with distinct accepted messages: calls for checking the provider’s idempotency scope and conditions.

No root cause or corrective code change is justified yet. I accessed no external services and changed no files.
