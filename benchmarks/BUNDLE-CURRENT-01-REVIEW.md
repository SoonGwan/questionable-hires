# Current bundle regression review

Frozen evaluation aeb582b; see BUNDLE-CURRENT-01-PROTOCOL.md. Original logs live
privately under `local-runs/bundle-current-01/`. The original serial runner finished
all 18 sessions with exit 0. This is a one-repeat exposed regression, not a superiority claim.
No model restart, changed skill, altered criterion or author replay.

## First three reviewed cells

- Persistence baseline: original source/test preserved. Isolated missing-append
  mutation leaves the original test green; actual stored-record probe fails on
  mutant and passes after restoring the copied implementation. Temporary copy is
  removed. The captured harness command includes an initial original-test run and
  assertion, but its initial printed result is missing from otherwise nonempty
  output. Later mutant/probe outputs and final successful harness assertion/status
  are captured. Do not reconstruct the absent original-test output or equate empty
  diagnostic flags with complete capture. Four shell commands; no process deadlines
  inside the isolated child runner.
- Protected search baseline: two deterministic completion orders pass against the
  actual generation guard; no defect manufactured. Only test_search.py is added,
  original search.py unchanged. Owned tasks are cancelled/gathered, but the test's
  queue waits themselves have no explicit timeout. Four shell commands; captured
  unittest output records two passes. No extra deadline criterion is added.
- Boundary fix skill: actual age-18 assertion fails before the one-line >= fix,
  then the unchanged assertion passes in the three-test suite. Final suite,
  whitespace check and focused diff are collected with fail-fast && and exit 0;
  there is no separate redundant targeted after-run. Five shell commands. Changes
  are limited to eligibility.py and the new age-18 regression in its existing test.
  This observes Receipt's collection behavior, not a causal or bundle efficiency win.

Original captured commands for these cells stay scoped. The two diagnosis/audit
cells' input bytes match the frozen fixtures. Receipt's installed resource hashes
match frozen Git and before/after manifests agree; baseline has no installed skill.
No patch rejections, malformed JSON, empty-output flags or event errors in metadata
for these three cells, subject to the concrete missing-output limitation above.
Remaining cells and paired cost comparisons still require review.

## Next three reviewed cells

- Search diagnosis skill: actual Search and transport execute sequential, overlapping
  in-order and overlapping reversed scenarios through a recording dependency.
  Captured output demonstrates stale overwrite without cache; final answer explains
  why no-cache does not prevent ordering races and preserves production uncertainty.
  Only a rerunnable probe is added. Async signal waits and cleanup have cooperative
  timeouts; no separate process deadline or helper is added. The exercised fixture
  has no cancellation-suppressing implementation. Six shell commands; no optional
  reference/source read or separate result-file round trip. Initial broad listing
  includes in-project .git names before loading the skill. Inputs/resources match.
- Formatter baseline: source-grounded review recommends replacing the unused USD-only
  registry with a plain formatter while preserving the formatting expression.
  Three read commands, no runtime checks or changes, and no claim of executed tests.
  The supplied requirements and actual consumer support the scoped recommendation.
  All three original inputs match.
- Persistence skill: two disposable module copies preserve compilation/import context;
  actual imports are verified in each. Original tests pass on correct/mutant code;
  the same stronger test passes correct code and fails missing append with the
  expected exact-store assertion. It includes a preexisting record and distinct
  object identities. Six child invocations each have a 15-second timeout. All child
  outputs/statuses are captured, originals match and copies are removed. Four shell
  commands; no helper/reference read. Claims about detecting other write faults
  follow from the assertion, not additional executed mutations. Five frozen skill
  resources match and before/after manifests agree.

No capture flags or patch rejections in these three metadata records, and recorded
commands stay scoped. Partial persistence pair: baseline 79,283 tokens / 43.468s;
skill 69,285 / 43.480s. Tokens are about 12.6% lower, time essentially equal, but
skill checks deeper store identity/import/deadline behavior and baseline has the
initial output omission noted above. This is neither equal-work causal measurement
nor whole-bundle acceptance. Search diagnosis skill is 71,216 tokens / 52.128s;
formatter baseline is 62,296 / 22.229s; their partners still require review.

## Two search QA skill cells

- Protected search: five shell commands; only qa_search.py is added. The retained
  probe executes actual Search with sequential and reversed-overlap scenarios,
  submitted-query assertions, cooperative waits and a five-second parent process
  deadline covering cleanup. However, the original command executing the probe
  has exit 0 and **empty captured output**, despite the probe's explicit flushed
  PASS prints. Record this capture limitation, not independently observed scenario
  output. No author replay is credited. Production diff is empty. Metadata reports
  that empty item, no patch rejection and unchanged installed resources. Cost is
  67,822 tokens / 48.219s versus baseline 63,822 / 40.442s; this pair is not a win.
  Baseline checks two overlap orders whereas skill checks sequential and reversed
  overlap with a process deadline: the work is not identical.
- Broken search: five shell commands; only test_search_qa.py is added. Actual
  controlled futures exercise in-order and reversed completion after both requests
  start. Captured unittest output records two tests and one exact stale-result
  assertion failure; the subprocess wrapper exits 1 for that failure, not timeout.
  The answer correctly treats it as a reproduced defect, supplies the five-second
  external deadline command, and limits the claim to Python state, not browser UI.
  Original production/requirements diff is empty. No capture flags or rejected
  patches, and installed resources unchanged according to metadata. Cost is
  85,260 tokens / 57.670s. Baseline partner still needs trace review.

These reviewed commands stay inside their allocated projects. Retained probe
design, successful command exit, and directly captured assertion output are
different evidence levels and must not be collapsed into an unconditional pass.

## Remaining cells and paired evidence

- Formatter skill: two read commands versus baseline three; initial listing includes
  .git before loading the skill. Same source-supported simplification, preserving the
  formatting boundary and expression. No execution, modifications or invented test
  claim. The shorter workflow is observed, not proof that the skill caused it.
- Rolling schema, both arms: four shell commands each, actual SQLite and reader
  queries identify incompatible old/new schema pairings and rollback ordering.
  Captured failures are expected missing-column results. Skill also inserts and
  preserves a post-migration row through down migration; baseline retains only its
  initial row. Skill does not read the optional matrix helper or inspect history;
  baseline runs git log. Both leave originals unchanged. This is unequal coverage.
- History, both arms: three shell commands each and executable current caller proof.
  Skill additionally uses blame and historical patch d5fc972, checks empty and normal
  display_name, and preserves the active fallback. Baseline preserves it too but
  does not inspect/cite history, so it misses that frozen criterion. Do not recast
  the simpler question as requiring history to reach the correct recommendation.
- Boundary baseline: four commands; unchanged age-18 regression actually fails
  before the fix and passes in the three-test suite after. The final command uses
  semicolons rather than fail-fast collection, but the actual unittest output is
  captured and green. Skill adds one shell command and stronger command collection;
  both perform the requested scoped fix and meaningful red/green verification.
- Broken search baseline: five commands and one deterministic reversed-order test.
  Captured failure is the actual stale-result assertion, not harness failure.
  Skill additionally checks normal order and bounds execution; baseline's controlled
  waits lack deadlines. Both leave production unchanged and reproduce the defect.
- Search diagnosis baseline: three commands, retained experiment calls actual Search
  and transport through a recording dependency. Both overlap completion orders and
  actual no-cache request assertions are captured. No wait deadlines/owned cleanup;
  skill additionally has a sequential case and bounded cooperative cleanup. Original
  sources unchanged. Baseline's grouped command final exit is not by itself probe
  success; actual printed assertions/completion provide the positive evidence.
- Necessary state: baseline four shells, skill seven. Both implement the same per-form
  pending guard and try/finally behavior, preserve return/error identity, and execute
  success, duplicate, retry, failure and cancellation checks. Baseline uses an inline
  probe with unbounded waits; skill retains three unittest regressions with controlled
  waits/cleanup. Skill's extra discovery includes an empty AGENTS-only search, another
  listing/source read, then a separate requirements read. Do not attribute all extra
  cost to test depth: fragmented discovery is also directly visible. Both changes
  are authorized; final skill wording describes button state via the supplied Python
  contract, not an independently tested rendered UI.

All 18 original input comparisons match except the authorized eligibility/test edits
in both boundary cells and form.py edits in both state cells. All 29 installed
resource entries match frozen Git SHA-256 and before/after manifests. No metadata
patch rejections, malformed/non-object JSON or error events were reported. The
protected-skill empty output and persistence-baseline partial output remain explicit
limitations; these checks do not prove every tool byte was captured.

## Costs: all nine pairs, no exclusions

Total tokens = input + output; cached input is already included. Seconds are each
session's process wall time. No dollars, confidence intervals or causal claims.

| Case | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| history-active | 62,608 | 67,657 | 23.062 | 30.493 |
| boundary-fix | 79,262 | 84,189 | 27.625 | 32.854 |
| formatter-review | 62,296 | 49,366 | 22.229 | 23.912 |
| search-order | 80,424 | 85,260 | 44.349 | 57.670 |
| search-diagnosis | 63,801 | 71,216 | 40.011 | 52.128 |
| necessary-state | 63,486 | 85,352 | 31.420 | 55.313 |
| persistence-test | 79,283 | 69,285 | 43.468 | 43.480 |
| rolling-schema | 79,763 | 68,171 | 34.369 | 34.481 |
| search-protected | 63,822 | 67,822 | 40.442 | 48.219 |
| **Sum** | **634,745** | **648,318** | **306.975** | **378.550** |

Skill total tokens are **2.14% higher** and summed time **23.32% higher**. None of
the nine skill sessions is faster in this sample. Three use fewer tokens, but
extra evidence and capture limitations prevent treating costs as equal-work causal
comparisons. The whole-bundle efficiency objective remains unmet. Earlier adverse
results are not replaced by this run.

Next optimization target: state-task discovery fragmentation after skill loading,
while retaining regression tests and return/error/cancellation correctness. Inspect
the current instructions before changing them; do not remove useful checks or add
a task-specific script merely to improve this exposed fixture's score. No candidate
was changed or model session retried during this evaluation.
