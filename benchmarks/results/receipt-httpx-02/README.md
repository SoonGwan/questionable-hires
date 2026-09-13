# Seeded HTTPX fix: equivalent required checks, substantially higher skill cost

[Protocol](../../RECEIPT-HTTPX-01-PROTOCOL.md),
[pre-model launch correction](../../RECEIPT-HTTPX-LAUNCH-01.md),
[run manifest](run.json), [metadata](summary.json). Launcher `cdef5ec`, frozen
Receipt resources `562c25a` with consolidated entry `f32de37`. Full HTTPX
`26d48e0` checkout plus disclosed authored fault `8ed44f4`, not an organic upstream
incident. One baseline then one skill session, serial, Astra medium; both
completed. No model retries/exclusions, candidate changes or concurrent author
tests during timing. The initial `receipt-httpx-01` preparation failed before any
model call; this successful launch uses a separate retained output directory.

| Arm | Input + output tokens | Process seconds | Shell calls | Before / after |
| --- | ---: | ---: | ---: | --- |
| Baseline | 66,746 | 34.212 | 8 | 1 expected failure + 2 passes / 3 passes |
| Receipt | 107,868 | 72.546 | 4 | 1 expected failure + 2 passes / 3 passes |

Receipt records **+61.61% tokens / +112.05% time**. Cached input is included once
in input; reasoning tokens are not added again. These are complete model-process
observations, not summed test runtimes. The shared host/cache, fixed order and
n=1 do not establish causal overhead or broad performance. There is no previous
entrypoint arm, so this is not a causal compression experiment. It does establish
that fewer shell calls did not produce a saving in this observed pair.

## Reviewed execution

- [Baseline commands](httpx-set-param-fix--baseline--1/commands.json): project
  instruction inventory (no match, exit 1), clean status, exact before pytest,
  focused implementation read, one-line patch, exact after pytest, separate
  focused diff, whitespace check and final status. The no-match search is not
  a test failure. Two empty-output flags are successful clean status and
  whitespace commands, not missing decisive test output.
- [Receipt commands](httpx-set-param-fix--skill--1/commands.json): entrypoint,
  status and base revision batched; a second project instruction inventory with
  before pytest; wider implementation region and test-region read; then after
  pytest, whitespace/diff/status and untracked-file listing in a fail-fast chain.
  No helper/reference is read and no redundant after probe runs. Initial
  semicolon chains do not establish every earlier search status; decisive test
  output is separately visible. The extra test read, wider context, revision and
  untracked inventory differ from baseline's work, despite equal required tests.
- Both captured before runs fail the actual set assertion: expected `?a=456`,
  actual `?a=123&a=456`; add/remove controls pass. Each uses the prescribed
  preinstalled interpreter and identical cache-disabled native pytest command
  again after editing, with all three passing. No dependencies installed, altered
  runner settings, extra test suite or outside-project search is observed.
- Both make the identical one-line `add` to `set` correction in `_urls.py`.
  All 124 other tracked files remain byte-identical to the prepared input. All
  125 final tracked files match original upstream hashes, including `_urls.py`.
  No test methods change. Final answers correctly limit claims to the executed
  checks and reviewed change. No new explicit import-identity assertion is added;
  do not describe this as a separate import-provenance experiment.
- Original and redacted event objects agree under the runner's path substitutions.
  No invalid JSON, error events or rejected patches appear. Skill resource hashes
  match every frozen exported file and its before/after inventories agree;
  baseline skill inventory is empty. Metadata flags alone are not the review.

No author replay of model solutions is used as evidence. The separate fixture
preflight is not included in model timing or credited as their before run.
The three focused tests are not exhaustive HTTPX regression coverage.

## What changes next

Batching is adopted, but this and the [frame pair](../receipt-frame-01/README.md)
do not support cost savings on small fixes with supplied regressions. Do not
keep compressing instructions or adding batching rules as if either guarantees
performance. Reassess task applicability and the missing evidence work Receipt
actually contributes, while retaining current-bug and historical-verification
capabilities. No skill-role restriction is proven by this single task, and
automatic selection was not measured here.

Do not rerun this exposed fixture for a better score or present broad 20–30%
improvement. The all-eight objective remains unmet. Featured images and bilingual
landing-page scores remain tied to their existing experiments.

## Export scope

Commands, events, metadata, answers and diffs are exported for both cells. Only
the relevant final `_urls.py`, `test_url.py` and upstream license are committed
under each `project/`; these selected files are **not a standalone runnable
checkout**. Full final snapshots and original logs remain in the local run.
Use the pinned upstream revision plus disclosed fixture diff to reconstruct the
project. `source-sha256.json` identifies original artifacts, not redacted exports.
