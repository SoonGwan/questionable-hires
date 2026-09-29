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

## Reviewed execution

Frozen source **`d0cefc47`**; [results](results/tool-bridge-cancel-errors-02/results.json),
[control output](results/tool-bridge-cancel-errors-02/control-reading.txt) and
[identity](results/tool-bridge-cancel-errors-02/identity.json). All three scheduled
controls pass on the first execution, controller exit0. SDK environment remains
Python3.11.6/MCP1.30.0/AnyIO4.15.1, same helper and native interpreter as errors01.

Timeout retains actual native−9/timed_out, one before phase and unchanged originals.
Canceled guard retains native before1, the deliberate `windows.py` modification,
and `NATIVE_FAILURE` with `Selected originals changed; not restored: windows.py`.
It does not launch after. Uncanceled guard retains both native phases1/0 and an
ordinary `isError` response carrying that same guard failure. Neither scenario
silently restores the source or credits the intentionally corrupted call as repair.

All three wait for native PID termination and copy removal before the explicit
author fixture reset. Each then completes a native before1/after0 recovery on the
same initialized session. These six reviewed recovery processes run six tests each,
no skips, seven complete v3 argument observations each:42 records total. The four
fault-phase process events are lifecycle evidence, not additional repair proof.
The ordinary guard-error pair's native1/0 does not override failed source protection.
Every listener exits−15 after awaited termination; no duplicate-response diagnostic
appears. No model calls, ordinary installation or hosted release occur.

The observed errors01 guard/session failure is repaired in this changed adapter.
This is narrow SDK evidence, not a claim about arbitrary crashes, hard kills,
abrupt client loss, cross-instance ownership, RPC deadline compatibility or token
savings. The separate model approval gate remains unresolved and must not be
bypassed. This prototype therefore remains outside the ordinary installed skills.

한국어: 첫 실행의3개 검사가 모두 통과했다. 취소된 보호 오류는 진단을 남긴 뒤
취소로 끝나며 연결이 유지된다. 취소 없는 보호 오류는 실제 도구 오류로 전달된다.
원본 변경을 자동 복구한 것은 아니다. 작성자가 의도적 결함을 원복한 뒤 같은 연결에서
3번 재검사했고,6개 네이티브 과정/42개 실제 인자 기록과 정리 상태를 확인했다.
기존 실패는 errors01에 그대로 남긴다. 모델 토큰·전체 작업 성능·공개 배포 증거는 없다.
