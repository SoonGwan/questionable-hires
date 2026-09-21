# Regression04: input cost, not a new optimization result

2026-09-21. Reuses all 16 original sessions at bundle `0d12dd9`, launch
`c2a0748`, after the [behavioral review](ALL-EIGHT-CURRENT-04-REVIEW.md).
[Exact arithmetic and source hashes](results/all-eight-current-04/input-cost-analysis.json)
come from the existing `analyze_response_costs.compare` function, not a new
profiler or model run. Each original usage profile was checked against its
published measurement: total/input/output counters and recorded response count.
All 16 cells are completed, unique and included. No frozen observation changed.

| Recorded quantity | Baseline | Current | Difference |
| --- | ---: | ---: | ---: |
| Responses | 36 | 39 | +3 |
| Input, cache included once | 582,570 | 704,767 | +122,197 |
| Output | 13,870 | 13,258 | −612 |
| Total tokens | 596,440 | 718,025 | +121,585 |

For input `I = n*f + g`, where `n` is response count, `f` first input and
`g = sum(input_i - f)`, the paired symmetric decomposition gives:

| Task | Baseline/current responses | Count term | First-input term | Later-input term | Output term |
| --- | --- | ---: | ---: | ---: | ---: |
| Editor snapshot | 4 / 3 | −15,180.5 | 367.5 | 956 | 121 |
| Invoice history | 5 / 6 | 15,069 | 550 | 5,165 | 361 |
| Ledger delivery | 4 / 5 | 14,988 | 396 | 35,555 | −960 |
| Refresh ownership | 5 / 6 | 14,873 | 583 | 21,915 | 208 |
| Runner environment | 4 / 5 | 14,791.5 | 445.5 | 4,655 | −105 |
| SQLite audit | 5 / 5 | 0 | 525 | 1,946 | −127 |
| Store scope | 5 / 5 | 0 | 475 | 2,072 | −18 |
| View contract | 4 / 4 | 0 | 364 | 1,686 | −92 |
| Sum | 36 / 39 | 44,541 | 3,706 | 73,950 | −612 |

The four summed terms reconcile exactly to 121,585. They are **not causal
attribution or recoverable savings**. First input includes all initial context,
not just the skill; selected bodies are observed later in tool output. Later
input includes generated work, application source, instructions and valid test
evidence. A shell command is not a model response: tools may be grouped within
one response. Cache, price, process count and elapsed time are separate metrics.

## Which extra work can actually be removed?

Original commands distinguish these mechanisms:

- **Receipt** reads the comparison and preservation implementation before the
  existing-fix guide, then uses the comparison helper with its tree guard. It
  does not invoke the separate preservation helper. This is a large inspection
  difference, but original source output is partly truncated. It does not prove
  that a trust question was unnecessary. The guide already routes ordinary use
  to recipes and says the tree guard removes the need for a second wrapper.
  Earlier read-order/support-routing candidates and repeated ledger tuning are
  documented as unsuccessful; do not add the same instruction again.
- **Hostage** reads the controlled-call implementation and performs a complete
  before-fix run with five genuine assertion failures, unlike baseline's
  after-only run. Current's before output contains 6,523 characters. Those
  observations support test sensitivity; they cannot all be labeled waste to
  manufacture an equal-work savings claim. Required overlap checks and cleanup
  remain intact. Asset source inspection is permitted for actual trust questions.
- **Exorcist** inventories filenames, reads the entrypoint separately, then
  reads the three project inputs. Its four actual child checks are grouped into
  one later response. Baseline also inventories before source inspection and
  runs four checks with different instrumentation. More command records do not
  imply four extra responses or an opportunity to omit native evidence.
- **History** includes unavailable-`python` recovery in both arms and performs
  different native-test coverage. Its baseline has six shell records but five
  responses; current has five shell records but six responses. Counting shell
  calls would reverse the observed response difference. Neither failure is a
  license to remove required consumer/history checks.
- **Editor** combines entrypoint/project reading and has one fewer response,
  but still has a positive later-input term. It is one favorable exposed pair,
  not proof that a universal batching instruction would improve every role.
- **SQLite, Store and Friday** have equal response counts and positive input
  differences. SQLite baseline also violates scope. Compare required work and
  permissions before interpreting equal counts as equivalent execution.

## Decision for further improvement

The latest bundle still has a cost problem. Repeating global compression,
path-discovery wording or read-order hints is not supported by a new mechanism.
The prior [discovery experiment](results/con-artist-discovery-01/README.md) and
[screen03 diagnosis](ALL-EIGHT-03-INPUT-COSTS.md) remain applicable warnings,
not successes superseded by this accounting. Shorter final answers are also not
the principal target: current already emits fewer output tokens in aggregate.

Before another instruction edit or model schedule, investigate a workflow where
the existing automation replaces repeated project-native setup rather than
adding it to a tiny direct task. Predeclare workload selection, include a simple
control where automation may not pay off, and freeze the unchanged skill bundle
before inspecting results. This is a test of the current capability's operating
range, not permission to select a favorable task or omit the adverse eight-role
result. Native provenance, assertion strength, original preservation and both
cost metrics remain required. Keep task selection separate from test outcomes;
do not tune against a supposed held-out case after seeing its answer.

This analysis does not establish that larger tasks improve results, that helpers
will be adopted, or that any cost can be removed without losing evidence. No new
skill capability, release approval or featured/localized graph value is claimed.

한국어: 최신16회 원본 기록을 대조했다. 스킬은 응답3회·입력122,197토큰이 늘고
출력612토큰은 줄었다. 추가 작업에는 수정 전 실패 검증과 도구 구현 확인도
포함돼 전부 낭비로 볼 수 없다. 이미 실패한 압축·읽기 순서 안내를 반복하지
않는다. 다음 검증은 기존 자동화가 실제 반복 설정을 대체하는 작업과 단순 대조를
미리 정해 살펴봐야 하며, 유리한 사례만 골라 전체 성능 향상으로 주장하지 않는다.
