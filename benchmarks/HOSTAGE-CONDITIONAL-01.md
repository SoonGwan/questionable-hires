# Hostage conditional instructions — separate, unmeasured candidate

2026-09-21. Parent `51dd30e`. Candidate:
`benchmarks/candidates/hostage-conditional/skills/hostage-negotiator`.
Production remains unchanged; this is not an accepted performance improvement.

## Hypothesis

The production entry includes asynchronous ownership, mutable snapshots,
framework callback hazards and runtime-asset selection for every invocation,
although its description also covers ordinary small synchronous changes.
Move those three paragraphs unchanged to one conditionally linked guide. Keep
general scope, state transitions, actual native evidence, missing-capture handling,
permission and stopping rules in the entry. Copy all existing resources and UI
metadata unchanged, including the Python cleanup correction.

This differs from the older [compact-entry experiment](HOSTAGE-COMPACT-01.md),
which did not establish an overall efficiency gain, and the [evidence consolidation](HOSTAGE-EVIDENCE-COMPACT-02.md),
which retained both runtime routes inline. Those adverse/limited results remain
relevant: shorter text does not imply better whole-task behavior.

Entrypoint whitespace-delimited words:711 →572 (139 fewer). The new conditional
guide contains181 words; loading both therefore costs753 words,42 more than the
prior entry, before any extra tool-call overhead. These are word counts, **not
tokens or savings**. The candidate may harm asynchronous tasks if guide discovery
adds a response or essential constraints go unread. That is an explicit rejection
risk, not a reason to omit asynchronous controls.

## Validation performed

Skill quick validation, repository relative-link validation and diff checks pass.
Both executable assets match the production files byte-for-byte; no runtime
rewrite or cross-skill dependency was introduced. This checks packaging/content,
not routing, actual instruction use, task quality or model cost.

## Frozen-candidate evaluation boundary

Before model execution, specify two new tasks: an ordinary synchronous scoped
change and a genuinely asynchronous state/ownership change, each with native
positive/negative fixture controls and a scope-preservation check. Use candidate,
current production and contemporary no-skill comparisons; retain every scheduled
attempt and all cost/failure/capture records. Total distinct tasks stays below ten.
Neither old form/refresh fixtures nor a favorable result selected after reruns
may stand in for this comparison. Both tasks count in the adoption decision.

Observe whether the async guide is read when relevant, whether it is needlessly
read for the synchronous task, native outcomes/cleanup, and full token/time cost.
Extra reads, failed edits, missed guidance and cleanup recovery all count. A body
word reduction alone cannot pass the gate, and an aggregate win cannot hide a
lost required behavior. Candidate has not been model-tested; charts stay frozen.
