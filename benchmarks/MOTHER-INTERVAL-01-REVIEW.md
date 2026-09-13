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
