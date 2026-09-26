# Receipt unittest completion02 — 2026-09-27

Candidate on parent **`3dac549a`**; [exact changed source hashes](results/receipt-unittest-completion-02/source-sha256.json)
identify this working candidate. This extends the
[earlier module-only correction](RECEIPT-NATIVE-COMPLETION-01.md), which remains
historical. No old model result or featured measurement is relabeled.

## Default-path defect and resulting behavior

An actual default bootstrap unittest test prints its body entry then calls
`os._exit(0)`. At `3dac549a`, the wrapper still sees native exit0, reports
`observed`, and executes both comparisons despite the missing completed suite.
The new regression fails before any implementation edit: `observed != incomplete`.
The separate native module path was already corrected at that parent.

The bootstrap now writes its actual completed result into an owned copy-local
observation directory. Its child-only result-path environment value is consumed
before project imports/tests; no global environment setting or additional test
subprocess is introduced. Both unittest modes validate tests/skips/success and
retain `native_exit_code` plus `suite_observation`. Missing completion or conflict
with native exit maps check7/CLI2/incomplete and stops later comparisons. There is
no giant bootstrap command/source string added to result JSON. Native mode keeps
its existing command/import provenance fields.

The actual interrupted default-path control executes only before, not after.
This removes a meaningless later comparison while preserving the actual native
exit0 and body-entry output. An actual failing suite whose shutdown hook masks
exit to0 is incomplete in both modes. Completed empty/all-skipped behavior remains
unchanged: bootstrap check5; native interpreter exits retained. These are coverage
limits, not evidence that a fix passes. No assertion, required ordinary test,
import binding or source guard is weakened.

## Checks performed

- First original bootstrap regression fails against the unchanged parent helper.
- Final Receipt discovery:198 tests, zero failures/skips,65.672s, Python3.11.6.
  Runner-scheduler controls inside that suite use synthetic model callbacks; their
  printed scheduling/usage is not a real model run.
- Separate disposable source copies without repository Git: parent helper's new
  bootstrap regression fails; final17 native controls pass7.564s. Retain
  [both original outputs and selections](results/receipt-unittest-completion-02/).
  These later author observations do not replace the first original reproduction.
- Repository installer copies all8 skills into an isolated temporary destination;
  its read-only comparison reports every resource byte/mode matching. Installed
  Receipt default CLI actually executes ordinary before1/after0 and interrupted
  before-only native0→check7/CLI2. Source trees stay unchanged. Retain
  [installation comparison and controls](results/receipt-unittest-completion-02/installed-checks.json),
  [normal result](results/receipt-unittest-completion-02/installed-normal.json) and
  [interrupted result](results/receipt-unittest-completion-02/installed-interrupted.json).
  This is the repository's local installer, not a cached third-party CLI, global
  install, anonymous remote installation or hosted release.

Configured startup hooks, source layouts, complete/partial fix observations,
real SQLite effects, timeouts, source preservation and copy cleanup remain covered.
Catalog and featured synchronization are checked separately; no featured changes.
The existing suite's simulated empty exit5 is a compatibility control, not an
actual additional Python-version run. Full other-platform/catalog behavior is
not implied by the affected Receipt tests or installation byte comparison.

## Decision and remaining objective

Adopt this concrete correctness fix in both supported unittest paths. Pytest and
Node retain separate contracts; no general runner-completion or adversarial
attestation claim follows. The observations do not prove requested coverage,
post-import dispatch, absence of transient changes or arbitrary external effects.
Tests are trusted; copies/guards are not a sandbox.

No fresh model calls occurred during these controls. We have not measured model
adoption, whole-task token or time reduction, or a comparative quality advantage.
The invalid-control execution reduction is not a percentage saving for developer
work. Integration05 still measures`75183f2f`; native-split02 still measures`6c099d68`.
The owner's all-eight better-work/lower-token/faster-time goal remains unmet.
Distinct relevant model workflows and ordinary controls remain required before
an efficiency claim; do not rerun exposed integration cases until favorable.

한국어: 이전 보강에서 남아 있던 기본 unittest 실행 경로의 중도 종료 오인을
재현하고 수정했다. 두 실행 방식 모두 완료된 결과와 종료값을 확인해 누락·
불일치면 후속 비교를 중단한다. Receipt198개 검사, Git 없는 복사본의17개 검사,
8개 스킬의 격리 로컬 설치 파일 일치와 설치된 Receipt의 실제 정상·중단 동작을
확인했다. 원격 설치·다른 플랫폼·실제 모델 토큰·시간 절감은 아직 입증하지 않았다.
