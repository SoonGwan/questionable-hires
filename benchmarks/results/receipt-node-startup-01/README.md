# Node guide transfer: lower cost than prior, small aggregate baseline difference

2026-09-21. Launch `8212a19`; prior Receipt `fcd523c`, current `107a0cf`.
Two related authored synthetic cases × three conditions × one repeat, GPT-6 Astra
medium. All six attempts are retained, with no retries, exclusions, timeouts,
account-limit stop or author replay substituting for original evidence.

- [Frozen protocol](../../RECEIPT-NODE-STARTUP-01-PROTOCOL.md)
- [Detailed review, costs and limitations](../../RECEIPT-NODE-STARTUP-01-REVIEW.md)
- [Final manifest](run.json)
- [Criterion decisions, preservation and capture reconciliation](comparison.json)

All six meet the five explicit criteria under unblinded author review: same four
native tests/startup, actual explicit-zero assertion failure before, four passes
after with supported mechanism, full revisions and native copy-bound identity,
and original-state preservation/cleanup. A completion flag alone is not this score.

| Two-task sum | Input + output tokens | Process seconds |
| --- | ---: | ---: |
| No-skill baseline | 135,053 | 129.242 |
| Prior guide | 188,874 | 131.417 |
| Current guide | 130,151 | 123.673 |

Current versus prior: **−31.09% tokens / −5.89% time**. Current versus baseline:
**−3.63% tokens / −4.31% time**. Ratios of sums, not task-ratio averages. Cached
input counts once; reasoning is not added twice. Shared host/cache, n=1, no causal,
stable or broad performance claim. Plain current costs more than baseline;
preloaded current takes longer than prior. See all six rows in the detailed review.

The exact native-command requirement excludes the comparison helper's observer
flags, even for plain. No cell uses that helper; this is guide/native-routing
evidence, not verification of helper adoption or its runtime savings. Prior reads
preservation support implementation in both cases; current does not. The lower
read/turn count is an observation, not a causal attribution.

## Evidence layout and known capture gaps

Each condition has two cell directories containing the answer, CLI commands/events,
metadata, unchanged final project files, initial/final diffs and source hashes.
`tool-records.json` retains original calls/outputs, including reads missing from
CLI capture. `usage-profile.json` reconciles original response usage with CLI totals.
`skill-exposure.json` publishes entry hashes and observation locations only.

Plain prior/current each has a read-command output at original line 22 missing
entirely from CLI events. Five native outputs are shortened in CLI capture;
current plain matches fully. All CLI outputs uniquely match equal-exit exact
outputs or nonempty suffixes in retained originals. See `comparison.json` for
per-cell mappings and lengths; the missing evidence is not an author replay.
CLI-only command counts undercount work in those two cells.

All four skill sessions contain the exact entry body in initial messages at line
11 and later tool output. Baseline exact-body matching is unobserved, not proof of
total absence. Exposure does not prove that instructions were necessary or caused
the outcome. Private initial messages and complete private rollouts are **not
exported**. Original tool records contain only tool calls/responses. Path/credential
pattern scan passes; this is not a proof of exhaustive privacy detection.

Condition `run.json` files are preparation snapshots. The top-level manifest is
the completed schedule. Resource digests and frozen input hashes were checked
before export. Artifact/HEAD/staged-entry checks agree with in-session preservation
reports; no pre-session binary-index snapshot exists. No claim covers concurrent
or restored changes. No featured pointer or historical chart was changed.

한국어: 기존 안내 대비 토큰은 31.09% 줄었지만 무스킬 대비는 3.63% 감소다. 각
1회의 관련 합성 과제 결과이며 비교 도우미 자체는 사용하지 않았다. 전체 성능
30% 개선으로 주장하지 않는다. 원본 실행 증거와 불리한 결과를 함께 보존했고,
비공개 초기 지시문은 제외했다. 기존 그래프와 실험 수치는 변경하지 않았다.
