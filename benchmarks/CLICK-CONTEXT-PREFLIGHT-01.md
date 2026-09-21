# Click nested-resource test gap — author preflight

2026-09-21, parent `5de6b8a`. A new project beyond the repeatedly exercised HTTPX
workloads: [Pallets Click](https://github.com/pallets/click), pinned to
`6aabf099bfdd4c1e75fe8d0e0d4241372b988ab1`. This is an author-selected coverage
investigation in actual upstream source, not an independently supplied issue,
an upstream production bug claim or a model efficiency result.

In `tests/test_context.py::test_with_resource_nested_exception`, the final
`pytest.raises(TestException)` block registers two nonsuppressing resources and
raises the exception without entering `ctx.scope()`. That block never exercises
the registered exit callbacks. Earlier scenarios cover other exception paths.
This finding does not imply the entire suite lacks cleanup coverage.

## Actual controls

`preflight_click_context.py` uses byte/mode-inventoried original source, separate
disposable copies, native pytest and checkout-bound imports. A synthetic mutation
records the pending resource count and changes only a false exit result to true
when an exception is present and more than one resource was registered. This
models erroneous suppression after both nested resources decline to suppress.
It is not a proposed fix. Source/tests in the original checkout are unchanged.

| Variant | Existing context file | Same author three-case check |
| --- | --- | --- |
| Correct | 30 passed, exit 0 | 3 passed, exit 0 |
| Faulty | 30 passed, exit 0 | 1 failed / 2 passed, exit 1 |

The failed case enters actual `Context.scope`, registers two resources, records
reverse-order exit calls with the original exception and requires that exception
to propagate. Faulty output reports both exit calls but `propagated False`; the
native assertion is `(None is RuntimeError('body-failure-sentinel')) == not False`.
Single nonsuppressing resource and nested suppressing resources remain passing
controls. Correct suppressing unwind passes a cleared exception to the outer
resource. These are actual imported Click operations, not a reimplementation.

Run under Python 3.11 with existing pytest 8.3.4:

```sh
python -B benchmarks/preflight_click_context.py --source /path/to/pinned/click
```

The local preinstalled environment was used without dependency installation;
each command has a 30-second limit, disables pytest plugin autoload/cache and
bytecode writes, and selects the copy's `src` via PYTHONPATH. Copy removal and
original bytes/modes including Git inventory were checked. Source is a shallow
clone; no history-origin conclusion is drawn from it. Network is unnecessary for
the native checks. Full command output is returned by the preflight.

## Next decision, not a promised gain

This provides a distinct real-code test-audit candidate for Con Artist. Before
model calls, freeze a neutral user task, success/scope criteria, resource versions,
dependency identity and schedule. Do not give the model the author oracle or
mutant. Require actual correct/faulty runs and cleanup, but allow sufficient
existing evidence and do not force a shipped helper. Compare baseline/current
without tuning instructions to this known answer. Only an observed model failure
or repeated-work cost should motivate the next skill change. Keep performance
claims separate from this author preflight and preserve adverse outcomes.

한국어: 새 공개 프로젝트 Click에서 실제 정리 경로를 실행하지 않는 테스트
구간을 확인했다. 기존 30개 검사는 결함 주입 후에도 통과하지만 같은 보강 검사
3개 중 하나는 실제 예외 전파 오류로 실패한다. 원본은 보존했으며 모델 비교나
스킬 성능 향상 결과는 아직 아니다. upstream 수정이나 이슈 등록도 하지 않았다.
