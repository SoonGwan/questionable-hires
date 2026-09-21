# Click context audit 01 — adverse cost result

2026-09-21. Launch `d3d94e1`, Con Artist resources `f253f38`, Click
`6aabf099bfdd4c1e75fe8d0e0d4241372b988ab1`. See the
[frozen protocol](CLICK-CONTEXT-01-PROTOCOL.md) and
[original reviewed evidence](results/click-context-01/comparison.json).

| Arm | Reviewed obligations | Total tokens | Wall seconds | Responses | Shell commands |
| --- | --- | ---: | ---: | ---: | ---: |
| No skill | 5/5 | 114,886 | 114.069 | 5 | 4 |
| Con Artist | 5/5 | 181,168 | 172.195 | 6 | 6 |

Skill used **57.69% more tokens and 50.96% more time**. Input includes cached
tokens once; output includes reasoning tokens once. Both completed, neither
timed out. One author-selected real-source task, synthetic mutation, fixed order,
shared host/cache and unblinded review: not a causal or general estimate.

Both identified the upstream test gap: the final nested-resource block never
enters `ctx.scope()`, so its explicit raise satisfies `pytest.raises` without
unwinding the resources. Both used actual copy-local core mutations and native
pytest, preserved source/Git/resources, and removed scratch. Independent checks
confirmed 177 original file contents/modes, unchanged HEAD and staged entries,
and no extra files. Initial binary index bytes were not independently captured;
the models' own before/after snapshots include Git metadata.

Baseline ran three relevant original tests on each variant (3 pass/3 pass), then
one identical added case (1 pass/1 propagation-identity failure). Existing cases
supplied neighboring controls. Its profile records include mutable returned
lists: those values are not entry-time snapshots. Actual exit events, pending
callback counts and added order/identity assertions support the scored claim.

Skill ran the entire 30-test file on each variant (30 pass/30 pass), then four
added cases. The first correct-code run failed all four because it asserted
traceback-object identity across a context-manager wrapper. It disclosed and
repaired that unsupported constraint, checking body traceback inclusion instead.
Final runs were 34 pass correct / 33 pass and 1 actual propagation failure faulty;
all neighboring controls passed. The preliminary failure and full repair cost
are retained, not counted as mutation detection or discarded as warmup. Skill
used 60-second native child deadlines; baseline had only the 360-second cell cap.
Neither adopted a comparison helper. Unequal work prevents treating the entire
cost gap as instruction overhead or attributing a precise saving to any edit.

Original call/output matching reconciles every shell command. One baseline and
two skill CLI outputs are shorter suffixes of the retained original native
records; no replay replaces them. Skill body appears exactly in the recorded
initial message and later read. Baseline non-observation is not proof of absence.
Private initial messages remain local; exported tool records are path-redacted
and pass the evidence scanner. Selected upstream excerpts retain LICENSE.txt.

Decision: no efficiency win, no featured promotion, no release-readiness claim.
A subsequent candidate may narrow assertion design to the requested behavioral
contract, but this pair cannot measure that candidate and is now exposed.

한국어: 최종 감사 결과는 양쪽 모두 요구사항을 충족했다. 다만 스킬 실행은
불필요하게 강한 traceback 동일성 검사 때문에 정상 코드에서 실패하고 복구했다.
더 넓은 검사 범위와 복구 비용까지 포함하면 토큰 57.69%, 시간 50.96% 증가다.
실패 기록도 보존했으며 성능 개선으로 홍보하거나 대표 그래프에 반영하지 않는다.
