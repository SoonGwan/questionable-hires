# Native edit audit01 — helper unused, efficiency not demonstrated

2026-09-21. Launch `f5654a2`; prior resources `04bf934`, current `e6aa16e`.
[Frozen protocol](EDIT-AUDIT-01-PROTOCOL.md), [schedule and inputs](results/edit-audit-01/run.json),
[review and capture mappings](results/edit-audit-01/comparison.json),
[author preflight](results/edit-audit-01-preflight.json).

All six original Astra medium sessions completed without timeout or account-limit
stop. No repeats, excluded cells, replacement runs or edits during measurement.
All three conditions meet the five proposal and six verified-assertion criteria.
This does **not** establish an efficiency improvement: current uses more tokens
than baseline in both requests and substantially more time in the verified request.
None of the four skill sessions reads or invokes the helper or its mode guide.
The new native invocation capability therefore has no demonstrated cost impact.

## Every measured cell

Tokens are input plus output, with cached input included once. All discovery,
instrumentation, failures, repairs and supplementary checks remain included.
Wall time is complete process time, not native-test time or a billing estimate.

| Request | Condition | Input | Cached subset | Output | Total | Seconds | Responses | Unittest processes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Proposal | Prior | 75,660 | 57,216 | 2,382 | 78,042 | 82.698 | 4 | 8 |
| Proposal | Baseline | 68,151 | 54,144 | 2,466 | 70,617 | 84.975 | 4 | 8 |
| Proposal | Current | 73,370 | 59,520 | 1,929 | 75,299 | 69.111 | 4 | 8 |
| Verified | Current | 132,367 | 112,512 | 5,298 | 137,665 | 183.065 | 6 | 21, including setup failure |
| Verified | Baseline | 69,643 | 54,272 | 2,355 | 71,998 | 83.559 | 4 | 16 |
| Verified | Prior | 77,038 | 64,000 | 2,517 | 79,555 | 86.833 | 4 | 16 |

Current versus prior: proposal tokens−3.52%/time−16.43%; verified
tokens+73.04%/time+110.82%. Current versus baseline: proposal
tokens+6.63%/time−18.67%; verified tokens+91.21%/time+119.09%.
One authored project, two requests,n=1 per condition, fixed order/shared host/cache
and unblinded review: not independent generalization, significance, causal
attribution or a broad20–30% improvement. No featured-chart replacement.

## Actual work and criteria

Every cell executes both selected native tests on correct code and on each of
three separate faults. Faults change only `apply_edits`: forward iteration using
original offsets, omitted overlap rejection, or caller-list in-place sorting.
The eight requested native observations have exits `0,0,0,0,0,1,0,0`. The single
detected fault is omitted overlap rejection; the assertion is `ValueError not
raised`, not an import/setup exception. Original-coordinate errors still return
length7, and sorting changes caller order without affecting these assertions.

All proposal answers give concrete exact-output and list-snapshot comparisons and
label them unexecuted. The observations also establish actual copied function
bindings and returned/list-mutated behavior in native test processes.

All verified answers establish stronger exact output and list preservation on
success and overlap failure: correct code passes, corresponding faults fail the
intended assertions. Extra overlap-rejection assertions are also executed.
The work is **not identical**, despite meeting the same minimum criteria:

- **Prior:**8 selected native processes plus8 individually selected stronger
  checks. Sixteen methods total. Same-process call traces establish module,
  imported alias and executing-code identities. No supplementary control suite.
- **Baseline:**8 selected native processes,4 supplementary `test_controls` runs,
  and4 stronger-suite processes with4 methods each:16 processes/28 methods.
  Binding/path/hash assertions are appended after unchanged native test bodies
  in copied `test_edits.py`; original files stay unchanged. Stronger tests import
  that verified alias. This is not byte-identical copied test-module content,
  though native test bodies remain intact and instrumentation is permitted.
- **Current:** first correct native test passes without the intended startup
  hook; the orchestration asserts missing same-process evidence and cleans up.
  The corrected execution supplies copy-local `PYTHONPATH`, performs8 selected
  checks and8 individually selected stronger checks, then starts supplementary
  controls. Forward application makes the control's deletion example fail
  (`βZ != Z`), contrary to the orchestration's expected0, so that command stops.
  A final command executes the two remaining controls. Total:21 processes,
  including the initial incomplete check, and20 valid native test-method runs.

The current answer excludes its initial run **as provenance proof**, not from this
report's costs. Both the missing-hook failure and the unexpected supplementary
control failure remain in the original records. The supplementary failure is
genuine detection, not a production repair or a failed task criterion. Current
and baseline preserve this additional forward-application finding in their answers.
Process or method counts are not coverage scores; neither can normalize these
sessions into a causal patch-speed estimate.

## Original evidence, capture and preservation

Reviewed actual commands, original native outputs/assertions, answers and final
project state; no author replay supplies missing model observations. All original
bytes/modes, repository HEAD and installed resources match. Only the four supplied
project files remain; owned scratch is removed. Saved pre-collection index entries
match the initial tree, but a pre-session binary index was not captured.

All recorded response usage reconciles with each CLI total. The four skill bodies
are identical between resources and appear in original initial messages, then are
reread; baseline exact-body observations are absent, not proof of every context
influence being absent. The helper resources differ, but are not read/invoked.

Of24 shell outputs,19 match exactly and5 match unique nonempty suffixes with equal
exits. No unmatched original outputs or CLI items. Missing prefixes retained in
the same-session originals are:

- Proposal prior `item_5`: the first correct native test, binding/behavior trace,
  pass/exit0 and the next command label.
- Proposal current `item_5`: first variant/cwd/command labels only.
- Verified current `item_7`: first corrected native test, startup/binding/behavior
  trace and pass/exit0.
- Verified baseline `item_4`: variant/hash, first correct native binding/result,
  pass/exit0 and the next command label.
- Verified prior `item_4`: first correct native binding/behavior/result,
  pass/exit0 and the next command label.

Public exports include redacted original tool records, commands, CLI events,
source identities, usage, exposure and project snapshots. Private initial
instructions/full rollouts remain local only. The limited evidence-pattern scan
passes; that is not a universal privacy/security certificate.

## Decision

Retain the implemented native-mode capability and its local tests, but **do not
promote it as a measured performance improvement**. Availability alone did not
lead to use. Do not rerun this now-exposed fixture until favorable, replace the
baseline with a weaker workflow, or subtract current's recovery costs.
Investigate the concrete tool-discovery/selection boundary before adding more
unconsumed helper functionality. Any future routing change needs a new relevant
task and equivalent requirements; another small authored audit alone cannot prove
the all-eight real-development objective.

한국어:6개 세션의 원본 검토를 마쳤고 모두 감사·보존 요구를 충족했다. 하지만
수정 스킬은 무스킬보다 제안 과제에서6.63%, 입증 과제에서91.21% 더 많은 토큰을
썼다. 입증 과제의 시작 훅 복구와 추가 대조 실행 비용도 모두 포함했다. 무스킬은
보강 검사를 묶어 더 많은 테스트 메서드를 실행했으므로 단순 실행 횟수가 품질
점수는 아니다. 네 스킬 세션 모두 바뀐 도구를 읽거나 실행하지 않아 패치의 비용
효과도 입증하지 못했다. 유리한 결과가 나올 때까지 같은 문제를 반복하지 않으며,
대표 그래프와 전체 성능 미달 판단을 유지한다.
