# Real HTTPX JSON comparison: native preflight, model execution pending

2026-09-15; repository parent `ddd7c5d`. This is one new task, not another replay
of the eight-task lean screen. It uses actual HTTPX source at
`26d48e0634e6ee9cdc0533996db289ce4b430177` and the original encoder change
`9fd6f0ca6616d0310a3ee0b0c6ef509a97995797` against parent
`8e36f2bc685dfbe43cd7503bc1c422a6ed6e05a5`.

[Task builder](httpx_receipt_json_case.py) requires identical current native tests,
configuration and package support while varying only `httpx/_content.py`. This
is deliberately not a reconstruction of two full historical dependency environments.
The model must inspect actual revision changes, preserve the project, retain real
failure values/exits and establish copy-local HTTPX/encoder imports in the native
test process. No native network requests, installs or production modifications.

## Actual controls

[Preflight](httpx-receipt-json-01-preflight.json) runs the five selected existing
upstream tests through Receipt's unchanged helper, using an already-installed
interpreter/dependencies. Current tests exercise public Request/Response paths,
not a rewritten JSON encoder. In both variants the same native project conftest
and pytest configuration execute. The normal empty-content control passes;
before has four actual failures (length/format, Unicode, separators, non-finite
values), after passes all five. No timeouts, skipped cases or output truncation.
NaN fails first in the original combined NaN/infinity test; do not claim its later
infinity checkpoint was reached in that failing before test.

The preflight verifies exact source identity, same-process imports, complete output,
source hashes/modes for all 125 tracked files, original preservation and owned-copy
cleanup. Final verbose output exposes observed length `19` versus expected `18`,
escaped versus preserved Unicode, compact-body differences and `DID NOT RAISE`.

## Discovered helper limitation, preserved initial attempts

The [first preflight](httpx-receipt-json-01-initial-preflight.json) included
`tests.test_content` among provenance imports. Receipt imports these before
launching pytest; this suppresses pytest assertion rewriting for that module.
The expected four failures still occur, but some have no useful actual-value diff.
This is a real usability problem with preimporting test modules, not a failed fix
or a model result. It merits a focused helper regression and correction.

The [second preflight](httpx-receipt-json-01-rewritten-preflight.json) verifies
only the required HTTPX package/encoder imports and lets pytest load its tests.
Unicode/format diffs return, but `-q` abbreviates the header comparison. Final
preflight uses `-vv`, as the task now specifies. It passes the same native
positive/negative controls with detailed values. Original inputs/assertions are
never weakened; initial attempts remain available. The local interpreter path in
the final public observation is replaced with `<PREINSTALLED_PYTHON>`.

## Next action and limits

No model session has run and no skill performance claim follows. Before comparing
models, address the observed pytest preimport behavior in isolation without
weakening copy provenance, then freeze resource revisions and a no-retry schedule.
The source task is real upstream code, but author-selected and development-visible;
it is not independent production-user evidence or a broad all-eight evaluation.
Existing shipped entries and featured charts remain tied to their measured sources.

한국어: 실제 HTTPX 수정 이력과 원본 테스트 5개로 새 검증 과제를 준비했다.
같은 현재 테스트/지원 코드에서 수정 전 4개 실패·1개 통과, 수정 후 5개 통과를
확인했다. 테스트 모듈을 먼저 import하면 pytest의 상세 실패 출력이 사라지는
도우미 제약을 발견했고, 초기 결과도 보존했다. 모델 실행 전 이 제약부터 회귀
검사로 고쳐야 한다. 이번 결과는 스킬 성능 향상 수치나 실사용 전체 검증이 아니다.
