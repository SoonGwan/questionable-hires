# Uncommitted fix: correct core comparison, optional helper not adopted

[Frozen protocol](../../RECEIPT-UNCOMMITTED-01-PROTOCOL.md), [run](run.json),
[metadata](summary.json). Revision `47f41ea`, Receipt resources `75c8718`,
one new authored settings-parser task. Baseline then skill, serial Astra medium;
both completed with no retries, exclusions, candidate edits or concurrent author
tests. This is not independent all-eight or organic real-repository evidence.

| Arm | Input + output tokens | Process seconds | Shell calls | Required test outcomes |
| --- | ---: | ---: | ---: | --- |
| Baseline | 70,492 | 66.622 | 3 | Before: 2 intended failures + 3 passes; after: 5 passes |
| Receipt | 76,898 | 68.874 | 5 | Before: 2 intended failures + 3 passes; after: 5 passes |

Receipt records **+9.09% tokens / +3.38% time**. Cached input is included once;
reasoning output is not double-counted. Shared host/cache, order, n=1 and differing
work prevent causal conclusions. There is no observed efficiency win.

## Actual workflow

[Baseline commands](uncommitted-settings-fix--baseline--1/commands.json) read
requirements/source/current tests and HEAD, then implement a native comparison
script. It copies the current project without Git into two project-local folders,
replaces only the before parser with HEAD bytes, runs both unchanged five-test
suites and separately executes import/binding checks plus all five sample inputs.
Its explicit expected-value map and direct sample executions add work beyond the
native suite. Four Python child executions, no per-child timeout. Logs, hashes,
input observations, report and both copies are retained as 23 extra files.

[Receipt commands](uncommitted-settings-fix--skill--1/commands.json) read the
entrypoint **and historical procedure**, including the new working-tree selector.
It nevertheless writes its own native comparison, not a `compare.py` invocation.
It freezes current tests/support/samples and copies the two implementations into
a project-local TemporaryDirectory. Separate import-provenance and native-suite
processes run per copy, each with a 30-second timeout. It checks fixed bytes in
copies before/after, collects final diff/status/whitespace results, checks original
bytes and modes including Git/installed resources, and removes owned copies.
Four child comparison processes plus a Python-version subprocess. No helper
implementation read, helper output or new selector adoption is observed.

Both actually capture the token-padding and query-value AssertionErrors on HEAD,
with the three required controls passing; both capture all five passing on current
implementation. The same current tests and sample data are used across each pair.
Import paths are verified in separate processes from unittest, not in the same
test execution; baseline also checks the test's parser binding in its probe.
Do not relabel these as the helper's same-process provenance behavior.

## Preservation, limitations and capture

- All **nine initial non-Git files** in both final snapshots match the combined
  committed-plus-working fixture bytes, including unrelated notes and untracked
  current checks. Both have the same initial-tree identity. No commit, stash,
  reset, original implementation edit, dependency install or outside-project
  discovery is observed.
- Baseline leaves copies/evidence; skill leaves no extra files. The frozen cleanup
  criterion is not met by baseline. The task/instructions say “disposable copies”
  but do **not explicitly command end-of-task deletion**; this task/criterion
  ambiguity limits interpretation. Keep both the criterion and observation rather
  than rescoring it. No cleanup-based superiority percentage is claimed.
- `initial.diff` retains the input patch. Baseline's `changes.diff` contains only
  its added evidence/copies; skill's is empty. Neither is credited with writing
  the already-present fix. Smaller diff is not inherently better performance.
- Original/redacted event objects match under intended substitutions (12 baseline,
  16 skill). No invalid JSON, rejected patches or empty-output flags appear.
  However, the skill's long final command output starts at before import evidence:
  earlier printed revision/hash/runtime headings are **missing in original events**.
  Native before/after test outputs remain visible. Do not reconstruct that missing
  prefix from final prose or an author replay. Final revision/content identities
  match prepared inputs, but the missing printed records remain a capture limit.
- Installed resources match frozen/current bytes and before/after inventories;
  baseline has no installed skills. No author replay of model solutions is used
  to replace captured evidence. Local preflight remains separate author validation.

## Development consequence

The new helper capability is CLI-tested but **not adopted in this model run**.
Native fallback is allowed, so non-adoption alone is not a task failure. It means
this pair cannot demonstrate the helper removing hand-built comparison work.
Why the model chose native code is not established by the trace. Improve the
optional workflow's usability/discovery and test transfer on separate tasks;
do not mandate a helper solely to make its adoption score look better or rerun
this exposed task for favorable numbers. Broad efficiency remains unproven.

All original adverse results and featured/localized charts remain unchanged.
Exports include both full small final projects and the baseline's retained
artifacts. `source-sha256.json` identifies original files, not redacted export bytes.
