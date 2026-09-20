# Screen03 input-cost diagnosis — 2026-09-20

Measured resources `ee5eb28`; analysis added after `71ced52`. This reuses the
[sixteen original sessions](results/all-eight-current-03/README.md), not new
executions or an improvement result. No frozen artifact is rewritten.

Reproduce with `python3 -B benchmarks/analyze_response_costs.py
benchmarks/results/all-eight-current-03`. The analyzer requires recorded response
usage (not inferred tool calls), reconciles all counters and the published
comparison, and emits source hashes. Three tests include inconsistent/missing
record rejection, a shrinking-context example, and all sixteen retained profiles.

## What increased

| Recorded quantity | Baseline | Current | Difference |
|---|---:|---:|---:|
| Responses | 34 | 36 | +2 |
| Input tokens, cache included once | 551,873 | 667,325 | +115,452 |
| Output tokens | 13,152 | 12,645 | −507 |
| Total | 565,025 | 679,970 | +114,945 |

Shortening the final answer is not supported as the primary intervention. Six
of eight pairs have identical response counts and still use more tokens. Nor is
eliminating two responses alone an adequate explanation of the observed increase.

For each arm let `n` be response count, `f` first-response input, and
`g = sum(input_i - f)`. Then total input is exactly `n*f + g`. The symmetric
decomposition of the input difference is
`delta_n * mean(f) + delta_f * mean(n) + delta_g`.

Summing paired terms gives **30,682.5 response-count term + 28,125.5 first-input
term + 56,644 later-input term − 507 output = 114,945 total difference**.
These are arithmetic terms, **not causal attribution or recoverable savings**.
First input contains all initial instructions/context, not just the skill. Later
input includes earlier generated work, observations and required evidence.
The decomposition neither aligns semantically equivalent steps nor assumes that
all additional work is unnecessary. Cache, price and latency are different metrics.

## Concrete observations and next implementation boundary

- Receipt uses four responses in both arms. Its current second command prints
  35,515 output characters, including the full comparison helper source. Its
  later-input term is +19,039. This is a candidate context-growth contributor,
  not a token estimate for that command. The existing guide already permits
  focused implementation inspection for trust questions. Do not remove evidence
  requirements, forbid necessary inspection, or resume tuning its exposed ledger
  task just to obtain a favorable result.
- Con Artist uses four baseline versus five current responses. In the current
  arm, the first filename-glob search emits only 46 characters and misses the
  actual test/implementation paths. The second command rereads the skill and
  lists the directory; the third inventories hidden paths and reads application
  files. The neutral task describes roles but supplies no paths. This is an
  observed speculative-discovery detour, separate from the subsequent valid
  mutation and same-process binding checks.
- Hostage adds a response and performs different test construction. Do not
  classify its entire additional work as waste or remove required transitions.

The next instruction experiment should target **path-unknown audit discovery**:
use one project-local filename inventory to locate tests/configuration before
guessing filename synonyms, then trace only unresolved bindings. Keep direct reads
when paths are supplied. Evaluate on a different realistic project/task, with a
known-path control; preserve all test provenance, assertions and permission scope.
Compare original/current candidate with contemporary no-skill baseline, freeze
criteria first, and retain any extra work or adverse result. Do not launch another
unchanged screen03 or claim that this proposed change already saves a response.
No production skill edit or model call is part of this diagnosis.

한국어: 기존 16개 실행을 재분석했다. 출력은 507토큰 줄었지만 입력은
115,452토큰 늘었다. 8쌍 중 6쌍은 응답 횟수가 같아 추가 왕복만의 문제도 아니다.
Con Artist는 경로가 없는 요청에서 추측성 파일명 검색 후 다시 목록을 찾는
우회가 관찰됐다. 다음 후보는 이 탐색에 한정하고 새 과제와 알려진 경로 대조로
검증한다. 계산 항목을 원인·절감 가능량으로 주장하지 않으며 실제 검증이나
필수 소스 검토를 생략하지 않는다. 이번 분석 자체는 성능 개선 결과가 아니다.
