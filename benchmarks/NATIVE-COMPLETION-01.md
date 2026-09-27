# Native completion01 — 2026-09-27

Parent `0024be51`; author execution-gate correction, zero model calls. No original
grading outcomes, selected inputs, ordinary skills or featured claims change.

The status/cache prospective driver recorded required-item status satisfaction
separately from execution completion. It wrote reports before owned service-thread
cleanup, and its completion field merely searched stdout for a string. A satisfied
item map therefore did not itself prove completed execution. No previously graded
cell is reclassified as a new failure by this prospective correction.

The next private driver writes the event JSON only after `pytest.main` returns
and owned service-thread cleanup succeeds. It adds an explicit completion boolean
and integer native exit. Its gate requires no parent timeout, actual process exit0
or1, exact matching integer native exit, and completion boolean identity. Unknown,
interrupted, collection-error and missing/contradictory completion records do not
qualify. The original item contract remains separate; a new combined field requires
both item satisfaction and execution completion. A completed pytest1 is still a
test failure, not a passing suite or quality success.

[Executed control](results/native-completion-01/control.py),
[exact extracted gate](results/native-completion-01/execution.py) and
[child command](results/native-completion-01/child.py) retain the implementation.
The child replaces only the issue-package import with a synthetic local
`control_package` carrying an author version string. It asserts the actual local
package path and installed pytest path. This is no real issue bootstrap evidence.

Both actual pytest2.8.7 and4.0.2 run four fresh process controls: one passing test
(exit0, complete), the existing seven-state author fixture (exit1, complete),
missing-file collection (exit4, rejected), and intentionally wrong pytest path
(assertion exit1 with no event file, rejected). Fixture bytes remain identical.
Additional synthetic gate inputs reject timeout, missing completion, mismatched
exit, boolean exit and unsupported exit2. These are gate controls, not actual
timeout/signal/service-cleanup-failure experiments. Runtime plugin limits from
[status capture01](NATIVE-STATUS-CAPTURE-01.md) remain applicable.

[Checkout](results/native-completion-01/checkout.json) and
[Git-free copy](results/native-completion-01/git-free.json) each pass all eight
real process outcomes and synthetic gate inputs. Each native process has a30-second
parent timeout; the Git-free coordinator has60 seconds. Captured stdout/stderr
hashes identify control observations; no selected gold, labels or issue logs enter
these public resources.

[Private driver identities](results/native-completion-01/driver-check.json) show
the cache03 source unchanged and the separate completion04 source syntax-valid.
The prospective external driver remains **unexecuted**. It is not full-cohort
readiness, independent issue-solving validation, all8 quality improvement or
whole-task token/time savings. Full grading/runtime/solver-isolation work remains
necessary before the requested update can be claimed complete.

한국어: 테스트 항목 만족과 실행 완료를 분리했다. 다음 드라이버는 테스트 종료와
정리 후의 JSON 완료 기록·실제 종료 코드·시간 제한을 함께 확인한다. 실제 두
pytest에서 정상 종료와 의도한 테스트 실패는 완료로, 수집 오류와 잘못된 runner는
미완료로 구분했다. 종료1을 테스트 통과로 세지 않는다. Git 없는 복사본도 통과했다.
전체 외부 과제는 미실행이며 모델·토큰·속도·8개 역할 품질 개선 증거가 아니다.
