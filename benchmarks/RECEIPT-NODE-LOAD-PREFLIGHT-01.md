# Native Node comparison: load-observation feasibility, not shipped support

2026-09-21, parent `4d13328`, local Node **v24.16.0**. Receipt's existing automatic
comparison supports Python unittest/pytest; its preservation-only API does not
copy revisions or run a native Node comparison. This is a concrete support gap,
not evidence that JavaScript users are necessarily slow or that a new helper will
improve model costs. No production resource or model benchmark changed.

## Question and implementation boundary

Can an observer record selected module sources inside the native test process
without replacing `node --test` or importing the application ahead of its tests?
The [version-matched Node module documentation](https://nodejs.org/download/release/v24.16.0/docs/api/module.html#moduleregisterhooksoptions)
provides synchronous hooks and preloading through `--import`. The local experiment
in `node_load_probe/hook.mjs` calls `nextLoad`, reports selected URL, process ID,
format and the returned source's SHA-256, then returns the same result. It does
not proactively import application modules or rewrite their sources.

## Native controls

Run `python3 -B -m unittest discover -s tests -p test_receipt_node_load_probe.py -v`.
All **3 tests pass**, covering **12 native Node executions**:

- ESM dynamic import and CommonJS require, each with correct and faulty values,
  each with and without the observer: eight executions. The test sets a sentinel
  before loading its application; the observed application retains that sentinel,
  so this controlled path has not been moved ahead of test setup. Native status is
  0 for value 2 and 1 for value 1 in both conditions. The failing assertion retains
  expected 2 / actual 1; it is not a setup failure. Each hooked execution records
  one application load with matching source hash and the same PID as the actual
  test's behavioral observation. Each native run discovers one test.
- Two wrong-binding executions import another module while watching the selected
  file. Native tests pass, but no selected-module load is recorded. A future
  comparison must call provenance incomplete, not infer it from a green exit.
- Two evaluation-failure executions load the selected source and then throw before
  producing application observations. Native tests fail, but a matching load record
  still exists. **Loading is not successful evaluation or defect reproduction.**

Each invocation checks every fixture file's bytes and directory entries unchanged.
Temporary projects live under `benchmarks/` and are removed by the test harness.
No dependency installation, network access, actual user project execution or model
calls. Tests explicitly skip when Node/synchronous hooks are unavailable; skipped
controls are not compatibility evidence. The preflight removes inherited
`NODE_OPTIONS` only from its child environment to isolate its fixtures. That is not
a production policy to discard user preloads, conditions or instrumentation.

## Integration gates still open

This benchmark-only hook is **not a standalone Receipt helper**. Do not advertise
Node support or speed gains yet. A useful integration must still supply:

1. Identical current tests/configuration in isolated before/after trees, bounded
   historical and working-tree inputs, loaded revision identities and preservation
   and cleanup evidence, reusing existing safe collection rather than duplicating it.
2. An explicit supported native invocation and environment contract. Do not silently
   replace an npm script, test runner, package resolution, custom loader or preload.
   Other Node versions, static import, multiple test workers, package maps and
   transpilers are not established by these simple controls.
3. Separate native assertion outcomes from missing/truncated load records, setup
   errors, evaluation errors and timeouts. A matching source hash proves only the
   observed loader result, not dispatch or full runtime behavior; later hooks or
   reassignment may change what runs. This is trusted-code observation, not a sandbox
   or tamper-proof attestation.
4. Native end-to-end positive and negative controls before any frozen model trial.
   Compare real orchestration work against an adequate project-native workflow;
   helper adoption alone is not a success criterion. Keep author feasibility tests
   separate from model performance evidence and expose extra loading/setup costs.

한국어: Python에 한정된 자동 비교를 Node 기본 테스트로 확장할 수 있는지 먼저
검증했다. 실제 테스트 실행을 유지한 12개 대조에서 정상·결함 판정, 로딩 순서와
소스 출처를 확인했다. 다만 파일을 읽었다는 기록은 초기화 성공이나 실제 기능 실행을
보증하지 않는다. 아직 배포 기능이 아니며 복사·환경 호환성·정리·완전한 비교 실행과
성능 검증이 남아 있다. 그래프와 기존 실험 수치는 변경하지 않는다.
