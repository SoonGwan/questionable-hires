# True normal sequence regression

The helper previously started both requests before completing either. Its
`normal` verdict only checked the final state. A guarded component that drops
its first standalone result could therefore pass every default check.

The revised helper completes and checks each request before starting the next
in the normal case. With `--boundary`, it also checks the normal boundary before
testing a late older completion. The entrypoint instructions remain unchanged.

## Frozen development screen

Run the existing `address-clear-boundary` and `guarded-profile-search` cases from
`mother-in-law-confirmation-cases.json`, once each per baseline and skill arm,
GPT-6 Astra medium, one job, seed 20260912, 240-second timeout. These cases are
already exposed development tasks; this is not a new held-out confirmation.
Retain every result, including resource increases and incomplete execution.
Review actual commands and output against the original criteria before reporting
resources. Require correct stale/clear reproduction and no clean-case false
positive. No retries for a better score; the featured confirmation stays dated.
