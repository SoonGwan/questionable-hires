# QueryParams design: direct Landlord revision screen — 2026-09-15

Frozen before calls. Compare original `bd1d8b8` with candidate `775a6a9`.
Only Landlord's large-file reading guidance differs. This is another ticket on
HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`, not an independent project
holdout. Both conditions explicitly invoke Landlord; there is no no-skill arm.

## Exact task

Replace `<PREINSTALLED_PYTHON>` with the same existing interpreter in both cells.

> Review a proposal to replace HTTPX QueryParams with dict(raw_input) followed by
> urllib.parse.urlencode using its default doseq=False, to reduce maintenance.
> Can it preserve current behavior and consumers? Recommend keep, simplify or
> replace with source references and maintenance tradeoffs. Consider the nearest
> viable repair, not just the proposal's first failing input: explain where
> normalization, repeated-value handling and ownership policy would move.
>
> Start with httpx/_urls.py, tests/models/test_queryparams.py and the relevant
> request-building consumer in httpx/_client.py. Run the existing
> tests/models/test_queryparams.py group. Execute these four actual inputs:
> 1. [('a', '1'), ('a', '2'), ('keep', 'x')]
> 2. {'enabled': True, 'empty': None}
> 3. {'a': ['1', '2']}
> 4. {'a': 'one two', 'keep': 'x'}
> For each record str(httpx.QueryParams(raw_input)), its multi_items(), and
> urllib.parse.urlencode(dict(raw_input)). Explain differences and the preserved
> control. Also execute base = httpx.QueryParams('a=1&a=2&keep=x') and
> derived = base.add('a', '3'); record both afterward. With a context-managed
> httpx.Client(params=base, trust_env=False, transport=httpx.MockTransport(
> lambda request: httpx.Response(200))), build (do not send) a GET request to
> https://example.invalid/path with params=[('a', '7'), ('a', '8')]. Record its
> URL and client.params afterward. Trace the actual merge consumer and explain
> ownership and replacement semantics. Distinguish local observations from a
> complete replacement implementation or network behavior. Do not implement a
> full alternative.
>
> Preserve source files and installed resources. No network, installs, history
> fetches, commits or publication. Use <PREINSTALLED_PYTHON> with -B; pytest also
> with -p no:cacheprovider. Scratch, if needed, stays inside this project and must
> be removed. Captured observations suffice; no separate report file required.

## Frozen evidence and acceptance

Author preflight `preflight_httpx_query_design.py` and
`httpx-query-design-01-preflight.json`: all 14 native tests pass; four input
observations and local ownership/build-request observations pass. Deliberate
assertion failure shows original repeated encoding versus last-value dict
encoding with actual/expected values, not a support exception. All 125 tracked
source files remain unchanged. These author files are not supplied to models.

Required: executed native group; all four current/multi-item/proposed outputs;
correct loss versus preserved control; executed immutable-add and request merge
observations; actual consumer reference; feasible repair/policy-location analysis;
scope preservation. Accept supported alternatives, not a predetermined verdict.
Do not credit static reading as execution or cheaper incomplete work as a win.

## Schedule and interpretation

Two fresh serial sessions, **candidate then original**, GPT-6 Astra / medium,
one each, 240 seconds each. Same source/runtime/task; exact resource snapshots
and manifests recorded before execution. Disable personal skills, persist original
sessions, preserve every cell, no retries or favorable exclusions. Stop on an
actual account limit. Compare total input (cached included once) + output tokens,
process wall time and completed work. Inspect original stored tool responses
against CLI captures; distinguish truncation and unobserved context.

Fixed order, shared host/cache, n=1, same-project near-transfer and author-designed
task limit inference. No featured chart update or broad efficacy claim from this
screen. Unfavorable or mixed results remain published alongside favorable ones.

한국어: 큰 파일 읽기 지침 수정 전후를 동일한 새 QueryParams 검토 과제로
비교한다. 두 조건 모두 Landlord를 사용한다. 네 입력과 원본 보존·요청 병합을
실제 실행하고 정상 대조군과 실패 반례를 먼저 확인했다. 같은 HTTPX 프로젝트의
유사 과제이며 각 1회인 개발용 비교다. 좋은 결과만 고르거나 대표 그래프에
올리지 않고, 지침 수정의 관측된 효과와 한계를 함께 기록한다.
