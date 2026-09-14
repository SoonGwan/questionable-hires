# Receipt tree guard adoption 01 — reviewed 2026-09-14

Launch `eb16150`, resources `ec0cc28`; [protocol](RECEIPT-TREE-MODEL-01-PROTOCOL.md),
[export](results/receipt-tree-model-01/), [candidate](RECEIPT-TREE-GUARD-01.md).
One unchanged exposed task, explicit skill, Astra medium, serial n=1, no retry.
Fixture SHA-256 and installed resource hashes/modes match the frozen source;
installed resources and original project bytes remain unchanged.

## Actual adoption and cost

| Execution | Tokens | Process seconds | Shell calls |
| --- | ---: | ---: | ---: |
| [Guide 01](RECEIPT-GUIDE-MODEL-01-REVIEW.md) | 76,746 | 49.094 | 4 |
| [Output choice 01](RECEIPT-OUTPUT-CHOICE-01-REVIEW.md) | 82,253 | 53.954 | 6 |
| Tree guard 01 | 76,962 | 46.154 | 4 |

Against the immediate predecessor: tokens **−6.43%**, time **−14.46%**. Against
guide 01: tokens **+0.28%**, time **−5.99%**. Current usage is 75,897 input plus
1,065 output; cached input 65,152 and reasoning output 55 are already included
in their respective totals. Completed without timeout.

The model reads the entry, guide and project sources, selects `guard_tree: true`
and compact output, and invokes the helper without reading its implementation.
No custom hash implementation or full hash listing is generated. A short wrapper
still runs the helper and three Git checks; unlike prior wrappers it propagates
any nonzero child exit. All four child exits are zero. A separate HEAD lookup and
repeated diff/status reads remain, so this is not a minimal-work proof.

Observed removal of custom inventory work supports this capability's usefulness
on this task. It does **not** establish causality, an all-eight improvement or a
20–30% gain. These are exposed n=1 sessions with shared cache, different resource
versions and unequal work, without a contemporary baseline. No favorable retry
was used and neither historical nor featured graphs change.

## Original evidence

Item_5 contains complete native transcripts for all five current methods in both
copies: query/token-padding assertions fail on HEAD with truncated URL/`abc`,
while three controls pass; all five pass with the working parser. Four copied
module checks cover settings, implementation, test module and support. No phase
timeout/truncation is reported. Current tests/samples are identical in both copies.
HEAD is `1877068eeac6ccbd648ab48ad3dc6e18b2458644`; working parser SHA-256 is
`5351ff27199aca2c61d7431b184fa34ff87e52bb563dd903c997dfec58674513`.

The original guard reports unchanged **80 entries / 37,100 file bytes**, inventory
SHA-256 `456ae61737ba153fd8b3941328b8caa02c0c6fa1da99c663197b58e48a9e6b54`.
Selected hashes/modes include unrelated notes. Comparison copies are removed;
no extra harness/report remains. This whole-tree guarantee covers the helper's
comparison interval, not Git operations before or after it, external link targets
or concurrent/transient changes.

**Prefix gap remains:** the submitted wrapper flushes a `COMMAND:` line before
launching the helper, but original raw output starts at the helper JSON. Later
command/exit lines are present. Automatic empty diagnostic lists do not establish
full capture. The missing prefix does not remove the native suite or guard result;
the executed helper command is retained in submitted source. Do not reconstruct
the missing original observation using replay.

## Separate replay: native equality, different tree identity

`python3 -B benchmarks/replay_receipt_guide_01.py --profile tree-01` reconciles
raw/redacted events, terminal usage, frozen fixture and installed files. It runs
the actual literal recipe unchanged in a disposable copy of the retained workspace,
not the whole wrapper. All native and selected-file result fields match after
normalizing only temporary paths and native test durations.

The **full result does not match**: replay guard reports 80 entries / **37,843 file
bytes**, digest `7ed5e187a3b1d29bd584000d4136adcffd614ce88baaf779929466a2a7f937d5`.
Replay independently checks that this matches its actual before inventory and
that the whole inventory remains unchanged afterward. Original retained workspace
and exported project inventories also remain unchanged by replay.

The runner executes `git add -N .` and force-adds supplied working paths **after**
model timing/output collection, so the retained Git index is post-collector state.
This is a concrete source of tree differences, not a reason to normalize hashes
away. The original per-file tree inventory was not printed, so the exact complete
original-to-retained difference cannot be reconstructed or attributed solely to
the collector. Later model Git status also lies outside the guard interval.
[Author replay](results/receipt-tree-model-01/author-replay.json) explicitly keeps
`observations_match: false` and both guard objects; native/selected equality is a
separate field. Original and replay tree identity must not be presented as equal.

Next evidence should improve pre-collector inventory retention and test transfer,
not keep repeating this exposed task until the desired percentage appears.
