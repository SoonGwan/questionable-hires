# Interval-contract checkpoint 01 — incremental review

Run in progress; no aggregate or improvement acceptance. [Protocol](MOTHER-INTERVAL-01-PROTOCOL.md),
resource/launch `14289df`. Four fresh serial Astra medium sessions, unchanged
protected/final-only tasks. No resource/task edits or author tests during timing.

## Protected search — baseline

Completed: **66,305 tokens / 68.208 seconds**, five shell calls. Adds only
test_search_overlap.py and runs three actual native tests (0.017s), all passing.
Tests cover both completion orders from empty state and normal-order overlap after
a real successful seed. They assert retained display after older completion while
newer remains pending, and final newest ownership. No defect is manufactured.

Custom per-request fetch objects expose actual entry Events/Futures; explicit
pending checks, two-second waits and owned-task cancellation/draining are present.
Source SHA-256/Git diff are captured unchanged before/after. Correct final report
and exact native rerun command. No capture diagnostics or observed scope deviation.
Standalone author replay and other scheduled cells remain pending.

## Protected search — skill

Completed: **72,758 tokens / 78.579 seconds**, five shell calls. Reads only the
native route, copies controlled support into standalone test_search.py, and
explicitly adopts continuous retention from the user task. Retained assertions
now check the seeded display after older completion while newer is pending,
for distinct and repeated keys; reverse/final ownership and loading entry are
also checked. Normal loading and an intended request-key mismatch bring the suite
to six methods. One-second async waits and owned-task cleanup; no installed imports
or production edits. The rerun command adds a 20-second parent subprocess bound.

**Native capture limitation:** original raw command output starts with a lone
`ok`, then the last test name and `Ran 6 tests ... OK` summary (0.033s). Earlier
individual test output is absent, even though automatic capture diagnostics are
empty and process exit is 0. The complete summary is captured, but a complete
per-test native transcript must not be claimed. Source inspection supports rule
adoption; planned post-timing replay will not fill the original output gap.

The final report is consistent with the retained assertions and captured summary.
No scope deviation appears in commands; exact source/inventory reconciliation and
standalone positive/fault controls follow after remaining model timing.

## Final-ownership-only search — baseline

Completed: **84,413 tokens / 67.610 seconds**, four shell calls. Adds retained
test_search_overlap.py plus SEARCH_QA.md. Actual Search normal completion passes;
reversed completion fails natively with `results for ca` versus `results for cat`
(two tests / 0.012s). Normal intermediate display is intentionally not asserted;
reversed first completion and final latest ownership are. Full native failure
trace is captured, unlike the protected skill's partial per-test transcript.

Two-second waits/cleanup, actual fetch entry and pending peer/Future checks are
present. Baseline additionally asserts Search.run returns None, matching the
current implementation but not an explicit task obligation. The prospective
guarded replay retains that API; it cannot certify every otherwise valid API
change. The extra QA document repeats evidence and the native command. Source and
requirements remain unchanged; no scope violation or capture diagnostic observed.
