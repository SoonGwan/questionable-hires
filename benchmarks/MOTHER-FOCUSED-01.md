# Focused interaction QA follow-up

Candidate `8312d1f` explicitly bounds discovery to the permitted project and
prefers existing facilities or a small shared reproduction over an additional
interaction framework. Controlled waits must terminate and operations must be
cleaned up. The character and discriminating failure/control sequences remain.

Two unchanged development cases, one skill execution each, serial Astra medium,
under ignored `local-runs/mother-focused-01`; no fresh baseline, retry or exclusion.

| Case | Tokens, input including cache + output | Seconds | Previous screen tokens / seconds |
| --- | ---: | ---: | --- |
| search-order | 68,614 | 54.992 | 87,163 / 73.232 |
| search-protected | 86,956 | 70.972 | 66,993 / 39.649 |

Combined: 155,570 tokens / 125.964 seconds versus 154,156 / 112.881 previously.
The favorable defect-case result must not hide the adverse protected-case result.
There is no aggregate efficiency win or repeated-run reliability claim.

Both command traces stay within the project. Original fixture files are
unchanged. Both generated tests use one parameterized completion-order method
with controlled responses and bounded behavior-dependent waits, not a separate
interaction driver. Independent post-run replay confirms the defect suite's
single stale-result assertion failure and the protected suite's two passes.
Neither claims browser-rendering verification.

These results support scoped discovery and correct distinction in these two
samples, not a causal claim that instruction wording guarantees either. The
scope correction is retained, but cost improvement remains unproven. Do not
repeat these unchanged cases to seek a favorable time sample.
