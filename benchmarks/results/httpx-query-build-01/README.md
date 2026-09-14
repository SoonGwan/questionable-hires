# Old/new discovery screen: candidate not accepted

[Frozen protocol](../../HTTPX-QUERY-BUILD-01-PROTOCOL.md), launch `6464e84`, full
HTTPX checkout `26d48e0634e6ee9cdc0533996db289ce4b430177`. Three fresh serial Astra
medium sessions: candidate `329d06c`, baseline, original skill `d90c1d4`. One
session per condition, not three repeats. The skill snapshots differ only in the
entrypoint's first discovery paragraph. All scheduled cells complete; no model
retries, transport errors, exclusions, input/resource changes or concurrent author
tests. Author-selected real-library task, not an organic incident or holdout.

| Condition | Input + output tokens | CLI seconds | Shell commands | Outer tool calls |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 113,748 | 67.741 | 5 | 5 |
| Original skill | 76,034 | 61.179 | 5 | 3 |
| Candidate skill | 101,345 | 63.100 | 4 | 4 |

Candidate versus baseline: **−10.90% tokens / −6.85% time**. Candidate versus
original skill: **+33.29% tokens / +3.14% time**. Cached input is included once;
reasoning output is not added again. Comparing only with baseline would hide the
adverse original-skill comparison. This does not establish a general winner:
fixed order, shared host/cache, n=1 and different extra work prevent causal claims.

한국어: 수정 후 스킬은 미적용 조건보다 토큰 10.90%·시간 6.85%가 적었지만,
수정 전 스킬보다 토큰 33.29%·시간 3.14%가 많았다. 첫 검색은 개선 의도대로
바뀌었으나 전체 비용 개선으로 채택할 근거는 얻지 못했다. 단일 실행과 실제
작업 차이가 있으므로 새 문구가 악화의 원인이라고 단정하지 않는다. 후보는
보류하고 기존 진입점으로 복원하며, 모든 결과와 한계를 보존한다.

## Coverage and actual work

All three construct the four requested cases with actual Client.build_request
and the supplied runtime, importing their own checkout. URLs and ordered repeated
items match the author preflight. They correctly distinguish omitted params from
an explicit empty mapping, URL-query replacement from client/request merging, and
replacement of a conflicting key's whole value list. No requests are sent.

All recommendations preserve repeated values using QueryParams and explicitly
condition precedence on caller intent. They warn against collapsing repeated
values into a plain dict and distinguish “no additions” from explicit clearing.
Original skill proposes a source-supported merge recipe but does not execute it;
baseline and candidate additionally execute caller-side compositions. The task
requested a recommendation, not mandatory execution of that recommendation.

The implementations do different work:

- Candidate starts with named-symbol content search and avoids the earlier
  uninformative project-name filename filter. It still discovers filenames in
  that same command. It executes four original cases, then repeats those four
  alongside four merged-query variants: twelve explicit build_request calls in
  two native probe processes. It uses four outer tool calls.
- Original skill inventories files, reads the skill, then runs symbol discovery
  and its four-case native probe concurrently in one outer call before reading
  implementation details. Five shell commands fit into three outer calls.
- Baseline executes the four cases plus two proposed-merge examples in one native
  probe. Its source-read command also searches a nonexistent `tests/test_urls.py`,
  producing exit 2; that error and its cost remain included. It does not invalidate
  the separately successful native reproduction, but limits efficiency comparison.

The baseline example chooses client < URL < request precedence; the candidate
example chooses URL < client < request. Both explicitly describe that choice,
and both preserve the winning key's repeated values. These are not interchangeable
application policies, nor evidence that one benchmark solution should silently
override a user's requirements.

The candidate's cheaper first search is real adoption, but fewer shell commands
do not prove lower whole-task cost. Additional probes, repeat constructions,
source/answer lengths and outer-call grouping all differ. Do not attribute the
33.29% increase solely to the new paragraph or claim the old skill universally
saves resources.

## Original evidence and integrity

Each condition directory contains its frozen run manifest, original events,
commands, answers, selected source excerpts/license, metadata, source hashes,
reviewed same-session tool records and an author-integrity report. All 125
tracked upstream files remain byte-identical in every final snapshot; installed
resources and usage match their recorded manifests. Probes run through stdin
with bytecode writing disabled; no original code, installs or diagnostic files
are changed/created. Selected excerpts are not full-checkout exports.

[Comparison and response reconciliation](comparison.json) preserve all selected
tool-response pairs. Candidate's final CLI command output contains only Git
status; its stored original response also retains the complete second probe.
Baseline and original shell outputs match their stored responses. Original's
parallel call returns two fulfilled Promise.allSettled wrappers; their actual
values are retained, not discarded as missing output. No missing, duplicate or
unmatched selected responses. This is original evidence, not an author rerun or
a repair of the CLI transcript. Full private rollout stays local. Runtime paths
are normalized to `<PREINSTALLED_PYTHON>` only in exported text.

## Decision

Do not adopt `329d06c` as a performance improvement. Restore the previous
entrypoint exactly; keep all controls, bounded-probe capability and diagnosis
scope. This is a provisional acceptance decision under insufficient/mixed
evidence, not proof that content search is bad or that the old wording caused its
lower recorded cost. No further draw on this exposed task follows. Following
skill-creator's narrow evidence-backed iteration rule, avoid keeping additional
guidance merely because one intermediate behavior looked better.

Twenty-one local HTTPX-runner tests and the native four-case/contradictory-assertion
preflight pass. Two upstream preflight tests pass before each timed session.
These checks do not establish all-eight efficiency or hosted release readiness.
Featured charts and prior frozen claims remain unchanged.
