# Receipt single-guide adoption 01 — reviewed 2026-09-14

Launch `885a1f5`, skill resources `723be6f`; [frozen protocol](RECEIPT-GUIDE-MODEL-01-PROTOCOL.md),
[exported evidence](results/receipt-guide-model-01/),
[candidate](RECEIPT-GUIDE-COMPACT-01.md). One exposed `src-settings-fix` task,
explicit skill, GPT-6 Astra medium, serial, n=1, no retry. Frozen fixture SHA-256:
`2ca86a989d524318d47a96f46053a79aff16f551a439f7d47d898a336ed87d07`.

## Original model observations

Completed in **49.094 seconds**, **76,746 total tokens**: 75,515 input plus
1,231 output. The 59,904 cached input tokens are already included in input;
90 reasoning output tokens are already included in output. Four shell calls.

The model reads the entry, compact single guide and actual project inputs, then
uses the copied comparison helper without reading its implementation. Its literal
recipe freezes the current `checks/`, package initializer and project instructions;
only `src/settings/parser.py` varies between HEAD and the existing working fix.
It selects `src` as an import root and verifies four copied module origins.

| Current test | HEAD implementation | Working implementation |
| --- | --- | --- |
| Duplicate key, last wins | Pass | Pass |
| Empty value | Pass | Pass |
| URL query containing equals signs | Fail, truncated value | Pass |
| Token padding containing equals signs | Fail, padding lost | Pass |
| Whitespace and comments | Pass | Pass |

Both native five-method transcripts are present: before exit 1 with two actual
assertion failures and three controls passing; after exit 0 with five passes.
Neither phase times out or truncates. Before commit is
`1877068eeac6ccbd648ab48ad3dc6e18b2458644`; working parser SHA-256 is
`5351ff27199aca2c61d7431b184fa34ff87e52bb563dd903c997dfec58674513`.

The helper reports unchanged selected originals, including unrelated `notes.txt`,
and removed comparison copies. The outer program independently reports unchanged
39-file bytes/modes (including Git) and unchanged directory entries. Git checks
each report exit 0. No extra harness or report remains in the measured project.
The original output contains the decisive native evidence; no decisive capture
gap was observed. Empty diagnostic lists alone are not the basis for that finding.

## Separate author verification

[Replay script](replay_receipt_guide_01.py) reconciles frozen fixture content,
installed resource hashes/modes before and after, raw/redacted event streams and
terminal usage. It extracts the actual literal recipe from the original command
and executes that recipe unchanged in a disposable copy, **not** the whole outer
verification wrapper. All result fields match after normalizing only temporary
project/copy paths and native test durations. Original and copied file inventories
remain unchanged. [Replay output](results/receipt-guide-model-01/author-replay.json)
is separate evidence, not a replacement for the original transcripts.

## Limits and next bottleneck

This establishes adoption and preserved behavior on one previously exposed task,
not a causal cost reduction, independent transfer or all-eight improvement. There
is no contemporary baseline. Guide bytes fell 8.08%; this percentage is **not**
model token savings. Historical/featured graphs remain unchanged.

The model still chooses `--pretty` output and writes an additional whole-tree
hash wrapper, including Git metadata and installed resources. Some integrity
coverage overlaps the helper; scope is also broader than its selected-file checks.
These observations motivate investigating reusable integrity evidence and output
volume, but do not establish that removing checks would preserve all obligations.
The wrapper prints each exit but does not propagate every failure as its own exit;
this run's actual printed exits are all zero, so no hidden failure is inferred.
