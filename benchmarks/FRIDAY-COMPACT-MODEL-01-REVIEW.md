# Friday compact entry comparison — review in progress

Launch `ce6dd4e`; original `b2816cd`, candidate `e063131`.
[Frozen protocol](FRIDAY-COMPACT-MODEL-01-PROTOCOL.md). This compares two explicit
skill versions, not either version against no skill. No aggregate before all
six sessions finish and raw/resource/original-file reconciliation is complete.
No author tests or resource/task edits during timing.

## Rolling schema — original

Completed: **72,238 tokens / 38.804s**, five shell calls. Reads entry, then batches
actual six release files with the core matrix reference. Executes the matrix CLI
once using actual reader literal references, all four initial/up/new-write/down
states. Native complete/nontruncated output captures both incompatible readers
and updated, unchanged and inserted rows surviving down. No model-written value
assertion loop or additional artifact. Correctly blocks rollout and rollback
orders, identifies the last compatible state and separates schema reversal from
restoring previous data. Does not invent application-writer/staging evidence.
Final diff is empty and status contains only installed skills. No observed
capture/scope issue; raw/resource/inventory reconciliation pending after timing.

## Rolling schema — candidate

Completed: **87,540 tokens / 39.824s**, six shell calls. Reads compact entry and
actual release files, then opens the unchanged core matrix reference separately.
Also collects a last-commit header despite no unresolved historical dependency.
Executes the matrix once with actual reader literals and all four states; native
complete/nontruncated observations retain updated, unchanged and inserted rows
after down and expose both reader incompatibilities. No extra assertion loop or
project artifact. Correct final readiness/recovery conclusion, with missing
application writers and staging still unknown. Final diff is empty; no observed
capture/scope issue. Raw/resource/inventory reconciliation pending after timing.

Both schema sessions preserve the required evidence, but candidate performs an
extra separate reference read. Recorded costs are **+21.18% tokens / +2.63% time**
versus original on this pair. Shorter entry text does not establish lower session
cost. Do not infer that compression caused the extra command from n=1, accept an
efficiency win, or stop the frozen writer/control schedule on this adverse pair.
