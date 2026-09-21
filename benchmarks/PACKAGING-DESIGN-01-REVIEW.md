# Packaging name-policy design01 — reviewed, no production promotion

2026-09-21. [Protocol](PACKAGING-DESIGN-01-PROTOCOL.md), launch `d9a9a6e`,
resource `a545a53`. [All three original attempts](results/packaging-design-01/run.json)
and [criterion/capture/integrity evidence](results/packaging-design-01/comparison.json).
One author-selected installed-distribution task, not an upstream checkout or
independent holdout. Fixed baseline/candidate/prior order,n=1,shared host/cache.

| Arm | Criteria | Total tokens, cached input included | Wall seconds | Responses / shell commands |
| --- | --- | ---: | ---: | --- |
| No-skill |5/5|76073|59.042|4 /3|
| Candidate |5/5|81947|61.405|4 /3|
| Prior |5/5|89313|66.403|4 /5|

Candidate versus prior:−8.25% tokens,−7.53% time. Versus baseline:+7.72% tokens,
+4.00% time. This is mixed comparative evidence, not a broad performance gain.

## Native evidence and recommendation

All three original sessions executed all eight requested filenames on unchanged
native packaging26.3 parsers, with asserted local imports. The normal wheel and
sdist cases normalize to `demo-pkg`, version1.0. Double underscores fail the wheel
parser with `InvalidWheelFilename` but are accepted by sdist. Unicode names are
accepted by both; leading-underscore wheel normalizes to `-demo`. Empty sdist name
raises `InvalidSdistFilename`. Successful wheels preserve build/tags.

Each answer correctly rejects the proposal as behavior-preserving deduplication:
strict canonicalization would accept double-underscore wheels but reject Unicode
and leading-underscore names, exposing `InvalidName` instead of format-specific
errors. These proposal effects are explicitly static inferences, not model-run
mutations. No upstream tests were supplied/run. No external-standard violation
is inferred merely from observed acceptance.

All retain format-specific checks with shared normalization as a viable design.
Baseline/candidate trace a future metadata underscore restriction; prior traces
a future wheel underscore relaxation. Candidate/prior additionally inspect pylock
and metadata consumers, showing broad exception wrapping and independent policy.
Baseline's two direct parser consumers suffice for the frozen task; do not change
the rubric after seeing this difference. All5 criteria pass per original evidence.

## Capture and integrity

All11 shell outputs match the original same-session records exactly. No unresolved
correspondence or source-truncation marker was found. The public export retains
redacted tool records, usage/exposure, answers, selected source with licenses and
the complete frozen case. Private initial session text is excluded.

All26 original files and modes match the frozen fixture, no extra files remain,
HEAD matches initial commit, staged entries match that tree, and installed skills
are unchanged. Pre-session binary index bytes were not captured; staged entries
were verified using the saved pre-collection index. Runtime before/after snapshots
in baseline/prior additionally cover file hashes/modes during native execution.
Resource usage agrees with original session accounting; no reruns or concurrent
author suites were used during measurement.

## Decision

Do not promote the candidate. It read the new entrypoint but neither read the
collector reference nor executed the collector. Both source and runtime fit direct
reads here, so lack of adoption is not itself a task failure. The favorable prior
comparison cannot be attributed to an unused helper; the no-skill comparison is
adverse. Keep the frozen candidate and all attempts, production Landlord unchanged.
Do not force a helper into simple reviews or rerun this exposed task for a win.

Further work must target decision-changing workflow costs, not a longer prompt or
an ever-growing tool bundle without observed use. Featured charts remain unchanged;
eight-skill whole-task improvement is still unproven.
