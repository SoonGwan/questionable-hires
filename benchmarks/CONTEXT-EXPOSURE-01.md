# Recorded skill exposure — 2026-09-15

Post-run inspection of six retained sessions, **no new model calls**.
[Machine-readable evidence](context-exposure-01.json) contains session/source
identities, line positions, catalog names and exact skill-body hashes—not private
instruction text. `inspect_skill_context.py` verifies the rollout matches its CLI
thread before examining messages before the first recorded tool call.

| Frozen screen | Conditions | Exact entry already injected before first tool |
| --- | --- | --- |
| view-contract-01 | original / candidate | Both |
| sqlite-debit-01 | original / candidate | Both |
| sqlite-debit-02 | original / candidate | Both |

Each matching `<skill>` user-message body is byte-identical to that cell's frozen
entry. The later command reading `SKILL.md` is **not its first recorded exposure**.
In view-contract-01, the first command lists files, the second rereads the entry
and project inputs, and the third executes the review. Thus a theory that entry
guidance could not affect the first command because the file was opened later is
contradicted by the original messages. The existing discovery clarification remains
unmeasured; this inspection neither proves nor disproves its performance effect.
Do not remove host-required file checks or assume all repeated reads are avoidable.

## Disable requests versus recorded catalogs

All six historical metadata files say `disabled_personal_skills: 9`. That value
was simply the number of discovered paths placed in CLI disable requests. Their
recorded initial catalog still names the target hire and six other entries:
imagegen, openai-docs, plugin-creator, skill-creator, skill-installer and lazy-doodle.

**Catalog presence is not proof of executable availability or failed policy
enforcement.** This audit does not attempt those skills or change host settings.
It establishes only that requested path counts do not certify an empty unrelated
catalog/context. Prior reports saying personal skills were disabled should be
read with this qualification, not as verified removal of every provider entry.
These six cells do not establish what all historical sessions contained.

Future `run.py` metadata uses `personal_skill_disable_requests` and
`personal_skill_disable_verification` with explicit unverified status. CLI requests
and permitted execution remain unchanged. Historical metadata, measurements and
charts are not rewritten. This is an additive interpretation audit, not new
performance evidence or a reason to silently discard unfavorable cells.

## Validation and boundaries

Four synthetic-record tests verify exact initial injection, later-body exclusion,
wrong-revision rejection, session-identity rejection and absence of private text
in the summary. Runner tests retain the same sandbox/persistence/config arguments
while checking that requests are no longer reported as verified removals. Export
privacy checks remain relevant; full rollouts stay in ignored local storage.
All **32 focused tests pass**: 27 runner / 2.882s, four context / 0.005s and one
export-privacy / 0.008s. These are local checks, not hosted CI or model gains.

The inspector recognizes the observed explicit wrapper, not every possible host
context mechanism. A missing match is not proof that unrecorded context was absent.
It measures neither tokens attributable to injection nor the benefit of eliminating
a reread. Further optimization must preserve the actual host's applicable rules
and compare complete equivalent tasks, not change benchmark controls to win.

한국어: 기존 세 실험의 여섯 세션에서 스킬 본문이 첫 도구 호출 전에 이미 정확히
주입돼 있었다. 나중에 파일을 읽은 시점이 최초 노출 시점은 아니었다. 따라서
“본문 안내가 첫 조회에 영향을 줄 수 없다”는 가정은 원본 기록과 맞지 않는다.
또 비활성화 9개라는 기존 필드는 요청한 경로 수였고, 초기 목록에는 다른 항목
6개가 남아 있었다. 목록에 보인다는 사실만으로 실제 실행 가능 여부를 단정하지
않는다. 새 메타데이터는 요청과 검증 상태를 구분하며, 기존 수치·그래프·원본은
보존한다. 비공개 지시문은 내보내지 않았고 새 모델 실행이나 성능 주장은 없다.
