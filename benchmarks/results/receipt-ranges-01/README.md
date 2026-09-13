# Range comparison: watch adopted, faster time but substantially more tokens

[Frozen protocol](../../RECEIPT-RANGES-01-PROTOCOL.md), [run](run.json),
[metadata](summary.json). Launch revision `073cada`, Receipt resources `cf4c2c0`.
One new authored verification task, selected to exercise explicit original-file
integrity requirements; not an organic bug or independent broad confirmation.
Serial baseline then skill, Astra medium, n=1, no retry/exclusion/candidate edits
or concurrent author tests while timing. Both cells completed.

| Arm | Input + output tokens | Process seconds | Shell calls | Native outcomes |
| --- | ---: | ---: | ---: | --- |
| Baseline | 52,040 | 58.267 | 3 | Before: 2 assertion failures + 5 passes; after: 7 passes |
| Receipt | 74,827 | 34.965 | 4 | Before: 2 assertion failures + 5 passes; after: 7 passes |

**+43.79% tokens / −39.99% process time.** Cached input counts once within input;
reasoning output is not added again. This is a time/token tradeoff, **not accepted
overall efficiency**. Shared host/cache, order, n=1, targeted synthetic selection
and different extra work prevent causal attribution or an all-eight gain claim.

## What actually ran

[Baseline commands](uncommitted-ranges-fix--baseline--1/commands.json) read
instructions/current files and build a native comparison script. That script
snapshots every existing file/symlink including Git internals, creates two
project-local copies containing implementation and unchanged current tests,
checks the imported implementation path within each test process, explicitly
checks discovery count seven, and executes native unittest. It reports actual
touching/bridge AssertionErrors before and seven passing tests after. It removes
owned copies and checks full original bytes/types/permissions/inventory equality
(24 files including Git). No missing-interpreter repair or failed shell command.
Two native test children, no per-child timeout; outer cell timeout remains.

[Receipt commands](uncommitted-ranges-fix--skill--1/commands.json) read the entry
and complete reference, then current implementation/tests/draft, diff and tracked
file listing. The fourth command directly invokes `compare.py` with working-tree
after and **`watch: [drafts/release.txt]`**, then batches diff/check/status with
individual exit statuses. No helper source read, custom integrity wrapper,
global TMPDIR override, rerun or launcher-file repair is observed. The helper
captures both seven-test native outputs and same-process copied imports. Its
structured report supplies original hashes/modes, unchanged status and cleanup.
Required integrity reporting is reused rather than reimplemented.

Both before runs fail specifically on touching and bridge expectations, with
five passing controls; both after runs pass all seven unchanged tests. Both
identify before commit `f0e4d86a49a4d6d2d1e7cbc3453070fa3adae517` and working
SHA-256 `6755f97b1e89dea7470b55322c46528b715e1c77cc8efbaaccea12e37149746b`.
The three requested originals have captured unchanged byte/mode evidence.

## Preservation and limits

- Both final exports contain exactly the five initial project files, with bytes
  equal to committed-plus-working fixture input. Both agent `changes.diff` files
  are empty; `initial.diff` retains the supplied fix, not credited to either arm.
  No original edits, commits, stash/reset, installs or external actions observed.
- Installed skill inventories are unchanged before/after and hashes match the
  frozen candidate. Baseline has no installed skill. No invalid JSON, empty tool
  output, rejected patches or helper timeout/truncation flags appear. Reviewed
  command outputs include the decisive native assertions and integrity records;
  automatic diagnostics alone are not a full-capture guarantee.
- Baseline's whole-file/Git snapshot and explicit count check exceed the requested
  three-file integrity report. Skill checks selected originals plus Git status,
  not all Git bytes. Both preserve final project originals, but extra verification
  work is unequal. Skill also performs more discovery/diff/listing calls and loads
  skill/reference instructions. These observations do not isolate the cause of
  either cost difference or prove removing a particular instruction saves tokens.
- The new child-temp default is active in helper code; these in-memory native
  tests do not independently exercise tempfile behavior. Local author tests cover
  that path; absence of a launcher artifact here is not universal prevention proof.

## Development consequence

Actual watch/report adoption now demonstrates that the wrapper can be eliminated
in a model workflow. The token increase is substantial and remains a failing
efficiency dimension; lower elapsed time alone does not meet the user's goal.
Prioritize instruction/context loading and unnecessary preparation next, preserving
required behavior. Do not rerun this exposed case for scores or infer improvement
against the different graph task. Confirm on separate realistic tasks and retain
the all-eight gate. Historical results and featured/localized charts are unchanged.

Post-run author validation: full repository suite **350 tests pass (49.804s)**;
catalog/local documentation and featured synchronization checks pass. Export
scan finds no unredacted home or macOS temporary-root paths. These checks do not
replace the original model observations or establish performance superiority.
