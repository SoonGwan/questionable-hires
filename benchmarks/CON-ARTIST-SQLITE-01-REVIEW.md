# SQLite commit audit transfer 01 — 2026-09-14

Launch `360775f`, skill resources `8e3bdc4`; [frozen protocol](CON-ARTIST-SQLITE-01-PROTOCOL.md).
Both scheduled serial sessions completed without timeout/retry. New authored disk
SQLite task, n=1 per arm, not an independent real-project holdout. No author tests
or task/resource edits occurred during model timing. The [complete export](results/con-artist-sqlite-01/run.json)
retains both cells, commands/events, source hashes and original projects.

| Arm | Total tokens | Process seconds | Recorded shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 86,152 | 69.112 | 4 |
| Skill | 99,868 | 49.308 | 5 |

Descriptively **15.92% more tokens / 28.65% less time** with the skill. All usage
is known; input includes cached input once plus output. Unequal checks/reads,
shared host/cache, one authored task and baseline's capture gap prevent a causal
efficiency claim. This is not all-eight superiority; no featured/chart promotion.

## Actual behavior and reads

Both inspect actual tests, endpoint alias, ledger and requirements. Both verify
the actual receipt test's `accept` binding to the endpoint and its `_record`
binding to the ledger writer in the same check processes, rather than substituting
a fake endpoint. The fault removes only ledger `connection.commit()`; acknowledgment
and connection closing remain. Stronger native tests read all ordered rows through
a fresh connection after the actual upload. Correct rows retain event 10 and the
new event 20 binary payload; faulty rows retain only event 10. The intended failure
is a missing committed row, not a setup/import exception.

**Baseline:** all sources are read, then three are reread with line numbers.
A heredoc creates project-local correct/fault copies and a shared native runner.
It checks both actual test method globals, endpoint/writer code paths and commit
presence/absence. Four child calls are scripted with expected counts; children
lack individual deadlines (the model cell has an outer bound). Correct/fault copies
are reused, but each native test owns a fresh on-disk database and cleanup.

The original command output **starts during faulty existing tests**. Its leading
fault diff and correct-existing test section are missing. Captured evidence shows
faulty existing two-test pass, correct stronger one-test pass and faulty stronger
one-test intended row AssertionError. The final prose's correct-existing pass claim
does not fill that gap. Original selected hashes/modes and scratch removal are
reported; no retained files were added or changed.

**Skill:** reads the shortened core guide and **the entire advanced guide** for
native `probe_files`/`probe_tests`, including unrelated batch/import-root/diagnostic
sections. No audit implementation or context collector read is recorded. It calls
the audit helper once. The actual probe invokes the existing binary-upload test
method with its inherited fixture, then reads through a fresh connection and uses
native `assertEqual` on all rows. This preserves the actual tested call/acknowledgment.
Both receipt method bindings, endpoint writer and native TestCase.fail identity
are checked. All four phases are captured with native counts **2/2/1/1**, exits
**0/0/0/1**, copied import hashes, no timeout/truncation, original integrity and
scratch removal. No separate artifact is retained. Core and native-probe guide
adoption is evidenced here, unlike the [earlier screen](CON-ARTIST-CORE-GUIDE-MODEL-01-REVIEW.md).

## Separate reconciliation and replay

[Exact-program author replay](results/con-artist-sqlite-01/author-replay.json)
reconciles raw terminal usage/events, frozen installed bytes/modes and complete
unchanged five-file inventories. It extracts baseline's actual Python heredoc and
skill's actual JSON with shell parsing, passes each body unchanged to its native
interpreter/helper in project-local disposable copies, and uses a 40-second outer
deadline. Frozen resources are used, not current future edits. Both programs
reproduce the expected four phase outcomes with intended missing-row assertions;
inputs, retained projects and scratch cleanup reconcile.

An initial review suspected inconsistent backslash escaping in the displayed
binary payload. AST-decoded constants show the fixture and skill probe both use
hex **00ff6e6577**, not literal backslash characters. The
[binary-check replay](results/con-artist-sqlite-01/author-replay-binary-check.json)
records that check and a second unchanged-program execution; no model code was
repaired. Both author attempts are preserved. This resolves that suspicion, not
the baseline's original capture gap. Author replay is not original model output.

## Next improvement target

The different disk/alias/native-fixture workflow is supported, but lower token cost
is not. The model correctly routes to native probes and then loads all advanced
topics. Separating that frequently needed interface from conditional diagnostics
is a concrete next candidate; keep actual fixture reuse, binary/native assertions,
binding and cleanup requirements intact. Do not keep rerunning this task for a
favorable number. Broader real-developer efficiency and hosted release checks
remain unproven; this screen alone changes neither.
