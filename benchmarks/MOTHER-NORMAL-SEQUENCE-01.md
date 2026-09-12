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

## Observed run at `7acbc2a`

All 263 repository tests passed. The new regression distinguishes a dropped
first standalone result from a correct guard, and the clear normal/late-response
checks pass on the correct implementation.

| Task | Arm | Total tokens | Process seconds | Evidence |
| --- | --- | ---: | ---: | --- |
| address-clear-boundary | baseline | unavailable | 240.016 | Session timeout; no completed reproduction |
| address-clear-boundary | skill | 65,810 | 24.864 | Captured normal and normal-clear passes; both stale overwrites reproduced |
| guarded-profile-search | baseline | 80,275 | 50.702 | Captured successful overlapping checks |
| guarded-profile-search | skill | 65,641 | 39.471 | Session completed, but helper command output is empty in captured events; final prose alone does not establish the verdict |

The complete guarded pair has lower recorded resources for skill, but missing
skill execution output prevents a quality-equivalent performance claim. The
clear pair lacks baseline usage. Neither pair establishes the requested 20%
overall saving. No aggregate chart update or retry was made. Raw local runs are
retained under ignored `local-runs/mother-normal-sequence-14`.
