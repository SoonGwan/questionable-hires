# Short Friday guide: actual adoption, mixed cost result

2026-09-14, launch `37686ac`, resources `ce82fcb`.
[Frozen protocol](FRIDAY-CORE-GUIDE-MODEL-01-PROTOCOL.md);
[retained evidence](results/friday-core-guide-model-01/).
One fresh skill-only Astra medium session, exposed rolling-schema task, no retry.

The model completed in **89,545 tokens / 54.127s** (88,237 input + 1,308 output;
cached input included once), four shell calls. It read the shortened core guide,
not the details file or printed implementation. It used the public API with
literal reader references and reused one matrix result for full value assertions.
No custom extraction, second SQL loop or standalone evidence file was added.

Compared with checkpoint 07's 109,377 tokens / 45.151s, recorded tokens are
**18.13% lower**, time **19.88% higher**. This is not a win on both axes. Earlier
code/resource changes, n=1, shared host/cache and unequal extra assertions prevent
attribution to the shorter guide. Document-size arithmetic is not model speed.

## Original observations

Item 5 captures the complete matrix JSON, four phase names, all eight actual
reader outcomes, columns, row values, truncation flags and static query provenance.
The same program checks `complete`, phase count, intended missing-column errors,
successful columns/rows and unchanged hashes of all six release files, then prints
its success marker. No observed initial execution error or decisive capture gap.
The initial filename scan still unnecessarily lists Git internals; these are
inside scope, not needed release evidence. No invented application-writer or
staging execution is claimed.

The model correctly identifies both migration-first rollout and old-binary-first
rollback incompatibility. It distinguishes schema reversal from restoring old
values: the new insert and changed value survive down, alongside an untouched row.
It proposes compatible schema staging or coordinated quiescence instead of calling
an untested rolling release safe. Application/runtime/staging evidence stays unknown.

Raw terminal usage, normalized events, installed resource hashes and all original
file bytes reconcile. No project files are added or modified. Model output uses
the smaller guide without needing the relocated conditional details in this task.

## Separate unchanged-program control

[Author replay](results/friday-core-guide-model-01/author-replay.json) extracts
the actual model Python program from its captured command, without rewriting its
assertions. Original source/recipe and original matrix output are retained.
Each execution is in an owned project-local temporary copy with a 20-second bound.

- Original release passes and reproduces the exact captured matrix observations.
- Appending a deletion of the newly inserted row to down.sql fails the original
  value assertion. The AssertionError retains actual rows `(1, 'Updated by new
  schema'), (2, 'Unchanged')`, exposing the missing new row, not a setup error.

Only the copied down migration changes for the fault. All supplied/copied inputs
remain unchanged during each execution; original retained files stay untouched.
This control establishes sensitivity to that data-loss fault, not every migration
hazard. It cannot replace original output or add production-readiness evidence.

No skill changes or new model retry are made after reviewing this result. Existing
featured charts and all adverse observations remain unchanged. All-eight general
developer gains remain unproven; this screen demonstrates usable shorter guidance
and result reuse, with a real time regression in the historical comparison.
