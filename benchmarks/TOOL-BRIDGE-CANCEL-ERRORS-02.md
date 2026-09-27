# Bridge cancellation errors02 — error checkpoint, 2026-09-28

Parent `875564d9`; preserves the [failed original controls](TOOL-BRIDGE-CANCEL-ERRORS-01.md).
The isolated [adapter](results/tool-bridge-cancel-errors-02/server.py) records a
bounded native exception diagnostic and checks pending cancellation before
rethrowing an ordinary helper error. The serialized gate, non-abandoned worker,
source guard and native helper stay unchanged. No ordinary skill, model permission,
MCP registration or deployed resource changes.

## Fixed controls

[Controller](results/tool-bridge-cancel-errors-02/control.py) reuses the exact owned
six-test fixture from errors01. Three scheduled cases, no retries:

- Timeout plus cancellation: one before phase, timeout, terminal native PID and
  removed copies; no original modification; same-session recovery after author reset.
- Guard failure plus cancellation: one before phase; intentional owned source
  modification detected and logged; canceled client response; session survives.
- Guard failure without cancellation: before and after phases; ordinary tool error
  must still expose the guard failure. Cancellation handling must not swallow it.

All three require explicit author restoration of the deliberately faulty fixture
before same-session native recovery: before1/after0, six tests/no skips, seven
complete v3 observations each, original preservation and copy cleanup. Record
listener terminal exit codes. Reject a duplicate-response diagnostic. Preserve all
outcomes, including failures, with source identity before interpreting results.
The already-executed fixture's real negative/positive native assertions are reused;
this is not a new independent validation case. A changed adapter motivates this
execution, not a retry of an unchanged candidate.

한국어: 이전 실패를 보존하고 오류 경로의 취소 전달만 수정한 격리 시제품이다.
시간 초과+취소, 원본 보호 오류+취소, 취소 없는 원본 보호 오류를 검사한다.
의도적으로 바꾼 테스트와 원본은 작성자가 복구한 뒤 같은 연결에서 재검사한다.
이 검사는 자동 원본 복구, 모델 승인 통과, 토큰 절감이나 공개 배포 증거가 아니다.
