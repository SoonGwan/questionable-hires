# Header dictionary design screen — 2026-09-15

Freeze before model calls. Current Landlord resources at `bd1d8b8`; no instruction
change under test. New authored ticket on the existing real HTTPX checkout
`26d48e0634e6ee9cdc0533996db289ce4b430177`. Same project as previous experiments,
not an independent project holdout. Purpose: locate current end-to-end work and
decision gaps before changing Landlord again.

## Exact task for both arms

Replace `<PREINSTALLED_PYTHON>` with the same existing runtime in both cells.

> Review a proposal to replace HTTPX Headers with a plain dict[str, str] to reduce
> maintenance. Compare two concrete representations: P1 keeps the last value for
> each lowercased ASCII name; P2 stores dict(existing_headers), including its
> joined values. Can either preserve the current public behavior and real
> consumers without adding equivalent policy/state elsewhere? Recommend keep,
> simplify or replace, with actual source references and maintenance tradeoffs.
>
> Start with httpx/_models.py, tests/models/test_headers.py and relevant consumers
> such as httpx/_transports/default.py. Inspect additional bindings only as needed.
> Run the existing tests/models/test_headers.py group. Also execute these four
> byte-pair inputs using actual httpx.Headers:
> 1. [(b'x-tag', b'one'), (b'x-other', b'other')]
> 2. [(b'X-Tag', b'one'), (b'x-tag', b'two')]
> 3. [(b'x-tag', b'one, two')]
> 4. [(b'x-tag', b'one, two'), (b'x-tag', b'three')]
> For each, record original headers and reconstructions from P1 and P2:
> indexing at 'x-tag', get_list('x-tag') without comma splitting, multi_items(),
> and raw name/value pairs. Decode these ASCII bytes only for readable reporting.
> Explain preserved behavior versus lost information and whether comma splitting
> can restore original field boundaries. Reconstruction is an information-loss
> probe, not a full replacement implementation; do not claim it tests a complete
> new transport. Inspect one real consumer and trace where the compatibility
> policy would have to move if the wrapper disappeared. Do not implement a full
> alternative or infer network behavior from these local observations.
>
> Preserve source files and installed resources. No network, installs, history
> fetches, commits or publication. Use <PREINSTALLED_PYTHON> with -B; pytest also
> with -p no:cacheprovider. Scratch, if needed, stays inside this project and must
> be removed. Captured observations suffice; no separate report file required.

## Controls and frozen criteria

`preflight_httpx_headers_design.py` / `httpx-headers-design-01-preflight.json`
executes the native group (27 pass) and all twelve representations. An actual
assertion comparing original repeated values with P2's joined value fails with
the differing lists. Unique lowercase input is a preserved control. P1 loses
earlier repeated values; P2 can preserve joined lookup but loses field boundaries
and raw casing. Repeated fields and one comma-valued field can collide under P2;
comma splitting cannot distinguish them. These are model-visible obligations.
Author preflight/expected outputs are not copied into model workspaces.

Accept supported alternatives that retain equivalent metadata/policy; do not
reward a predetermined architectural slogan. Required evidence: native test
identity/results, twelve observed representations, correct equivalence limits,
one actual consumer and policy-location explanation, scope preservation. Do not
credit static reading as executed checks or unexplained low cost as success.

## Execution

Two fresh serial GPT-6 Astra / medium sessions, **baseline then skill**, one each,
240 seconds. Full source copies. Snapshot all Landlord resources from `bd1d8b8`;
the skill arm alone receives explicit skill invocation. Persist original sessions,
disable personal skills and store manifests before launch. No retries, favorable
exclusions or edited tasks. Stop on an actual account limit.

Compare total input (cached included once) + output tokens, wall time and actual
work. Review stored tool responses against CLI output before interpreting results.
Shared host/cache, fixed order, n=1 and same-source task development limit inference.
No chart promotion or all-eight claim from this screen, favorable or otherwise.

한국어: 실제 HTTPX 헤더 표현을 두 종류의 dict로 바꾸는 새 검토 과제다. 기존
27개 검사와 4개 입력×3개 표현을 먼저 확인했고, 정상 대조와 정보 소실을 고정했다.
현재 Landlord의 실행량과 판단을 확인하기 위한 비교이며 새 지침의 효과 검증이나
독립 프로젝트 일반화가 아니다. 결과에 맞춰 과제를 고치거나 재추첨하지 않는다.
