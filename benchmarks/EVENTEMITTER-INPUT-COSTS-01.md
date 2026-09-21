# EventEmitter recorded input costs — 2026-09-21

Post-run accounting of the six original attempts launched at `ed74b11`, not new
model execution, improved performance or a revision to their outcomes. The
[review](EVENTEMITTER-BOUNDARY-01-REVIEW.md) still rejects candidate promotion.

Reproduce all conditions, without selecting only a favorable comparison:

```sh
python3 -B benchmarks/analyze_response_costs.py benchmarks/results/eventemitter-boundary-01 --all-conditions
```

[Recorded profile](results/eventemitter-boundary-01-cost-profile.json) retains
source-profile hashes. The analyzer reconciles actual response counters, profile
totals and published comparison totals; cumulative advances are not a substitute.
It rejects missing/duplicate arms and invalid path identities. Existing two-arm
mode remains the default and reproduces the earlier all-eight analysis unchanged.

## Exact accounting, not causal attribution

For each arm, input equals `n*f + g`, where `n` is recorded response count, `f`
first-response input and `g = sum(input_i - f)`. The symmetric paired difference
is `delta_n * mean(f) + delta_f * mean(n) + delta_g`, plus the output difference.

| Task / comparison to baseline | Response-count term | First-input term | Later-input term | Output term | Total difference |
| --- | ---: | ---: | ---: | ---: | ---: |
| Reentrant / prior | 0 | 6756 | 20376 | 22 | 27154 |
| Reentrant / candidate | 0 | 6732 | 21329 | 805 | 28866 |
| Empty event / prior | 0 | 5600 | 9264 | -47 | 14817 |
| Empty event / candidate | 15426 | 6193 | 15954 | 52 | 37625 |

All terms sum exactly to observed total-token differences, cache included once.
These are not billable-dollar estimates, isolated skill-token counts, avoidable
work, latency attribution or recoverable savings. Context may contain required
evidence. A different workflow can change every term, so deleting one response
does not establish savings equal to its arithmetic term.

## What this rules out and what remains worth inspecting

- Reentrant dispatch has six responses in every arm. Removing an extra response
  cannot explain that pair's increase. Nor is final-answer length the main numeric
  difference: output terms are 22 and805 versus total gaps27154 and28866.
- The original command records do not read the optional runtime assets or their
  implementation. Their filenames occur in inventories, which is not a body read.
  Shortening those helpers cannot be credited as solving this observed gap.
- Both skill arms emit their entry plus project source and then read initial test
  and license. These combined calls contain required evidence; whole calls cannot
  simply be classified as waste or their tokens subtracted.
- Reentrant skill arms execute parameterized before-fix suites producing20/21
  failures; original tool output is truncated. Baseline's recorded42-test suite is
  after its edit only. Extra verification and repeated failure diagnostics are
  a concrete difference, but that does not show that before evidence is worthless
  or quantify how many tokens came from it. Candidate also adds a test after its
  first passing run; retain its cost.
- Empty-event candidate has six responses versus five in the other arms. It uses
  three final shell checks in one tool interaction; shell-command count is not
  response count. Do not promise a saved response merely by joining shell commands.

The next plausible implementation investigation is retaining decisive native
failure evidence without repeatedly exposing large diagnostic streams—not another
five-word entry edit or shrinking unused assets. Inspect existing capture support
first. Any compact presentation must retain native test identities, failure reason,
exit, complete raw evidence/provenance and capture limitations; it must not hide
distinct failures or manufacture a repaired transcript. It would still need a fresh
workflow comparison before an efficiency claim. No such candidate is adopted here.

Five analyzer tests pass Python3.9/3.11, including all16 earlier profiles, all six
new profiles, shrinking context and malformed/incomplete comparisons. Production
skills, historic charts and reviewed outcomes remain unchanged.

한국어: 응답 수와 초기 입력·이후 입력·출력의 차이를 원본 카운터로 분해했다.
재진입 과제는 응답 수가 같아 왕복 횟수만의 문제가 아니며, 읽지도 않은 보조
도구를 줄이는 접근도 근거가 없다. 반복 실패 로그의 표시 방식을 조사할 여지는
있지만 이 계산 자체를 절감 가능량이나 성능 개선으로 주장하지 않는다.
