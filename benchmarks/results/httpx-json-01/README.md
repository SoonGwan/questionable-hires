# HTTPX JSON 01: real-source comparison, no token-efficiency win

Reviewed 2026-09-15. [Frozen protocol](../../HTTPX-JSON-01-PROTOCOL.md), launch
`fa86d62`; current resources `13394dc`. One actual upstream HTTPX task, three
fresh serial Astra-medium sessions, one observation per condition. The lean
entry uses the same corrected helper and supporting resources as current.
This does not isolate the helper fix from previous versions.

All three satisfy the four explicit task criteria after original-evidence review.
**The shorter candidate does not improve token efficiency. Do not promote it.**

| Condition | Total tokens | Wall seconds | Full task |
| --- | ---: | ---: | --- |
| No-skill baseline | 127,296 | 100.476 | Pass |
| Current Receipt | 188,038 | 80.399 | Pass |
| Lean Receipt | 221,517 | 80.229 | Pass |

Current uses 47.7% more tokens than baseline; lean uses 74.0% more. Both observed
wall times are about 20% lower, but lean and current are effectively equal in
time while lean uses 17.8% more tokens than current. Tokens include cached input
once plus output. No dollar estimate, confidence interval or broad superiority
claim: n=1, fixed order (lean, baseline, current), shared host/cache. All scheduled
sessions completed without timeout, quota stop or replacement attempt.

## Original evidence and criteria

Each directory contains the answer, CLI events, selected stored tool records,
metadata/resource hashes, initial-context inspection, review and selected upstream
source excerpts with its license. Full private session instructions are excluded.
Paths are redacted; source hashes refer to original unredacted artifacts.

- [Baseline](baseline/httpx-json-commit--baseline--1/review.json)
- [Current](current/httpx-json-commit--skill--1/review.json)
- [Lean](lean/httpx-json-commit--skill--1/review.json)
- [All rows](comparison.json) and [launch manifest](run.json)

1. **Equal native work.** All run exactly the requested five existing tests,
   with identical current assertions, package support, conftest and configuration.
   Only `httpx/_content.py` varies between the specified parent and encoder commit.
   Both skill cells use the frozen helper; baseline builds disposable copies and
   a reporting-only pytest plugin. No rewritten encoder or replacement assertions.
2. **Actual behavior.** Each before run has four real failures and one passing
   empty-content control; after has five passes. Native exits are 1/0. Failures
   expose length 19 versus 18, escaped versus preserved Unicode, separator
   differences and NaN not raising. The before combined non-finite test stops at
   NaN; none claims its infinity assertion ran. After passes both checkpoints.
3. **Provenance.** Full revisions and direct-parent relationship are identified.
   Native test processes report copy-local HTTPX and encoder modules; source
   inspection follows public Request/Response encoding paths. Baseline additionally
   records encoder hashes, public/model identities and native process IDs.
4. **Scope/preservation.** All 125 tracked original files retain bytes and modes;
   HEAD/resources unchanged, no extra retained project files. Actual commands
   create and remove project-local scratch. No installs, requests, external
   discovery, production edits or commits. Both skill guard reports and baseline's
   own pre/post inventory also confirm preservation around native execution.

The source is a real upstream project/commit but author-selected and development-
visible. Current support/dependencies stay fixed; this is not a reconstruction
of complete historical environments or independent production-user validation.
No native author replay was needed for this review.

## Capture and context limits

13 of 16 shell output/exit pairs match normalized stored responses exactly.
Baseline item 2 and current item 3 are broad source reads with explicitly
truncated stored output; omitted portions remain unavailable. Their native test
execution is a separate captured command, not inferred from the missing text.
Baseline item 2's final no-match instruction-file search returns 1; it is not a
native test failure. Required commit/tests and public paths are also supported
by the retained output, subsequent reads and executable evidence.

Baseline item 5's CLI drops the leading native output without a truncation marker.
The matching stored tool response at line 37 preserves the complete before/after
test sequence, provenance, actual assertions, native exits and cleanup. Both
captures remain exported. A literal `truncated` word in helper source or
`output_truncated:false` is not itself missing output. Tool-call IDs have no
missing, duplicate or unmatched outputs.

Recorded turn context identifies `gpt-6-astra` in all three. Both skill entries
match initial injected bodies before the first tool. Baseline lacks a matching
current Receipt body in recorded initial messages; this does not prove absence
of unrecorded context. Personal catalog names are replaced with counts/hashes.

## Development decision

Keep the shipped entry and the adverse candidate result; do not update featured
charts. Both skill sessions spend multiple reads inspecting helper implementation
before calling its Python API. Current reads two broad ranges; lean uses several
focused ranges. This suggests investigating helper selection/API usability, not
claiming that source reads alone caused the token gap. The guide currently directs
supported Python comparisons through the helper, whereas baseline completes the
same requirements with native facilities. Compare those tradeoffs before adding
another mandatory tool or another blanket instruction not to inspect code.

Do not keep replaying this ticket until a favorable number appears. Subsequent
changes need new task evidence and the wider eight-role objective still requires
successful validation at equal/lower whole-task cost.

한국어: 실제 HTTPX 과제에서 세 조건 모두 같은 요구사항을 충족했다. 현재 스킬은
무스킬보다 토큰 47.7%, 짧은 후보는 74.0%를 더 썼다. 시간은 약 20% 적었지만
각 조건 1회이므로 일반적인 속도 향상을 주장하지 않는다. 짧은 후보는 현재보다
토큰이 17.8% 늘어 채택하지 않는다. 누락된 CLI 앞부분은 저장된 원본 테스트
출력으로 확인했고, 실제로 누락된 광범위 소스 읽기는 한계를 명시했다. 재실행 없이
원본 증거·채점·보존 검토를 공개한다. 다음은 도우미 선택과 사용성 검토이며, 같은
과제를 유리해질 때까지 반복하거나 대표 그래프를 바꾸지 않는다.
