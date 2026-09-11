# Current nine-case paired regression

Freeze shipped resources and `fast-cases.json` at `eca8921`. No changes to source
skills, cases, criteria or runner during execution. This is the existing exposed
development regression set covering all eight skills, not a confirmation set or
a fresh population. Preserve the original adverse chart and all earlier runs.

Nine tasks, two arms, one fresh Astra medium session per cell: 18 total. Serial,
240 seconds per cell, seed 20260911, no cell retries/exclusions. Invoke run.py
separately per scheduled cell so order is explicit; each output includes run.json.
Stop after incomplete execution or account limits; retain attempted failures.

| Pair order | Case | First | Second |
| --- | --- | --- | --- |
| 1 | history-active | baseline | skill |
| 2 | boundary-fix | skill | baseline |
| 3 | formatter-review | baseline | skill |
| 4 | search-order | skill | baseline |
| 5 | search-diagnosis | baseline | skill |
| 6 | necessary-state | skill | baseline |
| 7 | persistence-test | baseline | skill |
| 8 | rolling-schema | skill | baseline |
| 9 | search-protected | baseline | skill |

Same fixture task and permissions in both arms; explicit skill invocation adds
only the installed skill prompt/resources. Use unchanged criteria. Inspect original
commands, outputs, artifacts and installed resource hashes against the snapshot.
Separate correct outcomes from missing scope evidence, setup failures, timeout
containment and verification depth. Author replays must be labeled separately.

Report input-plus-output tokens (cache already in input), process seconds, all
cells and per-case outcomes. A lower aggregate does not override a failing
required behavior/control or missing evidence. One repeat and unequal work do not
establish causal or stable superiority. This run checks the combined candidate
against a contemporary baseline; it does not measure automatic routing, every
optional helper, realistic cross-repository transfer or independent confirmation.

Raw ignored destination: `local-runs/fast-paired-02/<case>-<arm>/`. Do not change
the candidate while observing results or repeat this set until a desirable score
appears. Diagnose any regression from retained traces before further changes.
