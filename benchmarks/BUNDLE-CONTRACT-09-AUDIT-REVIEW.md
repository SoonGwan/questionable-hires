# Checkpoint 09 persistence/diagnosis review — 2026-09-14

Launch `3a7d972`, resources `9071a1c`;
[whole-run intake](BUNDLE-CONTRACT-09-INTAKE.md). No new model runs. This pair
review completes the first pass over task outcomes, not full publication or
every prospective independent control.

## Persistence: real missing-write evidence, another original capture gap

Both arms remove only the reachable append in isolated code, retain the existing
test and show that its acknowledgment check misses the missing write. Both run
one unchanged stronger stored-list assertion against correct and faulty code,
including a pre-existing entry. Actual test-global binding and implementation
paths are checked, not inferred from a mutation label. Originals remain unchanged;
no harness or mutation is retained in either project snapshot.

The baseline original output starts inside the missing-append/existing-test phase.
The first correct-code/existing-test execution and leading section context are
absent. The remaining three native results and the stronger stored-list failure
are present. Its final four-cell pass/pass/pass/fail table overstates the directly
captured original evidence. This is an additional original gap beyond the form
skill gap; do not infer the missing first phase from a later successful replay.

Con Artist captures all four helper checks: existing tests pass on both variants,
the correct plain-Python probe passes, and the faulty probe fails because the new
record is absent. Imports and the actual test-global binding are checked in every
process, with reported time/output limits and original bytes/modes/cleanup. It
reads its entry and core audit guide, not the helper source or advanced references.
This differs from checkpoint 08's full implementation read, but does not alone
prove which change caused the cost difference.

Costs: baseline 82,917 tokens / 69.594s; skill 73,571 / 36.635s. Baseline uses a
unittest stronger check including acknowledgment; skill's stronger probe checks
stored records directly and prints acknowledgment. Their work and original
capture completeness differ. Neither establishes real database durability—the
supplied implementation writes to an in-memory list.

## Diagnosis: actual transport, not a cache simulation

Both retained probes call actual Search and transport.fetch, replacing only the
request dependency with controlled local responses. They record the actual
no-cache header and request parameters, establish overlapping requests, and run
normal/reversed completion orders. Both observe newest results normally and stale
older results when the earlier request completes last. Waits are bounded and
owned tasks are cleaned up. Production search.py/transport.py are unchanged.

Baseline redirects output to a result file, then captures that whole JSON in a
later command. Its initial empty output is therefore not the persistence/form
gap. Skill prints its JSON directly. Both appropriately leave production cache
behavior unknown: the local request boundary has no cache. They are diagnostic
witnesses of the current behavior, not reusable acceptance tests for a repaired
generation guard; both contain assertions about each current result assignment.

Baseline retains a script, JSON and Markdown report; skill retains only a script.
Costs: baseline 122,168 tokens / 112.027s; skill 71,521 / 57.910s. The observed
reduction includes different reporting/artifact work. It is not equal-work proof
or evidence that all production stale-result incidents share this cause.

## Separate author replay

[Replay script](replay_bundle_contract_09_audits.py) executes the literal original
persistence shell programs in disposable complete workspace copies. Only each
copy's index is restored from its verified pre-collector artifact. Diagnosis
replays the unchanged retained scripts without rewriting the original saved JSON.
All four exit 0 within the 45-second bounds. [Full report](results/bundle-contract-09-audit-controls/author-replay.json)
retains original/replay output, commands and changed paths.

Skill persistence and both diagnosis outputs match after path normalization and
unittest duration normalization where applicable. Baseline persistence's captured
suffix matches, **not the full output**: replay supplies the absent first phase.
The complete-output equality flag remains false. Baseline replay also changes
its copy's Git index through status refresh; this remains a changed path, not
silently excluded preservation evidence. Other copies have no changed entries.
Original workspaces and retained project inventories remain unchanged.

Full-run export/privacy review, consolidated outcome report and outstanding
independent failure controls remain. No completion score or chart promotion follows
from these replays. Two original capture gaps are now known: form skill and
persistence baseline. Shared cache/host, exposed tasks and n=1 still limit claims.

## 한국어

저장 감사는 실제 append 제거와 저장 목록 단언으로 결함을 확인했다. 스킬은
네 비교 결과와 바인딩 증거를 모두 남겼지만 기본 모델 원본에는 첫 정상 실행
부분이 빠져 있다. 후속 재실행으로 이 누락을 채우지 않는다. 기본 재실행의
Git 인덱스 변경도 보존 기록에 남겼다.

검색 진단은 두 모델 모두 실제 Search·transport를 실행해 캐시 없이 응답 순서만으로
문제를 재현했다. 기본 모델의 리다이렉트 결과는 나중에 전체 캡처돼 출력 누락과
구분된다. 스킬 비용은 낮지만 기본 모델은 보고서·결과 파일도 만들어 작업량이
다르다. 재실행 4개는 끝났으나 전체 공개 대조와 남은 대조군 검증은 계속 필요하다.
