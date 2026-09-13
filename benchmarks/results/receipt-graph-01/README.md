# Graph comparison: helper adopted, no efficiency gain

[Frozen protocol](../../RECEIPT-GRAPH-01-PROTOCOL.md), [run](run.json),
[metadata](summary.json). Revision `884915e`, Receipt entry/helper `75c8718`,
reference examples `077805c`. One authored task, baseline then skill, serial
Astra medium, n=1. Both completed; no model retries, exclusions, candidate edits
or concurrent author tests during timing. Not organic real-repository evidence.

| Arm | Input + output tokens | Process seconds | Shell calls | Native outcomes |
| --- | ---: | ---: | ---: | --- |
| Baseline | 83,721 | 56.411 | 4 | Before: 2 assertion failures + 4 passes; after: 6 passes |
| Receipt | 96,687 | 72.288 | 4 | Before: 2 assertion failures + 4 passes; after: 6 passes |

Receipt records **+15.49% tokens / +28.15% time**. Cached input counts once;
reasoning output is not added again. Shared host/cache, ordering, n=1 and
different repair/support work prevent causal attribution. This is not a saving.

## Reviewed behavior

[Baseline commands](uncommitted-graph-fix--baseline--1/commands.json) first use
an unavailable `python` command (exit 127), recover with `python3`, then build a
native comparison script. It copies HEAD/current implementation and identical
current tests into project-local temporary copies. Within each child process it
checks the imported planner path and runs the six-test unittest suite. It captures
commit/content identities, checks original bytes/status, and removes its copies.

[Receipt commands](uncommitted-graph-fix--skill--1/commands.json) read the entry
and full updated reference, not the helper implementation. The model invokes
`compare.py` with `fixed: [test_planner.py]`, `vary: [planner.py]`, `before: HEAD`,
`after: {working_tree: true}`, `imports: [planner]`, native unittest and all six
current tests. **The new working-tree helper is actually adopted.** Its output
shows same-process copied imports, before cycle AssertionErrors with four passing
controls, and all six after passes; helper exit is zero, no timeout/truncation.

The model adds an original-file/status guard around the helper and sets TMPDIR
to the project root. A new `xcrun_db` file appears; this makes that wrapper exit
one despite successful comparison. A separate command removes this newly created
file and rechecks original hashes, modes, status and temporary-copy cleanup.
The precise process that created the file is not independently traced. This is
observed launcher/environment overhead, not a proven helper defect or test failure.
No helper/test rerun follows the cleanup. Both arms' repair costs remain included.

## Evidence and limits

- Both final project exports contain exactly the **five initial files**, with
  bytes equal to the committed-plus-working fixture, including unrelated notes.
  Both `changes.diff` files are empty; `initial.diff` preserves the supplied fix.
  Neither arm is credited with writing it. Installed resource inventories and
  hashes are unchanged and match the frozen candidate.
- Both satisfy the explicit end-of-task comparison-copy deletion requirement.
  Both verify the same current six native tests against HEAD and the working
  implementation, including import provenance within each test process.
- Before commit is `7180b34dc5ee5c3c309eb04346860c88a477f25e`; working planner
  SHA-256 is `5a54575496ae852d3d508124427b69b5d6a016cf55c798ab7fe8a27ff0ac3977`.
  Core before/after outcomes and helper revision/hash records are captured.
- Automated capture diagnostics report no empty output, invalid JSON or rejected
  patches, but do not prove completeness. The skill wrapper's captured output
  starts at `COMPARISON EXIT: 0`, omitting its earlier initial-status print.
  Do not reconstruct that missing prefix from final prose or author replay.
- Helper adoption is not a scored obligation. Baseline's native solution is valid.
  Different native/helper support work, baseline interpreter repair and skill
  launcher-file cleanup mean this is not controlled isolation of helper cost.
  Author fixture preflight is separate from these original model observations.

## Next engineering target

Executable examples transferred to actual use, but did not reduce end-to-end
cost here. Investigate duplicated orchestration/integrity bookkeeping and
project-local temporary-environment behavior before another performance claim.
Preserve required checks and original-file guarantees; do not remove obligations
or force helper adoption to improve a score. Confirm any later change on separate
tasks, not repeated optimization of this exposed case. The all-eight goal remains
unmet. Featured charts and historical adverse results are unchanged.
