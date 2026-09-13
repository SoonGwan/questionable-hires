# Native transcript review diagnostic — 2026-09-14

This is local evidence-integrity work, not a model performance experiment or a
skill efficiency improvement. Historical runs and their metadata are unchanged.

## Observed boundary

Interval checkpoint 01's protected skill command `item_6` has only started and
completed events in the original CLI stream. Its completed output already lacks
earlier verbose test lines. Thus the loss predates export; this inspection does
not establish the upstream cause or recover the missing output.

## Prospective diagnostic

`run.py` now records `unittest_transcript_review_candidates` alongside existing
capture diagnostics. For a command mentioning unittest and a verbose flag, with
one standard `Ran N tests` summary, fewer standard method headers than reported
tests creates a manual-review candidate. It does not change completion, test
outcome, token accounting, scoring, retries or exclusions.

Custom runners, multiline descriptions, output filtering, subtests, commands
containing misleading strings and multiple runs limit this heuristic. No warning
does **not** prove complete capture. Neither a warning nor a missing line proves
a test failed. Multiple-summary and non-verbose commands are left unclassified.

Read-only application to all four retained interval exports:

| Cell | Reported tests | Visible standard headers | Review candidate |
| --- | ---: | ---: | --- |
| Protected baseline | 3 | 3 | No |
| Protected skill | 6 | 1 | Yes, item_6 |
| Final-only baseline | 2 | 2 | No |
| Final-only skill | 3 | 0 | Yes, item_7 |

These agree with the existing manual review; a new diagnostic is not independent
confirmation of the underlying test outcomes. The old metadata remains frozen.

## Local validation

The runner tests execute a real stdlib suite with two successes and one intended
assertion failure. Complete verbose failure output is not flagged; removing its
leading method lines is flagged without changing exit status or original events.
Controls cover partial success, quiet/unrelated commands, empty output and multiple
summaries. All 19 runner tests pass. The first test attempt revealed that the
test's slicing removed the final method name as well; its slicing was corrected
to retain that name. Production detection was not changed to fit the expectation.

No fresh model sessions were run for this change; no efficiency claim or chart
update follows from these checks.
