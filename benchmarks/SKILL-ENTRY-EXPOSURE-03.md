# Skill entry exposure03 — 2026-09-28

Read-only follow-up to [Hostage scope lean01](HOSTAGE-SCOPE-LEAN-01-REVIEW.md),
previous resource `a2173887`, candidate/execution `333df414`. No new model calls,
solver test runs, candidate, invocation change or performance improvement.

The four original sessions do **not** support treating their first skill read
as a duplicate of an initially supplied full entry. This differs from the
historical [screen03 re-exposure audit](SKILL-REEXPOSURE-02.md); keep both cohorts
attached to their own recorded context instead of generalizing either result.

| Recorded observation | Previous a | Candidate a | Candidate b | Previous b |
| --- | ---: | ---: | ---: | ---: |
| Initial system/developer/user messages inspected | 5 | 5 | 5 | 5 |
| Exact complete entry matches in those messages | 0 | 0 | 0 | 0 |
| Exact body matches after removing YAML frontmatter | 0 | 0 | 0 | 0 |
| First recorded tool call line | 13 | 13 | 13 | 13 |
| Recorded full-entry tool-output line | 17 | 17 | 17 | 17 |

[Original checks](results/skill-entry-exposure-03/original-check.json) retain
session identities, source/event/entry hashes, message line numbers and boolean
matches. `extract_rollout_tools.extract` checked matching CLI/session identity;
`inspect_skill_exposure.summarize` reproduced the frozen exposure records exactly.
All source inputs were hash-checked again after inspection and remained unchanged.
No private message text is exported.

The extra substring check removes dependence on the inspector's exact `<skill>`
wrapper. For each recorded message text block before the first tool call, it
checks `entry in text` and `entry.split('---', 2)[-1].strip() in text`; the latter
body was checked to be nonempty. It does not cover partial, normalized, split-block
or unrecorded context, and does not establish attention or necessity.

The existing public-artifact summary is reproducible without private sessions:

```sh
python3 -B benchmarks/analyze_skill_reloads.py benchmarks/results/hostage-scope-lean-01
```

Its [retained output](results/skill-entry-exposure-03/existing-analyzer.json)
likewise reports no initial exact entry and one full-body tool output per cell.
Raw-session substring verification additionally requires the original local
sessions and frozen local resources; public artifacts alone cannot reproduce it.

The runner already requests `$hostage-negotiator` with its entry path. It does
not pass `--ignore-skills`. Current [official skill documentation](https://learn.chatgpt.com/docs/build-skills)
describes explicit and implicit invocation and loading full instructions on
selection; it does not promise that the initial message contains the body or
quantify the cost of a subsequent file read.

Do not remove that read, subtract its bytes or tool call from measured tokens,
or preload the body only in the experimental arm and call that a shipped skill
improvement. The invocation hypothesis supplies no supported optimization here;
retire it for this cohort without spending another model run. The original
token/time comparison and declined candidate decision remain unchanged.

한국어: Hostage scope lean01의 원본4회를 재실험 없이 확인했다. 첫 도구 호출
전5개 메시지에는 전체 스킬 본문이 없고,17번째 줄의 도구 출력에서 처음 정확히
일치한다. 기존 검사 형식에 의존하지 않는 본문 문자열 확인도 같은 결과다.
부분·변형·미기록 문맥의 부재까지 증명하지는 않는다. 이 실행의 첫 파일 읽기를
중복 낭비로 단정하거나 측정 토큰에서 빼지 않는다. 추가 모델 호출·스킬 변경·
절감 주장은 없으며, 다른 원본 실행에서 확인한 과거 중복 노출은 그대로 보존한다.
