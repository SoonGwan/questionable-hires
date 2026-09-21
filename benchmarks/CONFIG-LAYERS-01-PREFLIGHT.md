# Configuration-layer native preparation — 2026-09-21

Selection was committed as `e004fdf` before native execution; skill resource is
fixed at `e1e1ef8`. [Selection and limitations](CONFIG-LAYERS-01-SELECTION.md),
[runnable fixture](config_layers_cases.py),
[all original author observations](results/config-layers-01-preflight.json).
No model session was launched. This is a small authored, correlated single/four
request pair, not an upstream transfer or independent benchmark.

The original four-method native unittest suite passes on correct code. The
declared mutations were not replaced after seeing outcomes:

| Independent change | Original suite | Added native assertion |
| --- | --- | --- |
| Reverse layer priority | 4pass, exit0 | 5methods,1failure: region `us` versus `ap` |
| Discard false/zero/empty values | 4pass, exit0 | 5methods,1failure: supplied values versus defaults |
| Alias defaults rather than copy | 4pass, exit0 | 5methods,1failure: changed input mappings versus their originals |
| Accept absent override | 4methods,1failure, exit1 | Not needed or executed: `None` versus3 already detected |

The stronger file appends one actual unittest method without changing existing
assertions. It passes all five methods on correct code. Shared observation reuse
is recorded with direct references, not claimed as extra independent executions.
The single request uses4 native checks; the four-fault request uses9. Those counts
are author-helper behavior, **not baseline/current model comparisons**.

Fresh-process public import succeeds. Every actual check records copy-local
module paths/hashes and verifies the test module's `resolve` binding in the same
process. All captured outputs are complete and have no timeouts. Owned scratch is
removed; original bytes/modes/inventory remain unchanged. Failure reports retain
the actual differing values rather than a bootstrap exception.

Four fixture controls verify real benchmark workspace materialization, native
outcomes, separate request maps and relative-interpreter rejection. Python3.11.16
passes4/4 in0.833s. Python3.9 also passes4/4. There is no third-party dependency.
Repeated unit-test execution is compatibility checking, not extra model attempts.
Fresh source archive`d844ede`, without Git history or local-run artifacts, also
passes all four fixture controls on Python3.11.16 in0.781s, with no skips.

The fixture contains author answer controls outside the task's supplied files;
model projects receive only `settings.py` and the original `test_settings.py`.
Both tasks have the same files and differ only in requested mutations. They may
choose direct facilities or a helper. No runtime/artificial setup cost was added
to favor automation. The new non-adjacent cache is not isolated by this task: the
same stronger assertion suffices across survivors, so any observed model outcome
must be attributed only to the compared complete workflow, with limitations.

Before execution, freeze the runner identities, actual resource digests, runtime,
criteria and four-cell one-attempt order. Preserve every attempt and both cost
metrics. Native preparation cannot justify changing featured charts or claiming
the user-visible efficiency target has been met.

한국어: 사전 고정한4개 결함 중3개는 기존 테스트를 통과했고1개는 검출됐다.
추가한 네이티브 단언은 정상 코드에서 통과하고 살아남은3개 결함을 실제 값
차이로 검출했다. 파일·권한·실행 연결·정리를 확인했으며 모델 실험은 아직
시작하지 않았다. 작성자 제작 개발용 대조이고 전체 성능 향상 증거가 아니다.
