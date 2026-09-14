# Optional native evidence retention — 2026-09-15

Parent `b9cb260`; follows [refresh 03](HOSTAGE-REFRESH-03-REVIEW.md). An original
CLI command had empty captured output despite a pass claim. Dedicated commands
alone did not guarantee capture; the upstream omission's cause remains unknown.

## Candidate

Hostage conditionally routes unreliable terminal capture to a
[native evidence recipe](../skills/hostage-negotiator/references/native-evidence.md).
Prefer existing reports; this is not a mandatory extra file workflow for ordinary
tasks. No new runtime/helper dependency or replacement test runner. A subshell
creates a fresh permitted project-local directory, records command arguments,
runs the native command once, writes combined output and exit, then displays
output and returns the recorded exit. Existing evidence is not overwritten.

Reading the retained files can recover the **same new execution's evidence**
without rerunning tests. This does not recover earlier lost output. The recipe
provides no process deadline, child cancellation, input snapshot or tamper-proof
attestation. Existing execution bounds and task ownership remain necessary.
Interrupted runs without an exit file are unverified. Logs are not automatically
committed; privacy, retention rules and no-write task scopes remain explicit.

## Executed author checks

[Tests execute the shipped recipe](../tests/test_hostage_native_evidence.py) with
actual native unittest, under `sh -e`, while deliberately discarding terminal
display. Five tests pass / 0.195s:

- One native passing assertion leaves test identity, count, output and exit 0.
- One actual `42 != 43` assertion leaves its failure and nonzero exit; a local
  execution counter proves each test ran once, with no recovery replay.
- Empty discovery exposes `Ran 0 tests` despite exit 0; this is not a pass claim.
- Missing-command diagnostics and the actual same-context shell failure remain.
- Exit 37 survives a later successful output read unchanged.

Space-containing project paths work; prior owner evidence and test sources are
unchanged. Fresh scratch lives under benchmarks and is removed after tests.
This simulates display loss; it does not reproduce or fix the underlying CLI bug.

Two earlier missing-command test expectations failed: hard-coded 127, then a
comparison with a standalone command. Here `sh -ec` reports 1 for the missing
command in an `if` condition, while standalone `sh -c` reports 127. A minimal
same-condition check confirmed 1. The final test compares the actual same-context
native failure, not an assumed platform code; the explicit exit-37 control
separately verifies the recipe does not collapse application exits to 1.

All 12 bundle tests pass / 3.299s; skill and repository validation pass. These
are local author checks, not model adoption, production reliability or token
savings. No historical measurement/chart is changed. Next model evidence must
check use of retained native output and scope, not merely creation of files.

## 한국어

출력 수집이 불안정하고 파일 생성이 허용된 경우에만 쓰는 방법을 추가했다.
테스트를 한 번 실행해 인자·실제 출력·종료 코드를 새 디렉터리에 남기므로 화면
출력이 빠져도 같은 실행의 기록을 읽을 수 있다. 과거 누락 복원이나 CLI 버그
해결을 주장하지 않는다. 별도 시간 제한·하위 프로세스 정리 기능도 아니다.

화면 출력 폐기 상황에서 성공·실제 단언 실패·0개 발견·없는 명령·종료 코드 37
검사 5개가 통과했다. 기존 증거와 소스를 보존하고 테스트 재실행도 없었다.
셸의 없는 명령 종료 코드를 잘못 가정한 초기 검사 2회는 실패했고 동일 실행
조건으로 검증을 수정했다. 배포 묶음 12개도 통과했으나 모델 채택과 비용 개선은
아직 미검증이며 기존 그래프는 유지한다.
