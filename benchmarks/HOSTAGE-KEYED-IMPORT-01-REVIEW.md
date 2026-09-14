# Keyed import 01 — contract transfer with diagnostic limits

2026-09-14, launch `6d0d108`, resources `c0aa9a1`.
[Frozen protocol](HOSTAGE-KEYED-IMPORT-01-PROTOCOL.md);
[retained evidence](results/hostage-keyed-import-01/).
One authored transfer task, one explicit-skill Astra medium session, no baseline
or favorable retry. **118,971 total tokens / 103.161 seconds** (115,979 input,
2,992 output; cached input counted once). Six shell calls, full Python asset read.
Do not compare this larger task to the earlier form task as equal work.

## Original model evidence

The implementation owns a per-instance set, marks a key before fetch and keeps it
through persist, suppresses same-key duplicates, and removes only its own key in
finally. Active payload/result/error semantics are preserved. Both supplied tests
remain byte-identical. Added files are only controlled_call.py and test_importer.py;
requirements remain unchanged. Raw usage/events, installed resource hashes,
complete project inventory and exact copied asset reconcile.

The actual native command captures all **six tests passing in 0.043s**: the two
existing tests plus four added tests with subtests. The generated tests use
`started_before` with corresponding owned tasks. Duplicate checks await completion
without asserting its unspecified result. They cover equal-but-distinct string
keys, duplicates during both phases, independent keys/instances, exact active
payload/result/error values, four synchronous/async failure combinations, retries
and cancellation in both phases while another key remains active. State snapshots
copy the set rather than aliasing it. No original failed test attempt is observed.

Task ownership cleanup is registered before waits; entry/result waits are bounded.
Cleanup cancels and gathers owned tasks without a separate gather deadline. The
actual fixture callbacks cooperate with cancellation; this does not promise
containment of arbitrary cancellation-suppressing code. Native test execution is
separate from final diff checks. Empty output items 5/9 are copy and cmp/diff,
not missing test transcripts. Semicolon-separated final checks expose only their
last shell status; reconciliation separately verifies copied/original bytes.

## Separate unchanged-test controls

[Author replay](results/hostage-keyed-import-01/author-replay.json) uses six
disposable project-local copies, 20-second process bounds, unchanged tests and
full native output. Every run discovers six tests; subtest failures can exceed
that count. Original project files are unchanged afterward.

| Implementation | Native observation |
| --- | --- |
| Final | 6 pass, 0.044s |
| Valid duplicate return False | 6 pass, 0.045s |
| Original without busy state | 8 subtest/test errors: missing required busy_keys |
| Missing duplicate guard | 2 failures + 1 error; actual forbidden callback executes |
| Missing cleanup | 9 failures + 1 error; busy keys remain present |
| Blocks every key when any key is busy | 8 failures + 1 error; independent work is suppressed |

All preregistered variant-level expected exits match, but that does **not** mean
all diagnostics are good. Three faulty variants also produce `UnboundLocalError`
for `saved`: dependent fetch/persist phases are wrapped in continuing subtests,
so an earlier assertion can skip the assignment and still reach later code.
The intended duplicate/state/entry failures are retained before that secondary
error. Do not attribute the unbound local to the production implementation or
count it as another defect detected. This is a concrete next test-generation
improvement, not a reason to rewrite the original model artifact.

The all-keys-blocked variant produces early `EntryNotObserved` for the suppressed
application task, demonstrating real task-aware waiting in a second workflow.
No replay times out. This is diagnostic behavior, not a measured model speed gain.

## What this establishes

The candidate can produce a test suite that accepts an alternative duplicate
result while detecting ownership and cleanup faults in a two-stage keyed workflow.
The task explicitly states the duplicate return is unspecified, so skill guidance
and task clarification are confounded. This does not isolate the instruction
change's effect, establish generalization to external projects or prove efficiency.
The prior [form overconstraint](HOSTAGE-PYTHON-ENTRY-MODEL-01-REVIEW.md) remains a
real adverse result. No featured chart, old score or measured resource is changed.

No skill source changed during this screen. The skill-creator guidance was used
to keep the transfer task scoped and distinguish contractual outputs from an
implementation choice; no new universal skill rule was added for this result.
Local repository validation: 499 tests pass in 68.930s, no failures/skips;
catalog/link checks and featured EN/KO synchronization pass. This is maintenance
verification, not another model run or a performance score.
