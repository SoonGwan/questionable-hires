# Recorded skill body loading audit — 2026-09-28

Parent`1be35120`. Read-only review of24 existing original sessions using the
existing `inspect_skill_exposure` and `extract_rollout_tools` utilities. No new
model call, skill instruction, global setting or permission change. Exact entry
hashes match each pinned resource and original cell metadata.

| Historical checkpoint | Reviewed sessions | Exact body before first tool | CLI version |
| --- | ---: | ---: | --- |
| Model-choice01, Astra/Sol,resource`6701069f` | 16 | 16 | 0.157.1 |
| Receipt guard-output01,resources`1b6ae5f5`/`a77e4d93` | 4 | 0 observed | 0.157.1 |
| Con Artist guard-output01,resources`1b497a05`/`96ac17f4` | 4 | 0 observed | 0.157.1 |

[Observations](results/skill-loading-01/observations.json) retain exact thread/source
hash, entry hash, original record lines, phase and CLI version. Private initial
message content is not exported. Exact full later entry reads are observed in23 of24; the remaining session
already has the initial body.
For Con Artist, the exact entry hash is identical across these older/recent
checkpoints, so rewritten entry text cannot explain its exposure difference.
This does not imply that complete tasks, resources or host conditions are equal.

The existing runner already prepends `Use $<skill>` and its in-project path for
skill arms. Missing explicit invocation is therefore not the demonstrated cause.
An observed exact structured initial body is stronger evidence than a catalog
mention. Missing matches are unobserved, not proof that no equivalent instruction
was ever present; reading a body does not establish attention, necessity or use.
No parser repair or workaround is justified by this inspection alone.

Official [skill documentation](https://learn.chatgpt.com/docs/build-skills), opened
2026-09-28, describes initial metadata followed by selected full-body reading and
explicit `$skill` invocation. The [Astra guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
recommends focused descriptions and task-dependent supporting references. Neither
source establishes why these recorded sessions differ or guarantees fewer tokens.
The repository already retains adverse compact/conditional-entry experiments;
those results are not overridden by general documentation advice.

Decision: do not invent an eager-loading switch, remove normal rules, or subtract
recorded skill-reading costs. Use a contemporaneous no-skill arm for the changed
deployed bundle and inspect actual exposure for every new cell. The
[integration07 protocol](ALL-EIGHT-CURRENT-07-PROTOCOL.md) implements that measurement
boundary; it is still an exposed development screen, not independent validation.
This review changes the next measurement decision, not the deployed capability
or an efficiency claim. Historical results remain at their measured resources.

한국어: 원본24개를 확인한 결과 같은 CLI 버전에서도 과거16개는 첫 도구 전에
본문이 제공됐고 최근8개는 그 방식의 본문 제공이 관찰되지 않았다. Con Artist
본문 자체는 같으며 명시적 `$스킬` 호출도 이미 사용한다. 원인은 미확정이다.
공식 문서만으로 절감을 보장하거나 설정을 우회하지 않고, 현재 묶음의 미적용
대조군을 같은 실행 조건에서 다시 측정한다. 비공개 지시문은 공개하지 않았다.
