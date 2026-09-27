# Con Artist final integrity evidence01 — 2026-09-28

Parent **`1b497a05`**. Following the ordinary
[Receipt repair](RECEIPT-GUARD-EVIDENCE-01.md), source inspection found that
Con Artist also discarded completed observations when its final selected-file or
project guard raised. A batch RuntimeError additionally discarded earlier audits.
The existing [project guard](AUDIT-PROJECT-GUARD-01.md) detects changes; this change
preserves diagnostic evidence when that guard fails. No model was called.

## Contract and limits

After at least one collected native result, a final integrity failure attaches
incomplete evidence to the original exception's `audit_result`. The direct API
keeps its exception type/message; CLI keeps exit2 and the original stderr
diagnostic, and additionally emits incomplete JSON. Errors before observations
keep their existing behavior. Native checks retain their actual output and exit
values; unexecuted phases are absent. Unreached/unavailable guard fields are null,
detected changes are false, and scratch removal is checked rather than assumed.

Batch results retain earlier audits and references to shared successful baselines,
without counting reused output as new execution. Later mutations stop and
`unrun_mutations` reports their count. RuntimeError and first-audit input/I/O errors
still raise; later ordinary input/I/O errors retain the existing incomplete-return
contract. Interruptions are not swallowed. No restoration, retry or child-process
sandbox is introduced. This does not recover results a runner never returned,
prove arbitrary descendants stopped, or isolate concurrent project changes.

## Native verification

[Regression tests](../tests/test_audit_guard_evidence.py) execute real unittest and
stronger-probe subprocesses in author-owned temporary copies. The original
positive assertion accepts values1/2/3; the stronger assertion actually fails with
`AssertionError: 2` or `3`, preserving the observed value. Deliberate original
edits affect only temporary fixtures and remain changed until author cleanup.

[Before](results/audit-guard-evidence-01/before.txt): seven intended regression
assertions fail because evidence is missing; nine existing guard tests pass.
Importing the fixture class initially caused those nine existing tests to be
discovered too; switching to a module import removes duplicate discovery without
changing the seven assertions. [After](results/audit-guard-evidence-01/after.txt):
all seven pass. Covered failures: selected originals, unselected project files,
timeout plus mutation, direct RuntimeError, unreadable final inventory, second
batch integrity failure and later-batch OSError. The batch control confirms the
third mutation never runs and reused baseline checks point to the first audit.

Two subsequent API compatibility controls verify batch RuntimeError still raises
with previous observations and first-audit OSError still raises with the batch
envelope. [Nine controls](results/audit-guard-evidence-01/after-final.txt) pass.
[Git-free source archive](results/audit-guard-evidence-01/archive.txt): all180
methods from21 helper/guard/recipe/native-invocation/cache/pytest test modules pass,
without skips or repository history. These are native tests, not model evidence.

A final controlled retained-scratch case checks that removal is false when the
directory still exists; the author cleans it afterward.
[All ten controls](results/audit-guard-evidence-01/after-cleanup-control.txt) pass.
This last test was added after the180-method archive run and is not counted in it.
[Source identity](results/audit-guard-evidence-01/identity.json) records parent and
changed source hashes. English/Korean capability text is synchronized. Frozen
featured measurements and charts are unchanged.

No token or timing improvement is claimed. More informative error output can
itself cost tokens; whether it avoids additional investigation remains unmeasured.
The all-eight quality/token/time goal remains unmet. Installation and public
download delivery are separate from these source checks.

한국어: 최종 보호 검사 오류로 이미 실행한 근거가 사라지는 문제를 수정했다.
실패·원래 API 예외·확인하지 못한 항목을 유지하고, 배치의 다음 변형은 중단한다.
수정 전 재현7개가 통과했고 Git 이력 없는 소스의 관련 검사180개도 통과했다.
추가 임시 폴더 잔존 검사까지 새 검사10개가 통과했다. 네이티브 정확성 개선이며
모델 토큰·시간 절감이나 전체8개 목표 달성으로 해석하지 않는다.
