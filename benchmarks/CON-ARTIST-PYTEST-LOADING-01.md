# Con Artist: preserve the native pytest lifecycle

2026-09-20, parent `9c0c458`. Implementation/native-regression checkpoint; no new
model run, efficiency claim or featured-chart change.

Review of all eight shipped entries and the [all-eight original observations](results/lean-screen-01/README.md)
did not justify promoting the prior lean rewrite. Inspecting audit support revealed
a concrete execution limitation: listed modules loaded before pytest configuration
and collection. The old guide worked around assertion rewriting by asking agents
not to list test modules, but implementation modules can also require configuration.

## Demonstrated failures and correction

Five initial actual-pytest tests against the old helper produced three failures:

1. A collected test module in `imports` lost the `assert 19 == 18` diagnostic.
   The mutant still failed, but only a bare `AssertionError` was retained.
2. A correct implementation requiring `pytest_configure` environment setup failed
   at premature import; the audit was incomplete before any behavioral check.
3. `--version` returned `observed` rather than an incomplete baseline, despite no
   native test session verifying the requested behavior.

Failed-precheck and escaped-import negative controls already passed. The change
runs native pytest configuration/collection first, then verifies copy-local imports
and the precheck in `pytest_collection_finish`, before fixtures/test bodies. Setup
failures retain reserved exits 6/7 and stop the audit. A successful-looking exit
without the verification hook becomes incomplete. Native collection failures and
explicit `--assert=plain` keep their own meaning.

Unittest and inline probes retain direct import/precheck execution. Inline probes
do not gain pytest configuration/fixtures implicitly; the guide routes those needs
to native file probes or test replacements. Prechecks still cannot establish later
fixture rebinding. No dependency install occurs inside the helper.

Seven new tests verify native diagnostics, configuration order, missing-session
handling, failed prechecks, escaped imports, import `SystemExit(0)`, and explicit
plain assertions. Each checks original bytes/modes and scratch removal. Existing
pytest replacement tests retain parametrized/autouse fixtures, native assertions,
collection-error handling and correct-baseline reuse boundaries.

## Validation actually run

Python 3.11.16 / pytest 8.3.4. Initial targeted run: five new tests, three failures
against old code (0.602 seconds). After correction: those five plus the three
existing native replacement tests pass (8/8, 2.944 seconds). Two additional
negative/policy controls were then included in full discovery.

Full discovery ran 693 entries in 114.072 seconds: **691 passed and two module-load
errors**, because this isolated environment lacked declared dependency PyYAML.
After installing PyYAML 6.0.3, the omitted issue-form tests pass 2/2 (0.038 seconds)
and source-archive workflow test passes 1/1 (0.277 seconds). Thus 694 actual tests
are covered across these runs, with no skipped tests; this is **not one green
full-suite invocation**. Preserve the initial dependency failure rather than
reporting 693/693 passed. No model sessions were launched: printed benchmark
scheduler events in unit tests are mocks.

Repository validation, the skill validator, diff whitespace and featured
synchronization checks pass. The environment is under ignored local runs;
global Python packages and model settings are unchanged.

This removes a real setup/diagnostic limitation, not evidence of reduced model
tokens. New-task model comparison is still needed. The remaining roles have not
been rewritten merely to shorten their entries; broad performance remains unproven.

한국어: 8개 진입 지침과 기존 실행 기록을 점검한 뒤, Con Artist에서 pytest 실행
순서 문제를 재현했다. 설정 전에 모듈을 읽어 정상 코드가 실패하거나 상세 실패 값이
사라졌고, 버전 출력만으로 검증이 완료된 것처럼 처리되기도 했다. 실제 설정·수집
이후 출처·사전 검사를 수행하도록 수정하고 원본 보존·정리와 실패 분류를 검사한다.
이는 기능 개선이며 전체 토큰·시간 절감 성과는 아직 아니다. 대표 그래프는 유지한다.
전체 실행은 691개 통과·의존성 누락으로 모듈 로딩 오류 2개였고, 의존성 설치 후
누락된 실제 검사 3개가 따로 통과했다. 단일 전체 실행 성공으로 표시하지 않는다.
