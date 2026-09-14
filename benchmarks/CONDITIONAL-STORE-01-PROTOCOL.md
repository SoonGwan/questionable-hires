# Conditional store audit — 2026-09-15

Freeze before calls. Exact project and task are `FILES` and `TASK` in
`cases_conditional_store.py`. This is a new **authored synthetic** developer task,
not a real upstream incident or independent project holdout. It targets an area
used to develop the recent collector correction; do not portray it as unseen
confirmation of that capability.

## Question and controls

Compare Con Artist original `1d80f49` against candidate `de65613`. Both explicitly
invoke the skill. The entry is identical; only the context collector and its
focused reference differ. Does ordinary task execution adopt that optional
collector, and does the complete audit become more effective/efficient?
Do not force the collector, score its use as success or attribute a difference to
it when neither condition uses it. There is no no-skill baseline in this pair.

Seven project files implement a synchronous JSON store with a conditional default
codec and two acknowledgment-only tests. Contracts exclude concurrency, crash
atomicity, path hardening and unsupported codecs. Required work is explicit:
actual binding/default-codec analysis; original tests on correct/faulty isolated
implementations; improved first-write and replacement assertions retaining both
acknowledgments; both improved tests on correct/faulty implementations; observed
fault-specific assertions and scope/cleanup. Only original `tests/test_submit.py`
may change. No production mutation, installs, network, environment changes or
commits. Model scratch must stay inside the project and be removed.

Author preflight `preflight_conditional_store.py` runs all four native combinations.
Original two tests pass both correct code and a mutation writing JSON null instead
of the supplied content. Author-added semantic content assertions pass correct
code and fail both faulty tests with `None !=` actual/expected evidence. Source
hashes and project-local scratch cleanup are checked. Author assertions and
preflight outputs are not copied into model workspaces. Equivalent reachable
payload-loss faults and meaningful assertions are accepted; runtime/binding/setup
errors are not credited as detecting a production fault.

## Schedule and evidence

Two fresh serial persisted GPT-6 Astra / medium sessions, **original then
candidate**, one each, 240 seconds. Freeze resources, exact files/task and resource
digests before launch; personal skills disabled. Use existing `run_cell`, save
every cell, stop on `limit_detected`, no favorable retries or task changes.

Inspect actual stored tool responses as well as CLI logs, final test changes,
original production/resource hashes and scratch cleanup. Compare total input
(cached included once) plus output tokens, process wall time, completed work,
extra/recovery work and helper adoption. Author replays are separately labeled.
Shared host/cache, fixed order, synthetic task and n=1 limit interpretation.
No chart promotion or all-eight performance claim from this screen.

한국어: 조건부 JSON 코덱을 사용하는 작은 저장소의 테스트 감사 과제다. 직접 만든
개발용 과제이며 독립 프로젝트 검증이 아니다. 수집기 수정 전후 스킬을 각 1회
실행하고, 도구 사용을 강제하지 않는다. 양쪽 모두 네 번의 실제 검사와 올바른
테스트 보강·원본 보존·정리를 수행해야 한다. 정상 통과와 실제 값이 남는 실패를
미리 확인했고, 결과에 맞춘 재시도나 대표 그래프 갱신은 하지 않는다.
