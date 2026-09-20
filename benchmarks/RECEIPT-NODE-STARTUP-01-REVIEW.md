# Node guide transfer 01 — reviewed checkpoint

2026-09-21. Launch `8212a19`; prior resources `fcd523c`, current `107a0cf`.
See the [frozen protocol](RECEIPT-NODE-STARTUP-01-PROTOCOL.md). All six original
sessions completed with no timeout/account limit. Unblinded author review of
original commands, native outputs, answers and preserved artifacts meets all five
explicit criteria in each cell. This is two related authored cases × one repeat,
not an independent holdout or evidence of a broad 20–30% performance gain.

## Recorded cost and outcomes

Tokens count input (cached input included once) plus output. Seconds are process
wall time, not CPU time or isolated helper runtime. Shared host/cache; no dollar
estimate. Responses come from retained original session usage records.

| Case | Condition | Tokens | Seconds | Responses | Original shell outputs |
| --- | --- | ---: | ---: | ---: | ---: |
| Plain | Baseline | 66,234 | 53.816 | 4 | 3 |
| Plain | Prior | 94,602 | 66.308 | 5 | 5 |
| Plain | Current | 73,970 | 56.402 | 4 | 4 |
| Preloaded | Current | 56,181 | 67.271 | 3 | 2 |
| Preloaded | Prior | 94,272 | 65.109 | 5 | 4 |
| Preloaded | Baseline | 68,819 | 75.426 | 4 | 4 |

Two-task sums: baseline **135,053 tokens / 129.242 seconds**; prior **188,874 /
131.417**; current **130,151 / 123.673**. Current versus prior: **−31.09% tokens,
−5.89% time**. Current versus baseline: **−3.63% tokens, −4.31% time**. These are
descriptive sums, not confidence intervals or stable/causal savings. Plain current
still costs more than baseline; preloaded current is slower than prior. Do not
present the 31% prior-version reduction as a no-skill improvement.

## Original evidence and scope

Each comparison runs the same four tests, reports explicit-zero actual 3 versus
expected 0 before with three neighboring passes, then four passes after; native
exits 1/0. Full Git revisions and copy-local native test-bound origin/PID are
observed. Preloaded commands keep the required unchanged bootstrap; no cell
substitutes a setup failure for a defect assertion. Explanations keep unspecified
inputs out of scope. Files/modes, notes, HEAD, staged entries and skill resources
remain unchanged; owned scratch is gone. In-session preservation inventories
include Git metadata over their stated interval, not a pre-session binary-index
snapshot or protection against restored/concurrent changes.

Prior uses `preserve.py` in both cases; current uses it in plain and a handwritten
inventory in preloaded. Both baselines use handwritten inventories. Neither skill
condition invokes the Node comparison helper. **The exact-command requirement
excludes its added observer flags even on plain.** Thus this pair evaluates guide
reading/native routing, not ordinary comparison-helper adoption or execution-cost
improvement. Do not infer that the helper optimization goal is verified.

Prior reads the preservation guide and implementation in both cases. Current
plain reads the preservation guide but not its implementation; current preloaded
uses only the Node guide before its native workflow. Fewer observed reads/turns
are consistent with lower recorded token cost, not proof of causation. Both skill
conditions use 30-second native child deadlines; baselines rely on the external
360-second cell deadline. Workload is tiny and cannot establish timeout robustness.

## Capture reconciliation and remaining publication work

Original sessions, complete tool records, usage and exposure inspection records
are retained privately under `benchmarks/local-runs/receipt-node-startup-01/`.
The native executions were not replayed to repair capture. All CLI shell outputs
uniquely match equal-exit exact outputs or nonempty suffixes of stored originals.
Plain prior/current each have a complete read-command output at original line 22
missing entirely from CLI events. Counting only CLI commands would undercount
their work. Five cells have shortened native CLI output; current plain matches
fully. Complete original outputs retain the missing prefixes and source identities.
The prior count-equality checker stopped on this discrepancy; the local review
now preserves unmatched originals explicitly rather than pairing by position.

Public artifact export/privacy scanning and final exposure synthesis remain
pending. Do not export private initial messages. No featured pointer or graph is
changed, and the earlier adverse Node experiment remains unchanged. Retain this
guide candidate for further validation, not as a general release-performance claim.

한국어: 수정 안내는 이 두 합성 과제에서 기존 안내 대비 토큰 31.09%, 시간 5.89%
감소했다. 하지만 무스킬 대비는 각각 3.63%, 4.31% 감소에 그친다. 모두 요구사항을
충족했지만 각 1회이며 비교 도우미 자체는 사용하지 않았다. 전체 스킬의 30% 개선,
인과관계 또는 배포 준비 완료로 주장하지 않는다. 원본 증거 공개 준비는 남아 있다.
