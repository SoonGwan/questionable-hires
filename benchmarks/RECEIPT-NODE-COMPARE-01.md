# Native Node before/after comparison — 2026-09-21

Parent `310d483`; this implements the integration following the
[load-observation preflight](RECEIPT-NODE-LOAD-PREFLIGHT-01.md), not a model trial.

Receipt's existing collector now accepts `runner: "node"` and `--node`. It reuses
revision/tree/blob collection, frozen current tests/support, selected-original and
optional full-tree preservation, copy cleanup and bounded foreground execution.
Python bootstrap/module behavior retains its existing interface; only subprocess
capture is extracted into a shared function. No second Git/copy/process supervisor
is introduced. The [conditional Node guide](../skills/receipt/references/node-comparison.md)
contains the recipe, exact native invocation and limitations.

## Native evidence

`tests/test_receipt_node_compare.py` uses actual isolated Git repositories, committed
before/after modules and one unchanged current boundary assertion. On Node 24.16.0:

- ESM static import: before `accepted(18)` is false, after true; actual native
  assertion diagnostics retain expected true / actual false. Both discover one
  test. Selected loads have matching source digests inside native processes.
- CommonJS require with working-tree after: before fails and after passes;
  working-tree identity is hashes/modes, not an invented commit.
- A passing unrelated test with no selected load is incomplete (check 7, native
  exit 0) and no after run occurs. Oversize output likewise cannot certify missing
  early provenance. Timeout stops the comparison and removes owned copies.
- Custom Node startup/search/cache settings, Python-only options, nonselected
  paths/flags and varying tests reject. Tests must come from the fixed selection.
- Malformed/unselected load records are exercised with mocked capture; these
  parser controls are not additional native runs.
- The actual JSON-stdin CLI collects before failure/after success with exit 0,
  demonstrating why CLI completion is not itself a claim that tests passed.

Eight integration tests pass under Python 3.9. Each comparison verifies originals
including Git inventory are unchanged and no `.receipt-*` copies remain. No package
installation or model calls. Synchronous hooks must be available; absent runtimes
explicitly skip the native tests rather than implying compatibility.

The complete `test_receipt*.py` group passes **159 tests in 60.507 seconds** under
Python 3.11, including existing Python runner/cleanup regressions and these Node
controls. Fixture-runner model calls in that suite are mocked, not model evidence.
Repository metadata/link checks, skill validation and featured synchronization pass.

## Limits and next performance gate

This provides a previously unsupported automated workflow; it is **not measured
token/time improvement**. No frozen benchmark, criteria, graph or featured pointer
changes. English/Korean capability descriptions now link both supported paths.

The helper is for a project already using native Node tests without required custom
startup flags/loaders, npm scripts or build orchestration. It does not claim Jest,
Vitest, arbitrary Node versions, package-map/transpiler compatibility or production
readiness. A load record is not evaluation, actual function dispatch or test coverage,
and at least one observed load is not coverage of every worker. Original assertion
output remains necessary. Observation is not adversarial attestation or a sandbox.

Before any efficiency claim, freeze a representative native-project verification
task and complete controls, compare current support with the prior skill and an
adequate no-skill workflow, and retain all attempts. Review whether the helper
actually removes manual orchestration without replacing required runtime setup or
weakening provenance/coverage. Added setup and instruction cost must also count.

한국어: Node 기본 테스트의 수정 전후 비교를 기존 복사·Git·보존·실행 제한 코드에
연결했다. 실제 이전 코드 실패/수정 코드 통과와 누락·잘림·시간 초과 처리를 검증했다.
새로운 자동화 기능이지 토큰·시간 절감률 증거는 아니다. npm 등 다른 실행 방식을
대체하지 않으며, 실제 개발 과제를 고정한 모델 비교는 아직 남아 있다.
