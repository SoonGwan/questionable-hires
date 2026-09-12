# Large selected hunk: preserve evidence without increasing the text allowance

The previous focused-hunk collector still lost the relevant line when one
contiguous hunk exceeded 12,000 characters. This is the documented remaining
failure from [focused patches](NECROMANCER-FOCUSED-PATCH-01.md), not a new model
benchmark selected for a favorable score.

The collector now supplies numbered selected patch rows when a validated
single-file unified patch exceeds the allowance. It prioritizes all attributed
new-side lines, then up to three adjacent patch rows. Omission markers and an
explicit limitation distinguish this from a complete or applyable patch. Old/new
coordinates do not assert which removed line corresponds to an added line.
The ordinary evidence prefix shrinks to 4,000 characters; the excerpt is at most
8,000 characters. Truncation remains true. Ambiguous, malformed, combined,
missing-target or over-budget-target cases retain the previous capped fallback.
Small patches, shallow cutoffs and entrypoint/UI routing are unchanged.

## Actual Git regression and before/after check

A temporary complete Git repository commits 160 long comments followed by a
value. The next commit changes all comments and that value in one contiguous
hunk, without artificial unchanged separators. The test verifies that the
selected addition lies beyond character 12,000 in the original Git output.
Both collectors run against the same repository and line 161, with no model:

| Observation | Previous collector (`60f7bfb`) | Revised collector |
| --- | ---: | ---: |
| Evidence prefix characters | 12,000 | 4,000 |
| Selected excerpt characters | 0 | 435 |
| Selected historical addition present | No | Yes |
| Truncation disclosed | Yes | Yes |

This reduces returned patch text from 12,000 to 4,435 characters while recovering
the selected addition in this fixture. It does not recover the distant removed
value: establishing the exact prior behavior can still require focused parent
inspection. Counts exclude JSON fields, current lines and attribution; these are
not total response-token, model-token or wall-time improvements. Git output is
still captured in full internally, and the number of Git processes is unchanged.

New tests cover this real single-hunk history, old/new numbering with deletion,
context and missing-final-newline markers, multiple selected lines, invalid
counts, combined/duplicate patches, missing targets and an insufficient budget.
All 137 repository tests pass (13.747 seconds), including the existing no-write,
rename, shallow-boundary, genuine-root and four-Git-process checks. Repository and
skill validators pass. These verify helper behavior, not broad model performance.

The next model check must evaluate whether the selected evidence actually removes
follow-up work at equivalent decision quality, retaining cases where the helper
is unnecessary or insufficient. Do not credit author-side character savings as
completion of the eight-skill objective; that objective remains unverified.
