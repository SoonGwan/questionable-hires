# Receipt output choice 01 — reviewed 2026-09-14

Launch `15a2e38`, resources `72e1ff2`; [protocol](RECEIPT-OUTPUT-CHOICE-01-PROTOCOL.md),
[evidence](results/receipt-output-choice-01/),
[previous execution](RECEIPT-GUIDE-MODEL-01-REVIEW.md).
One unchanged exposed task, explicit skill, Astra medium, serial n=1, no retry.
Fixture/resource hashes and modes match the frozen source and remain unchanged.

## Adoption is observed; efficiency improvement is not

| Recorded resource | Previous guide run | Output-choice run | Change |
| --- | ---: | ---: | ---: |
| Total tokens | 76,746 | 82,253 | +7.18% |
| Process seconds | 49.094 | 53.954 | +9.90% |
| Shell calls | 4 | 6 | +2 |

Current usage: 80,900 input + 1,353 output. Cached input 67,072 is already
included; reasoning output 25 is already included in output. Completed, no timeout.
This is a descriptive comparison of exposed single executions with shared cache
and different work, not causal attribution to the wording. There is no concurrent
baseline. Do not promote this result or alter historical/featured graphs.

The model reads the entry, compact guide and project sources, then invokes the
helper without `--pretty` and without reading its implementation. It nevertheless
adds a separate 39-file hash/mode listing including Git metadata, then computes
another whole-tree snapshot inside its comparison wrapper. Guide adoption did
not remove this extra work or establish lower whole-task cost. The helper's
selected-original check does not replace requested whole-tree/entry guarantees;
simply deleting all outer verification would be an unjustified shortcut.

## Original evidence and a capture limitation

Item_7 contains the complete native five-method suite for each copy: the token
padding and query-value tests fail on HEAD (actual values `abc` and the URL ending
at `?x`); the other three pass. All five pass with the existing working parser.
Five same-process import checks cover settings, implementation, checks package,
support and test module. Neither phase times out or truncates.

The literal recipe puts AGENTS.md in `watch` instead of `fixed` and includes the
checks package in import verification. Current tests/samples remain fixed in both
copies. HEAD is `1877068eeac6ccbd648ab48ad3dc6e18b2458644`; working parser SHA-256
is `5351ff27199aca2c61d7431b184fa34ff87e52bb563dd903c997dfec58674513`.
The helper reports selected originals unchanged and copies removed. Outer output
reports unchanged file bytes/modes and no added, removed or changed paths. Each
of four Git checks reports exit 0; no extra harness/report is retained.

**Original prefix gap:** the submitted wrapper prints `SPEC ...` and `PYTHON ...`
with flushing before invoking the helper, but the raw original item_7 output
starts at the helper JSON. Neither prefix is present. Thus empty automatic
diagnostic lists are not evidence of complete capture. The decisive native suite
results are present, but the final answer's exact Python 3.9.6 claim is not backed
by that missing version line. Do not reconstruct the original version observation
from later execution. The recipe is recoverable from the submitted command.
The wrapper prints each exit but does not propagate every failed child as its
own exit; this run's printed child exits are all zero.

## Separate author replay

`python3 -B benchmarks/replay_receipt_guide_01.py --profile output-choice-01`
reconciles raw/redacted events, usage, frozen fixture and installed resources;
executes the actual literal recipe unchanged in a disposable project copy; and
compares all helper result fields after normalizing only copy paths and native
test durations. All match and copied/original file inventories are unchanged.
[Replay output](results/receipt-output-choice-01/author-replay.json) does not rerun
the whole outer wrapper or fill its original prefix gap. Exported project files
match the unchanged fixture plus supplied working changes.

The instruction remains a narrow clarification of an existing lossless option,
not an accepted performance optimization. Further work should address unnecessary
evidence construction/output, not accumulate format advice or repeat this fixture
until a favorable number appears. Runtime and discovery behavior remain unchanged.
