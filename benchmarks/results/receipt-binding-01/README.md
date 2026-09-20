# Receipt binding transfer pilot 01 — reviewed 2026-09-21

Launch `567167d`; old Receipt `ba6fedd`, current `253273d`. Two authored, related
tasks × three conditions × one session, GPT-6 Astra medium. See the
[frozen protocol](../../RECEIPT-BINDING-01-PROTOCOL.md), [frozen cases](../../receipt-binding-cases-01.json),
[author preflight](../../receipt-binding-preflight-01.json),
[all outcomes and evidence paths](comparison.json) and [actual schedule](schedule.json).
All six scheduled sessions completed, no timeout, retry, exclusion or account limit.

## Observed cost — not a general percentage claim

| Loader | Condition | Input + output tokens | Seconds | Responses | Reviewed criteria |
|---|---|---:|---:|---:|---:|
| Dynamic | Baseline | 83,238 | 73.052 | 5 | 5/5 |
| Dynamic | Old Receipt | 90,391 | 65.632 | 4 | 5/5 |
| Dynamic | Current Receipt | 82,963 | 40.593 | 4 | 5/5 |
| Ordinary | Baseline | 66,793 | 70.498 | 4 | 5/5 |
| Ordinary | Old Receipt | 99,461 | 70.419 | 5 | 5/5 |
| Ordinary | Current Receipt | 93,534 | 52.275 | 5 | 5/5 |

Summed over these two tasks: baseline **150,031 tokens / 143.550s**, old
**189,852 / 136.051s**, current **176,497 / 92.868s**. Current versus old is
**−7.03% tokens / −31.74% time**. Current versus baseline is **+17.64% tokens /
−35.31% time**: mixed, not a combined resource win. Cached input is included once;
response-level, cumulative and CLI counters reconcile. These are process wall
times on a shared host/cache, not helper timings, prices or causal attribution.
The synthetic loader pair, fixed order, unblinded review and n=1 per cell do not
establish broad superiority, significance, or achievement of the eight-skill goal.

## What actually happened

All cells run the same four current test identities against both full revisions:
before `341f10beb9c0e0e941c70573c08216ba5fdaaaaa`, after
`f112e2647e333b7b11d0f12471990b6fd0d35748`. These are authored fixture commits.
Before shows the two positive/negative midpoint assertion failures and two passing
controls; after passes all four, with native exits 1/0 and no skips. Each actual
test process checks the bound module's exact copy-local source path. Original
file bytes/modes and final HEAD match, retained pre-collector index entries match
the original HEAD, installed resources are unchanged, and no extra files remain.
Recorded whole-tree guards include Git during comparison and scratch is removed.
Guards do not establish absence of restored changes or metadata refresh before
their start; read-only discovery/status precedes them in these sessions.

Current Receipt uses `compare.py` with `module_bindings`, native unittest invocation
and preservation in **both** tasks. Old Receipt uses custom native comparison code
and `preserve.py`; baseline writes its own inline comparison in both tasks. Thus
the new capability is actually adopted, not merely present. It does not eliminate
source inspection: dynamic current reads 260 helper lines plus supporting guides;
ordinary current uses a focused implementation search. The next cost problem is
remaining exploration/context overhead, not missing native test coverage. Do not
ban necessary trust inspection or retune these exposed tasks to seek better scores.

## Capture and exposure limitations

Original private sessions were retained separately; only reviewed tool records,
usage/exposure summaries, emitted CLI events, commands and project snapshots are
exported. Private initial instruction text is not published. Exact Receipt body
exposure is observed in initial messages and later tool output in all four skill
cells; baseline matches are unobserved, not proof of global absence.

- Dynamic old: stored tool line 23 truncates a large guide/source read (CLI item 3);
  CLI output is 44,527 characters, the truncated stored block is 40,102 characters.
  Do not infer that the model saw the entire CLI source output. This is not the
  native test result. Native command CLI item 5 omits a prefix present in original
  stored line 32; the remaining suffix and exit match.
- Ordinary current: CLI item 5 omits a prefix retained at stored line 38.
- Ordinary old: CLI item 5 omits a prefix retained at stored line 38.
- Ordinary baseline: CLI item 3 omits a prefix retained at stored line 30.
- Dynamic baseline/current command outputs match their stored counterparts.

All other corresponding command outputs and exits match. Full original native
results are available in exported `tool-records.json`; missing CLI prefixes were
reviewed there, without reruns. Capture differences are enumerated in comparison.json.
There are no reconstructed model outputs or replacement attempts.

한국어: 두 과제에서 개선 Receipt는 이전 버전보다 합계 토큰 7.03%, 시간
31.74%가 줄었고 실제로 새 도우미를 사용했다. 하지만 무스킬 대비 시간은
35.31% 줄고 토큰은 17.64% 늘어 혼합 결과다. 여섯 실행 모두 같은 검증을
완료했으며 원본 보존·정리도 확인했다. 직접 작성한 두 연관 과제를 한 번씩
비교한 결과라 전체 우위나 8개 스킬의 목표 달성으로 표현하지 않는다. 출력
누락과 소스 읽기 중 잘림도 보존하고 대표 그래프는 변경하지 않는다.
