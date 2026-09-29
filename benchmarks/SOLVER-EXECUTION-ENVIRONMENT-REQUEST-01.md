# Execution environment needed for the prospective guest comparison

2026-09-27, parent `566be7fb`. This is a concrete environment request, not a
completed optimization or a change to the original model attempts.

The candidate is [HTTP01 server](results/solver-mcp-http-01/server.py), using
the owned disposable VM and localhost streamable HTTP. Native four-command
delivery preserves Linux output, nonzero exit, cwd error and recovery, with guest
stop, process absence and port closure. [Actual model HTTP01](SOLVER-MODEL-HTTP-01.md)
confirms its tool is present in the model catalog, but its first command is
rejected before reaching the guest because approval is required and policy is
never. The general shell interface honestly permits guest mutations; it cannot
be relabeled read-only because a particular uname request is read-only.

What is needed: an owner-provided execution environment in which this actual
tool can obtain legitimate authorization. The exact server/tool, command and
scoped CLI launch are available in the original HTTP01 manifests; no permanent
service or personal registration has been added. Do not disable review, change
approval modes or invent safer annotations to bypass the recorded rejection.
An authorized environment is a prerequisite, not proof of host-tool exclusion:
that boundary and gold/grading non-exposure must still be verified before using
private grading resources. The existing native SDK tests do not substitute for
model authorization, and old development cases are not fresh validation.

No further identical model invocation is scheduled while this prerequisite is
missing. Read-only catalog inspection already answered its question. Remaining
native grading, all-eight quality and whole-task cost/time comparisons are not
waived. No global goal-completion or whole-project impasse claim follows merely
from this one route being unavailable.

Inspection of the current eight skill entries finds existing instructions to
batch known reads, reuse adequate native checks and stop after decisive evidence.
[Receipt guide-first01](RECEIPT-GUIDE-FIRST-01-REVIEW.md) already tested avoiding
helper source reads: tokens−2.17% but time+9.74%, both tasks slower; declined.
Do not repeat that approach as a new candidate. The frozen integration05
[input-cost analysis](results/all-eight-current-05/input-cost-analysis.json)
already separates response-count, initial-input and later-input effects; token
cost is not attributable to skill-file length alone. No new analysis tool,
speculative ordinary-skill edit, model run or improved-performance claim here.
README, featured benchmark and hosted pages remain unchanged.

한국어: 준비된 HTTP 게스트 도구는 실제 모델 목록에 노출되지만 호출 승인이
필요하고 현재 정책은 never라 실행되지 않는다. 사실과 다른 읽기 전용 표기나
승인 우회가 아닌, 정상 승인 가능한 실행 환경이 필요하다. 환경이 제공돼도
호스트 도구 제외·채점 정보 비노출·전체 품질·토큰·시간 검증은 별도로 남는다.
기존 스킬의 반복 억제 안내와 거절된 guide-first 실험을 확인했으며 같은 문구나
호출을 반복하지 않는다. 이 요청 자체를 성능 개선이나 목표 완료로 취급하지 않는다.
