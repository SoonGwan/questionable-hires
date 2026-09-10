I’ll use the exorcist skill to separate the evidence from the retry theory and identify the next check, using only local artifacts and without changing files.


The artifacts do **not establish a cause**.

- **Observed:** Two users reported receiving two emails. The provider SDK exposes an optional `idempotency_key` argument. [incident.md](project/incident.md#L1)
- **Unproven:** Whether retries occurred, whether a key was supplied or reused, and whether the provider deduplicated requests. An optional SDK argument establishes neither deployed usage nor deduplication guarantees.
- **Competing explanations:** A retry submitted the same confirmation twice; separate jobs or triggers each submitted it; or duplication occurred downstream. None is ruled out. Frequency beyond the two reports and a known-good comparison are unavailable.

The next useful check is to trace **one affected confirmation** from its originating event through job IDs and attempts to outbound requests, actual idempotency keys, and provider message IDs. Repeated attempts of one job would support the retry theory; distinct jobs would point toward duplicate enqueueing; one submission with two deliveries would shift attention downstream.

No corrective change is justified yet. If repeated submissions with missing or changing keys are confirmed, a stable key per logical confirmation would be a candidate fix, subject to the provider’s actual contract. The decisive evidence is absent locally; no external services were accessed or files changed.
