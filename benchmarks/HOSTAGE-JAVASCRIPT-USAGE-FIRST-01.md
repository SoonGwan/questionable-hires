# JavaScript usage-first candidate — 2026-09-14

Instruction candidate, following the [lifecycle screen](HOSTAGE-JAVASCRIPT-SCOPE-MODEL-01-REVIEW.md).
Its [first model screen](HOSTAGE-JAVASCRIPT-USAGE-MODEL-01-REVIEW.md), resource
`f0b29dd`, adopts the shorter read and preserves required regressions, but uses
30.82% more total tokens / 6.75% less wall time than its fresh baseline. No general
efficiency claim; this is one exposed authored pair, not independent confirmation.
That run loaded the full module and took seven shell calls versus five baseline,
with +10.80% total tokens. Existing instructions already requested batched reads;
adding another generic batching rule would not address the observed full-source
read. No causal fraction of measured cost has been established.

## Change

The JS route now reads the opening usage comment alongside known application
files, then copies the complete module. Its delimiter-based sed command reads
through the closing comment rather than relying on a stale line number. The
implementation remains available for adaptation or unclear behavior. This is
progressive disclosure, not a ban on inspecting copied code or permission to
skip application tests. Python routing and runtime behavior are unchanged.

The usage comment additionally discloses `run()` converting synchronous throws
to rejected Promises, and how to assert the original API does not throw before
registering its task. The previous model explicitly guarded against this masking;
the shorter reading path must retain that information. All lifecycle deadlines,
cleanup obligations and cancellation limitations remain in the comment.

## Local checks and limits

The documented sed command was run on the actual asset and stops at the closing
comment. Executable source from `export function controlledCall` onward is
byte-identical to `22bd929`. Native callback/lifecycle suites and standalone-copy
integration passed: three Python integration checks in 0.290s, containing the
seven original and ten lifecycle native tests. Skill validation passed.

The entry grows slightly and the module gains three comment lines. This does
not shrink the copied module. Only a model trace can show whether it chooses the
shorter read, avoids compensating extra calls and preserves real task outcomes.
Historical model numbers and featured graphics remain unchanged.
Before measuring, freeze its revision; use unchanged explicit contracts, retain
all attempts and review implementation, tests, scope, original capture and raw
cost. Exposed development pairs remain distinct from independent confirmation.
