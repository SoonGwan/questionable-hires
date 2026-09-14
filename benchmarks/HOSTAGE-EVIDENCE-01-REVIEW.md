# Handoff evidence screen 01 — 2026-09-14

Launch `fe62f84`, resources `6510712`; [frozen protocol](HOSTAGE-EVIDENCE-01-PROTOCOL.md).
All three scheduled explicit-skill sessions completed without timeout/retry.
Timing ended 2026-09-14 11:53:30 UTC before author replay or edits. New authored
handoff scenarios reuse an exposed six-test form project; no baseline comparison,
independent holdout or causal instruction-effect estimate. Tasks explicitly ask
for attribution and distinguish new verification from old evidence.

| Handoff | Tokens | Seconds | Original observed behavior |
| --- | ---: | ---: | --- |
| Matching report | 96,307 | 40.542 | Matches command/five hashes; reuses prior evidence without a test rerun |
| Stale report | 97,260 | 43.977 | Repairs cleanup, restores exact prior inputs, reuses attributable report |
| No report | 74,656 | 31.630 | Issues new native test command, but original result output is missing |

Input includes cached input once plus output; all usage known. Different work,
shared host/cache and n=1 preclude cross-case efficiency claims. Completion is
not a three-out-of-three verification success result. No featured/graph updates.

## Matching report

Reads actual form, requirements, all test/support files, handoff and prior report.
Checks exact native command, complete expected five-file digest set, each current
digest, recorded exit zero, count six and all six named passes/terminal OK. The
final answer explicitly reuses prior verification rather than claiming a new run
or recovery of the missing transcript. No edits or new test run occur.

The collector flags a missing-summary candidate because the evidence-comparison
program contains a `-m unittest` command string. It does not invoke that command;
this flag is not missing test output or a failure. Separate evidence/diff/status
exit handling is captured. All prior report contents are present in original reads.

## Stale report: valid restoration and reuse

Reads actual sources and observes the changed form hash plus `finally: pass` diff.
Only restores pending cleanup in form.py. The corrected file is byte-identical to
the previously tested file; all five input hashes and native command then match.
Current/prior interpreter paths agree in captured output. The old six-pass native
report is printed and explicitly labeled prior verification, with no new suite run.
All tests, support and handoff/report files remain unchanged.

The protocol anticipated stale evidence might trigger a new run, but the visible
task permits reuse after matching current inputs. Restoring exactly the tested
implementation is a supported alternative, not a failure for skipping a rerun.
Do not invent an after-every-edit rerun requirement or reward redundant work.
This is a local standard-library fixture; no changing external state is in scope.

## Absent report: original verification remains unconfirmed

Reads actual files and recognizes that the previous unsupported pass claim cannot
be reused. Issues a new native unittest command with separate suite, copy-integrity,
preservation and status exits. Its final answer claims six passes and native exit 0,
distinguishing that claimed new run from the earlier missing transcript.

However, original item 4 output contains only `?? .agents/` and `STATUS_EXIT=0`.
No native count/test lines, NATIVE_SUITE_EXIT, copy exit or preservation exit are
captured. The final shell exit and answer do **not** establish a new native pass.
That observation stays unverified even though the retained code later passes.

The gap already exists in `stdout.original.jsonl`; the saved events are its exact
path-redacted form. run.py writes the captured CLI stdout directly before export;
export/redaction did not remove a native section. We have no independent record
of what tool output the model itself received. Thus neither “the model ignored
visible missing output” nor a specific upstream logger defect is established.
No attempt was restarted or rescored to remove this limitation.

## Separate artifact verification

[Author reconciliation/replay](results/hostage-evidence-01/author-replay.json)
checks raw terminal usage/events, frozen installed resource hashes/modes, complete
initial source reads and retained file inventories/modes. Matching/absent projects
are unchanged; stale restores only the authorized form.py working change. No new
artifacts, test edits or prior-report edits remain.

Four bounded native executions in disposable project-local copies use unchanged
retained tests: each final project runs six passes; stale's initial missing-cleanup
implementation fails six intended True-is-not-False assertions. All counts/exits
and input preservation match. These are author tests, not replacement output for
the absent-report cell. Full original attempts, source hashes and projects remain
in the [export](results/hostage-evidence-01/run.json).

Next: investigate capture consistency before treating every absent raw section as
a reasoning failure requiring more skill prose. This screen does not exercise
live-process waiting, unsafe replay refusal or genuinely unavailable verification.
Those branches, broad all-eight efficiency and hosted release readiness remain
unproven. No skill edit was made during this review.
