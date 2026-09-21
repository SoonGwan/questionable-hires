# SWE-Lite pilot01: verification cost review

2026-09-22. Analysis of all four original sessions at resource `8ee6c56`,
runner `796926e`; not a new model experiment or skill improvement. See the
[review](SWE-LITE-PILOT-01-REVIEW.md) for native outcomes, environment limitations
and original elapsed times. No frozen result or featured chart changes.

The existing `analyze_response_costs.compare` validates the per-response sums
in each published `results/swe-lite-pilot-01/{project}-{condition}/usage.json`.
All four total-token values also match `review.json`.

| Quantity | Requests baseline/current | pytest baseline/current |
| --- | --- | --- |
| Recorded responses | 9 / 7 | 10 / 11 |
| First input | 12,024 / 12,381 | 12,021 / 12,378 |
| Input including cache once | 163,600 / 131,753 | 238,389 / 267,382 |
| Output | 1,372 / 1,274 | 2,100 / 2,193 |
| Total | 164,972 / 133,027 | 240,489 / 269,575 |

For input `I = n*f + g`, use the existing symmetric decomposition of response
count `n`, first input `f` and later-input difference `g`. These identities are
not causal attribution, removable overhead, billable dollars or timing estimates.

| Current minus baseline | Requests | pytest | Sum |
| --- | ---: | ---: | ---: |
| Response-count term | −24,405 | 12,199.5 | −12,205.5 |
| First-input term | 2,856 | 3,748.5 | 6,604.5 |
| Later-input term | −10,298 | 13,045 | 2,747 |
| Output term | −98 | 93 | −5 |
| Total-token difference | −31,945 | 29,086 | −2,859 |

First input includes the whole initial context. Both current sessions read
Receipt later through tool output, so the first-input difference is not the
Receipt body cost. Later inputs include necessary source, test output and prior
conversation. Shell commands, tool invocations and responses are different counts.

## What the commands support

- Requests baseline makes a malformed diagnostic `python -c` call and repairs
  it on the next response. Current does not. Both read project files, reproduce
  the defect, apply the same implementation change and run neighboring tests.
  Their regression inputs and selected coverage differ. The favorable pair
  cannot establish that Receipt prevents syntax mistakes or causes the saving.
- pytest current spends two further inspection responses locating existing
  skip-location checks before executing its new regression. Baseline locates
  relevant code with fewer response boundaries. This is a candidate for focused
  inspection, not proof those reads were unnecessary: current also extends an
  existing explicit-skip test. Removing that coverage would change the work.
- Both pytest sessions run the broader three-file suite, see the same three
  fixture-induced path failures, and compare those failures with the original
  implementation. Current uses a copied source tree; baseline temporarily
  rewrites and restores the working source. These are not equivalent safety
  procedures or established unnecessary checks. Do not subtract their costs.
- Current reuses the broader after run; baseline additionally reruns the two
  passing files. Receipt already instructs reuse when assertions and runtime
  match. Adding the same rule again is not a newly supported optimization.
- Both current sessions read only Receipt, with no optional helper execution.
  These are current-bug tasks, while Receipt's comparison helpers are routed
  to already-present fixes. Non-adoption here is not evidence of a broken
  route. Forced helper use would add setup without an identified missing need.

## Development decision

Do not add another generic batching, compression or mandatory-helper rule.
The [entry consolidation](RECEIPT-ENTRY-COST-01.md) and
[eight-role accounting](ALL-EIGHT-04-INPUT-COSTS.md) already warn against that
unsupported inference. This review leaves skill instructions unchanged.

Before another timed external comparison, repair and preflight a **new** fixture
version against neighboring tests as well as scored tests. The empty temporary
`pytest.ini` changed nested root discovery; the four completed sessions remain
fixture-confounded even if a future version is fixed. Replays of these exposed
cases can validate environment behavior, not independent model improvement.
Investigate a concrete repeated setup cost before introducing more automation.

한국어: 네 실행의 원본 토큰 합계를 모두 대조했다. Requests는 응답이 9→7회,
pytest는 10→11회였고, 전체 토큰 차이는 −2,859다. pytest의 추가 비용에는
실험 환경이 만든 실패 조사도 포함된다. 이를 낭비로 빼거나 스킬 성능 향상으로
포장하지 않는다. 이번에는 근거 없는 지침 압축·도구 강제를 추가하지 않았으며,
다음 측정 전에 별도 버전의 환경에서 주변 테스트까지 검증해야 한다.
