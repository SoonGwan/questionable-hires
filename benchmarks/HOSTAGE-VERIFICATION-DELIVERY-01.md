# Hostage verification delivery — instruction and diagnostic candidate

The [controlled-call model screen](HOSTAGE-CALL-MODEL-01-REVIEW.md) has no native
test output in its original final command, although the final answer claims six
passes. Semicolon-chained Git status supplies shell exit 0 independently of the
test's exit. Separate replay validates retained tests but cannot fill that gap.

Hostage's delivery guidance now asks for the test's own exit and observed required
checks, not the last shell command's success. Missing, undiscovered or skipped
checks do not support a pass claim. Inspect existing evidence before rerunning
only an unresolved safely repeatable check. No new mandatory harness, universal
rerun, output-file requirement or subprocess restriction is introduced.

The benchmark collector adds `unittest_missing_summary_review_candidates` for
commands containing `-m unittest` without a native count summary. Existing
verbose-header diagnostics miss this whole-summary case. This new heuristic is
review-only: redirection, unrun shell branches, setup failure, custom output and
capture gaps can look alike. It cannot prove capture loss, test failure or
success. Zero-test summaries are not flagged by this missing-summary rule, but
are also not automatically accepted as verification. Shell syntax is not fully
parsed; commands expressed in other forms can evade the check.

Regression checks apply the new detector to retained original events: item_8 is
flagged while its exit 0, content and terminal completion remain unchanged.
Native unittest failing output remains a complete transcript, not missing output.
Controls cover successful/failed/zero-count summaries, redirected logs, an unrun
command and setup error. No historic metadata or scores are rewritten.

Initial targeted runner suite: 21 tests pass in 2.637s. Skill structure, local links
and featured synchronization pass. These are local diagnostic checks, not proof
that the revised skill obtains better model results or cheaper verification.
The callback asset is unchanged from `d9e7711`; new instruction adoption and
token/time effects remain unmeasured. Historical and featured numbers stay fixed.

Full local suite after final test edits: **454 tests pass in 80.333s**, no
failures/skips. This is not hosted CI or a new model measurement.
