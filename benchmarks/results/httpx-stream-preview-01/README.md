# Real-checkout stream diagnosis: correct mechanism, mixed efficiency

[Frozen protocol](../../HTTPX-STREAM-PREVIEW-01-PROTOCOL.md), launch `a2546a2`,
Exorcist resources frozen from `d90c1d4`. Full HTTPX checkout pinned to
`26d48e0634e6ee9cdc0533996db289ce4b430177`. New author-selected real-library
diagnosis, not an organic production incident or seeded upstream defect. Two fresh
Astra medium sessions, serial skill then baseline, one repeat each, 360-second
limits, equal explicit session persistence. Both complete without transport
errors, reruns/exclusions, source/resource changes or concurrent author tests.

| Arm | Input + output tokens | Full CLI seconds | Shell commands |
| --- | ---: | ---: | ---: |
| Baseline | 114,634 | 59.637 | 5 |
| Skill | 97,000 | 64.308 | 4 |
| Skill change | −15.38% | +7.83% | |

Cached input is included once; reasoning output is not added again. This is not
an overall efficiency win. n=1, shared host/cache, fixed order, authored selection
and different probe organization prevent causal/general conclusions. Neither
historical outcomes nor featured/localized charts are replaced.

한국어: 실제 HTTPX 체크아웃에서 두 조건 모두 세 가지 응답 읽기 경로를 재현하고
원인을 정확히 설명했다. 스킬은 토큰 15.38% 감소·시간 7.83% 증가로 전체 효율
목표에는 미달이다. 실제 라이브러리를 사용했지만 작성자가 정한 단일 진단 과제이며,
실서비스 장애나 일반적인 성능 우월성을 입증한 것은 아니다.

## Original diagnosis evidence

Both use the supplied interpreter and import HTTPX from their own copied checkout.
Each runs one stdin Python probe with actual Client/MockTransport and a recording
SyncByteStream, not a simulation of HTTPX internals. All paths use the same body
within each arm, delivered in two chunks. Preview bytes, cached-content availability,
consumed/closed state and underlying closure are observed before/after preview,
later read and context exit. Assertions check bodies, outcomes and single closure.

The streaming `iter_bytes` preview consumes the response without retaining HTTPX's
body cache; a later read raises StreamConsumed. A streaming `read` preview and an
ordinary buffered GET allow later reads. All three exhaust and close their streams
once. Both ground the distinction in `_models.py` and `_client.py`, explain why
observed closure alone is not the cause, and recommend full buffering only when
its memory cost is acceptable, otherwise one-pass bounded logging. MockTransport
has no live connection pool; the skill explicitly leaves production pool events
unproven, and neither claims actual network diagnosis or deploys a fix.

Baseline additionally asserts one underlying iteration and reads constructor
semantics. Skill records per-yield/exhaustion events, asserts final consumed/closed
state, and combines its probe with final status. Payload lengths, printed format,
source reads and extra checks differ; fewer shell calls alone are not a measured
causal mechanism. Neither uses the optional bounded-probe helper or its reference.

Skill's first filename filter returns two documentation images and pyproject,
not the implementation. A second inventory plus symbol search locates useful
files. Baseline also inventories twice. The skill's first selection is concrete
wasted discovery on this report; do not turn that observation into an unsupported
claim that every inventory is unnecessary.

## Stored responses resolve this run's incomplete CLI display

Reviewed same-session tool records are retained for both arms. Baseline's five
shell outputs match CLI command records. Two of skill's four CLI outputs omit
leading content: symbol/provenance discovery and the decisive probe. The stored
responses preserve both complete outputs, including all three probe paths, the
PASS assertion message and exit 0. No selected calls lack a matching response.
See [exact comparison](tool-reconciliation.json) and the
[skill tool records](response-preview--skill--1/tool-records.json).

This uses original stored tool evidence, not a reconstructed author replay or a
claim that CLI capture is fixed. The original CLI records remain unchanged in
their separate artifacts. Full private rollout context stays local. Exported
runtime paths are normalized to `<PREINSTALLED_PYTHON>`; source hashes identify
original unredacted artifacts. Rerunning requires a compatible installed runtime.

[Author integrity](author-integrity.json) separately verifies all 125 original
tracked files in each final snapshot against the pinned checkout, skill digest
and all four frozen skill resources. Original command traces contain no file
mutation; probes use stdin and bytecode writes are disabled. Selected source
exports include their upstream license and are not represented as full clones.
No post-run probe replay is substituted for the original observations.

Before timing: two native upstream tests pass, author three-path observations
and contradictory assertion control pass preflight. Twenty HTTPX-runner tests
pass, including new persistence propagation/default and isolated-profile tests;
their mocked model calls are not live model evidence. Metadata/link validation,
featured synchronization and whitespace checks pass. These are scoped checks,
not current hosted CI or whole-skill performance acceptance.

## Subsequent discovery correction, not measured above

After this run, Exorcist's first instruction distinguishes supplied paths from
API/error names: find named symbols with content search, using filename discovery
for missing locations. The observation motivating this change is the first filter
returning unrelated images, not evidence that all discovery is wasteful. Controls,
stopping criteria, native execution and scope stay intact; no helper is added.
The correction follows skill-creator's evidence-backed, narrow-instruction rule.
Its adoption and resource effect need new-task evidence, not this run's percentages.

Later [old/new query-construction screen](../httpx-query-build-01/README.md)
observes direct-search adoption but does not accept a whole-task improvement.
The discovery paragraph is restored to its previous version; this earlier stream
comparison remains unchanged and is not repurposed as evidence for that decision.
