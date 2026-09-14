# QueryParams design: region selection did not reduce whole-task cost

Frozen launch `f8ac46c`; [protocol](../../HTTPX-QUERY-DESIGN-01-PROTOCOL.md).
Original Landlord `bd1d8b8` versus large-file candidate `775a6a9`; both explicitly
invoke the skill. HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`.
GPT-6 Astra / medium, candidate then original, one fresh persisted session each,
240-second cap. Same-project near-transfer, not an independent project holdout.

| Condition | Total input + output tokens | Seconds | Shell / outer calls |
| --- | ---: | ---: | ---: |
| Original | 128,259 | 81.188 | 6 / 4 |
| Candidate | 130,283 | 92.509 | 8 / 4 |

Candidate **+1.58% tokens / +13.94% time**. Cached input is included once.
Both complete the required work: 14 native tests pass, all four encoding and
multi-item observations are correct, immutable-add and client request merging
are executed, and actual consumer/policy-location analysis is supported.
No performance win. Fixed order, shared host/cache, n=1 and different extra work
limit causal inference. No no-skill comparison or featured/chart promotion.

## Decisions and execution

Both show duplicate loss, boolean/None normalization changes, list stringification
and the preserved scalar/space control. Both observe base staying unchanged,
derived gaining a third value, and request values replacing the client's entire
matching group while retaining unrelated defaults. Both trace
`build_request` → `_merge_queryparams` → `QueryParams.merge` and distinguish
immutable public operations from universal deep copying.

Both recommend keeping the abstraction while considering a viable repair:
grouped normalized values or repeated pairs, protected ownership and whole-group
replacement. `doseq=True` alone does not recover duplicates already discarded by
`dict()`. Both explain policy relocation rather than just rejecting the first
counterexample. Neither implements a replacement or sends a network request.
Candidate additionally records identity and post-client base/derived checks.

Candidate locates definitions before reading `_urls.py` 420–660 and selected
client regions. Original already selects ranges, but includes `_urls.py` 1–180
as well. Candidate also reads the whole shared `tests/conftest.py` plus
configuration; original does not. Smaller core-source ranges therefore do not
establish less total context or work. Both take four outer tool calls; candidate
uses two additional shell commands. This observation does not isolate a causal
cost for any one command or sentence.

The result argues against treating a preliminary definition search as a mandatory
extra phase. Preserve relevant context and truncation recovery, but allow known
regions to be read directly. A further wording change requires its own evidence;
do not attach these measurements to it or retry this task for a favorable number.

## Original evidence, scope and limitations

[comparison.json](comparison.json), manifests, commands, answers, selected public
source and stored `tool-records.json` are exported for both conditions. All 14
shell output/exit pairs match the original stored tool responses after workspace
path normalization. No unmatched or missing outer outputs, duplicate call IDs or
unparseable JSON blocks. No observed output-budget truncation in this pair;
the word “truncation” inside the candidate skill text is not a truncation warning.
Native pass summaries and all decisive probes are complete in original records,
not author replays. Exact capture correspondence is not a certificate of all model
context. Full rollouts remain local because they contain private instructions.

All 125 original file bytes and installed resource manifests remain unchanged.
No non-Git/non-skill extra files remain. Reviewed commands contain no source
writes, installs or network calls. Candidate's final instruction-file discovery
returns exit 1 for no matches; native tests and probes exit 0. No failed runtime
checks, retries, timeout or account limit occurred. The launch snippet checked
an obsolete `account_limit` key rather than `limit_detected`; neither cell hit a
limit, so no observed scheduling effect, but that snippet must not be reused.
Final identity alone does not prove absence of every transient write.

한국어: 이전 지침과 큰 파일 구간 선택 수정본을 각각 1회 비교했다. 양쪽 모두
14개 검사, 네 입력, 원본 보존·요청 병합 관찰과 실제 소비자 분석을 충족했다.
수정본은 토큰 1.58%, 시간 13.94% 증가해 효율 개선이 아니다. 관련 정의를 먼저
찾는 행동은 나타났지만 추가 검색·공통 테스트 설정 읽기도 있었다. 구간 선택을
필수 사전 단계로 강제하기보다 이미 아는 위치는 바로 읽을 수 있게 해야 한다.
같은 프로젝트의 소규모 개발용 관찰이며, 불리한 결과와 원본 근거를 보존하고
대표 그래프는 바꾸지 않는다.
