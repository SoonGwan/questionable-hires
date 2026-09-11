# Separate emitted evidence from task success

Investigation after the Exorcist setup follow-up, runner revision `34703be`.
No new model benchmark or skill change was needed for this check.

Official [non-interactive mode documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
describes `--json` as a JSONL event stream on stdout and `workspace-write` as the
explicit edit-permitting sandbox mode. The runner already uses those modes;
this investigation does not widen permissions, change credentials/configuration,
switch models, or infer that emitted events contain every byte of tool output.

## What was established

For `local-runs/exorcist-runtime-01/runner-environment-timing--skill--1`, the
original CLI command-completion event contains 451 characters of output. Its
first original-unittest failure section is absent even in `stdout.original.jsonl`,
before redaction or report generation. The retained script and independent replay
show that section. This localizes the observation gap upstream of our report
transformation; it does not identify the CLI/runtime component that lost it.

A subprocess-backed regression test substitutes a deterministic JSONL producer
for the model CLI, while exercising actual process pipes, `communicate`, complete
cell preparation, log persistence, metadata and snapshots. First/middle/last
multiline command output, including Korean text, survives unchanged. This does
not reproduce or clear the real CLI's intermittent behavior; it establishes that
the tested runner path preserves the complete text it receives.

`httpx-diagnosis-03` contains one stderr `patch rejected` report. Successful later
artifact creation and original-file integrity do not establish why it was
rejected or which attempted path was involved. Path aliasing remains only a
possible explanation, not a diagnosed cause. No permission relaxation or path
workaround is shipped based on that hypothesis.

## New metadata, not a new score

`capture_diagnostics` records invalid JSON line numbers, JSON non-object line
numbers, completed commands with empty/missing aggregate output, error/failed-turn
event types, and the number of stderr patch-rejection markers. Original stdout
and stderr are still retained; parsing does not silently discard malformed lines
without describing their locations. Old raw results and metadata are unchanged.

Empty command output may be normal; nonempty command output may be incomplete.
The known partial-output run has no empty-command marker, demonstrating why this
field is not an automatic completeness verifier. Marker absence does not certify
capture. Patch rejection is not proof of a successful outside write. CLI process
completion remains distinct from correctness, scope, and complete evidence.

Full local suite: 92 passes; the updated real-subprocess capture test also passes
in its 10-test runner suite. Eight skill metadata/link sets validate. These are
mechanical checks, not a model performance improvement.

For future performance decisions, preserve adverse costs and inspect diagnostic
flags, actual commands, and retained artifacts. If a decisive output section is
missing, independently replay the reviewed local reproduction and label that
evidence separately, as already done for the runtime control. Do not fill gaps
from expected answers or erase rejected attempts. Further CLI root-cause work
requires a bounded reproducible tool-capture/patch failure, not more unchanged
developer benchmark repetitions.
