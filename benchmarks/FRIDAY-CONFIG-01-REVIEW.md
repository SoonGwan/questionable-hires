# Friday configuration transfer 01: reuse, no net efficiency win

2026-09-15 KST. Launch `0723722ba99438f51f39409b0ac4b277485b1318`,
resources `636935e`. [Protocol](FRIDAY-CONFIG-01-PROTOCOL.md),
[all four original-session exports](results/friday-config-01/summary.json).
All scheduled sessions completed, no limits/timeouts/retries. Two newly authored
related configuration variants, n=1 per arm, shared host/cache; not production data.

| Case | Baseline tokens | Friday tokens | Baseline seconds | Friday seconds |
| --- | ---: | ---: | ---: | ---: |
| A: bridge restored | 85,306 | 89,525 | 59.467 | 55.471 |
| B: premature old consumer | 66,455 | 88,962 | 49.018 | 51.554 |
| Sum | 151,761 | 178,487 | 108.485 | 107.025 |

Friday sum tokens **increase 17.61%**; sum time falls only **1.35%**. Both token
pairs regress and B time regresses. Input includes cache plus output once; no
extra reasoning/cache addition. Unequal execution/discovery work and one repeat
prevent causal claims. This is not the requested broad 20–30% improvement.

## What actually transferred

All four read root, ops and worker AGENTS.md before invoking actual versioned
`options()` functions through `runpy.run_path`. They follow manifest-relative
paths, compare exact timeout/attempts values and caller mapping preservation,
and distinguish local evidence from unavailable production reload/network/process
orchestration. Both A answers find a compatible sequence. Both B answers identify
step 4 old/current returning 1000 ms instead of 7500 without an exception, while
the final old/legacy state recovers. These conclusions are in actual native
captures, not just self-reported prose or author replay.

The two Friday scripts reuse identical consumer/config observations. Inspection
of the supplied functions supports reuse here: functions only derive fresh scalar
result dictionaries from the provided mapping, with no global state, effects or
mutations; source/config bytes stay unchanged during each script. This is not a
general license to cache stateful/config-reloading consumers by filenames alone.

| Case/arm | Actual function invocations | Observation mapping |
| --- | ---: | --- |
| A baseline | 7 | Each listed active pairing executes |
| A Friday | 5 | Four unique active pairings; three later occurrences reuse; one extra off-plan old/current call |
| B baseline | 9 | Seven active calls plus two bridge mitigation calls |
| B Friday | 5 | Five unique active pairings; two later occurrences and both bridge mitigation observations reuse |

A Friday's extra old/current call observes the same silent failure outside A's
plan and labels it off-plan, not a false positive. B Friday reuses the earlier
bridge evidence for mitigation rather than claiming a fresh replay of a changed
rollout. No active failing combination is skipped. B scripts print comparisons
and retain failure descriptions despite outer exit 0; no release approval is
inferred from process success. No independent mutation/replay of these witnesses
was performed, and their correctness outside this fixture is not certified.

## Discovery and scope

Both Friday sessions use four commands: hidden discovery, grouped instructions
and manifest, source/config reads, native witness. Baseline A uses four, baseline
B three. Friday avoids repeated Git-object inventory; baseline A lists Git files
again after reading the manifest. Friday A also prints a source diff and reads
unrelated owner notes; Friday B discovers/preserves those notes without opening
them. These work differences remain visible, not attributed to one paragraph.

Neither Friday session reads or invokes the SQL matrix. Correct routing transfers
to actual Python consumers, but no helper performance is measured. The previously
observed fewer reads on the flat pair does not imply fewer calls on this layout.
Fewer trivial Python invocations also do not establish whole-task savings.

## Integrity and decision

Both resource inventories match each other and current candidate bytes/modes;
resource digest matches the launch manifest. Frozen input hash matches the manifest.
All ten supplied project files (including three AGENTS.md and hidden owner notes)
match byte content in all retained/exported projects, with no extra retained scratch.
Friday's reported fifteen non-Git files include the five installed skill resources;
there are ten task-supplied files, not fifteen independent user inputs.

Raw turn usage matches metadata, raw stream matches stored redacted events, public
events and source hashes match originals, and public project file sets are complete.
All fifteen shell commands have nonempty captures and exit 0. A scan finds no local
home/temp paths or key-shaped strings in exports. Raw evidence remains unchanged.

Keep the demonstrated stateless evidence reuse and scoped discovery. Do not pile
more mandatory read rules onto this pair or promote the tiny time difference.
Further work should target a workflow with material repeated execution cost or
missing developer value, rather than another near-identical low-cost config loop.
Whole-bundle efficiency, real-user usefulness and generalization remain unproven.
Historical/featured charts remain tied to their original measurements.

## 한국어

새 설정 과제에서도 양쪽 모두 중첩 지침을 읽고 실제 함수를 실행해 정상 계획과
롤백 중 1000ms 오류·최종 복구를 구분했다. 스킬은 상태가 없는 동일 조합의 근거를
재사용했고, 실제 함수 호출은 A 7→5회·B 9→5회였다. 필요한 오류 조합은 실행했다.

하지만 전체 토큰은 **17.61% 증가**, 시간 감소는 **1.35%**뿐이다. 오류 과제는
시간도 늘었다. 값싼 함수 호출 감소를 전체 성능 향상으로 포장하지 않는다.
새 도우미 채택도 없었고, 작성 예제 2종·반복 1회라 실사용 일반화는 미입증이다.

입력 10개·설치 리소스·원본 사용량·공개용 로그를 대조했고 원본은 보존했다.
같은 작은 과제에 지침을 계속 추가하지 않는다. 다음 개선은 반복 실행 비용이
실제로 크거나 기존 스킬이 개발자에게 제공하지 못하는 가치가 있는 작업을 대상으로
해야 한다. 대표 그래프 수치는 변경하지 않았다.
