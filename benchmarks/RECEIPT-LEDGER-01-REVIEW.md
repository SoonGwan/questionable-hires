# Receipt committed SQLite transfer 01 — reviewed 2026-09-14

Launch `2d8785d`, skills `ec0cc28`, collector `4325a05`.
[Frozen protocol](RECEIPT-LEDGER-01-PROTOCOL.md),
[all four executions](results/receipt-ledger-01/).
Two correlated authored cases, baseline/skill, n=1, Astra medium, serial,
seed20260911. All four complete; no model retries or excluded cells.

## No efficiency win

| Case | Baseline tokens / seconds | Skill tokens / seconds | Skill change |
| --- | ---: | ---: | --- |
| a: complete fix | 69,961 / 60.285 | 131,694 / 72.321 | +88.24% / +19.97% |
| b: incomplete fix | 70,669 / 71.086 | 90,255 / 68.772 | +27.72% / −3.26% |
| Sum | 140,630 / 131.371 | 221,949 / 141.093 | **+57.82% / +7.40%** |

Tokens are input + output, cached input included once. Input/output/cached counts:
a baseline 68,280/1,681/59,264; a skill 130,003/1,691/113,024;
b baseline 68,736/1,933/51,456; b skill 88,647/1,608/70,400. Reasoning output
is already included. Baseline uses three shell calls on each case; skill uses five
on a and three on b. All skill resources match frozen hashes/modes before/after.

Both arms correctly distinguish complete from incomplete fixes, using the actual
five-test SQLite suite in both revisions. HEAD^ has two retry failures and three
passing controls in both cases. Case a HEAD passes five; case b HEAD still has two
retry balance failures despite False acknowledgements. Native actual/expected
tuples, controls and fresh-connection reads support the conclusions; helper CLI 0
is not used as proof that the incomplete fix works.

No all-eight/general claim follows: these are two correlated authored tasks, one
execution per arm, shared host/cache, unequal instrumentation and fixed randomized
order (b skill, a skill, a baseline, b baseline). Historical/featured graphs stay
unchanged. Newly observed adverse transfer outweighs treating the earlier exposed
parser reduction as a broad improvement.

## Observed extra work and backend mismatch

Both skill sessions inspect helper implementation and replace `run_check` in memory
to execute the exact requested `python3 -B -m unittest -v checks.test_delivery`.
The installed helper normally launches its import-checking bootstrap with `-c`.
This is the observed reason given for adaptation, not proof of a causal cost
percentage. The fixture preflight exercised native assertions via the default
helper, not the literal requested `-m` invocation; do not claim it validated that
launcher compatibility. Frozen tasks and original criteria remain unchanged.

Case a reads several source ranges and uses PYTHONVERBOSE import traces, slicing
native stderr between the first test header and native summary. It prints pretty
JSON and repeats a whole-tree inventory outside the guarded comparison. Case b
reads the whole helper and adds temporary `sitecustomize.py` only inside owned
copies, using a child-local PYTHONPATH for same-process provenance. Both adapters
hardcode this suite and replace the helper's process/output handling; they are
observed task-specific code, not supported reusable runtime improvements.

Baselines create their own isolated historical copies (archive on a; tree/blob
copy on b), overlay current tests/schema and execute native unittest. Their import
probes are separate from the test process, unlike skill instrumentation; both use
the same copy and environment. Do not describe all arms as identical provenance
mechanisms or equal work. Loaded implementation hashes/revisions are captured.

## Original evidence and limits

Original native transcripts include all five method results and actual failures
for both phases in all four sessions. Current tests/schema match frozen bytes;
ignored cache, owner notes and remaining project files are preserved. Original
outputs show normal database cleanup, comparison-copy removal and no retained
harness/report. Skill a verifies its entire tree again after Git review; skill b's
guard covers the native comparison interval, not subsequent Git operations.

Baseline a's raw output omits its first revision/copy/current-overlay prefix and
starts at the first import probe. The submitted program, implementation hash,
initial Git log and native results remain; later phase prefixes are present.
This is a capture gap, not something to fill from replay. Skill b's native output
contains four macOS xcodebuild diagnostic lines (two per phase) before test headers;
tests still complete with expected assertions. Do not call its environment clean
or silently remove those diagnostics from original evidence.

## Separate author replay, including failures

[Replay script](replay_receipt_ledger_01.py) executes the actual submitted programs,
unchanged, in disposable copies. It verifies raw/redacted events, usage, frozen
fixture/resources and captured index bytes/hash/mode. Only the disposable copy's
index is restored to the captured end-of-model/pre-collector bytes. Originals are
not modified. [Replay output](results/receipt-ledger-01/author-replay.json) retains
all results; raw binary indexes remain local and are not exported.

- Both baseline programs exit 0 and leave replay inventories unchanged. Captured
  original output matches after normalizing only paths and native durations;
  baseline a's omitted prefix is separately disclosed, not reinstated as original.
- Skill a's complete helper object, including original tree digest, matches. Its
  **outer program exits 1** at the final preservation assertion: later Git review
  changes `.git/index` in the replay copy. Native comparison succeeds, but the
  complete author replay does not. Original outer execution exited 0.
- Skill b's replay exits 0 but `.git/index` changes after helper execution. Helper
  tree identity and non-output fields match; complete helper equality is false
  because the four original xcodebuild lines do not recur. Native tests/assertions
  otherwise match. The adapter has no final whole-tree assertion to reject that
  later index change.

The first strict author replay stopped at skill a's outer assertion. The observer
was changed to record such failures instead of stopping, then ran all four actual
programs unchanged. This was not a model retry or an attempt to obtain favorable
results. Restoration of an index containing original file stat information does
not make a new physical copy equivalent under subsequent Git refresh operations;
the observed changed path is recorded, not normalized away.

Next improvement: provide a supported native-module invocation with same-process
provenance so callers need not inspect/patch internals. Preserve test semantics,
cleanup and bounded execution; validate before any further model screen. This
result does not justify another wording-only optimization or a superiority claim.
