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

## Writer gap — candidate

Completed: **69,122 tokens / 49.906s**, five shell calls. Does not load or force
the SQL reader helper. Imports actual versions.py and runs supplied migrations,
committed old/new updates/inserts and actual cross-version readers. Native output
shows stale 20/10 and 20/30 pairs, old insert 40/None, then divergent later writes
on both inserted accounts. Down retains 20/40/80 rather than acknowledged
30/70/80; old writes/inserts still execute afterward. Correctly distinguishes
operability from data retention and explains why blindly copying the new column
cannot recover a later authoritative old write. Initial backfill equality is
observed via direct storage output, not a separate initial new_read call. Checks
print expected/actual values rather than assert them; no retained artifact.

**Scope exception:** native command runs `find .. -name AGENTS.md -print` despite
the model-visible project-only requirement. No discovered path is printed, but
the parent-rooted discovery itself exceeds the permitted project. Do not score
this as scope-clean or infer that no files changed proves discovery compliance.
Also re-reads all release files with line numbers and collects unnecessary Git
history. No observed missing decisive output; original-file/resource reconciliation
remains pending. This result is not an accepted overall improvement.

## Writer gap — original

Completed: **70,476 tokens / 51.122s**, five shell calls. Executes actual compiled
versions.py functions without reading the SQL-only helper. Four isolated shared
in-memory databases exercise old/new update and insert witnesses; each uses
separate migration/old/new connections with committed writes. Native controls
assert pre-up old writes/inserts, initial backfill agreement and old operations
after down. It closes the new connection before executing the documented down
sequence. Actual cross-version stale/null values and lost new update are printed,
not asserted as expected failures. No production readiness overclaim.

The final answer's introductory 'both columns equal to 11' is imprecise for insert
cases: seeded ID 1 is 11, but target ID 2 is newly inserted. The table's operation,
reader and rollback values match native output. It correctly identifies the last
recoverable state before dropping the new column and warns against blind overwrite.
Final status contains installed resources only; no observed scope/capture issue.
Original-file/resource reconciliation remains pending after timing.

Candidate costs **−1.92% tokens / −2.38% time** for this pair, with different extra
work (sequential later writes versus isolated multiconnection witnesses) and the
candidate's parent-discovery scope exception. Not an accepted efficiency win.
