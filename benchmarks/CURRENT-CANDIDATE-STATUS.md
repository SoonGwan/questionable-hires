# Current candidate: whole-task performance remains unproven

Decision checkpoint **2026-09-21, local validation at `04741d7`**.
This index is not a new measurement. Each result below belongs to its named
resource, not automatically to this working version.

## Objective and unfinished requirements

All eight skills should improve real developer outcomes at similar or lower
token/time cost. The broad20–30%+ goal is **not established**. Passing helper
tests does not establish model efficiency, independent generalization or release
readiness. No public-release approval or successful hosted matrix is claimed.

한국어:8개 스킬 전체의 실제 개발 성능·비용 개선 목표는 아직 미달이다.
도구 테스트 통과, 모델 성능 실증, 공개 배포 준비는 서로 다른 조건이다.

## Model evidence that governs claims

[External-issue pilot selection](SWE-LITE-PILOT-01-SELECTION.md) freezes two
SWE-bench Lite instance identities by a predeclared hash rule, without inspecting
solution patches. Environment/license/scoring gates are pending; no model calls
or new performance result. Public tasks are not proven uncontaminated holdout.
[Image feasibility](SWE-LITE-PILOT-01-ENVIRONMENT.md): both pinned amd64 images
start under compatibility mode with matching source blobs, but differing modes
and broad Git stores require solver isolation. Imports are not native-test validation.
[Base-only copies and smoke checks](SWE-LITE-PILOT-01-ISOLATION.md) now preserve
the exact base trees with one fresh commit/no remotes. Requests one native control
and pytest77 existing tests pass; setup failures are retained. Hidden scoring,
same-process provenance and complete solver-access review remain pending.
[Scoring preflight](SWE-LITE-PILOT-01-SCORING-PREFLIGHT.md) rejects the current
offline environment: pytest setup fails despite its expected gold transition;
Requests gold retains60 failures with network errors. All attempts retained, no
model calls or scored efficiency claim; no dropping controls/task replacement.
[Build/service repair](SWE-LITE-PILOT-01-SERVICES.md), attempt03: offline wheels
restore successful installation; pytest gold passes78/78 with the expected base
failure. Requests internal HTTP service reduces failures but gold still fails7
required checks. Both-task execution/access gates remain unfinished; no model run.
[Requests diagnosis](SWE-LITE-PILOT-01-REQUESTS-DIAGNOSIS.md): unchanged public
suite134pass/8fail identifies runner API, hostname/TLS and timeout-network causes.
Pinned pytest4.6.11 repairs the demonstrated string-raises case; actual pass/fail
assertion controls work. Combined service/scoring validation is still pending.

| Reviewed checkpoint / measured resource | Observed result | Decision |
| --- | --- | --- |
| [Probe-edit transfer01](PROBE-EDIT-TRANSFER-01-REVIEW.md), current`aed8a27` |6cells; current vs baseline full tokens−7.87%/time+67.29%, prefix+10.43%/+0.74%. Current costs more tokens/time than predecessor on both. All scoped native checks succeed; helper unused. | No API adoption or efficiency benefit; no promotion. |
| [All-eight regression04](ALL-EIGHT-CURRENT-04-REVIEW.md), `0d12dd9` |16cells; summed tokens+20.39%, time−5.17%. Scope included: baseline7/8,current8/8 because baseline SQLite searches outside the project. | Cost goal unmet; not a general quality advantage. This predates subsequent changes. |
| [Configuration audit01](CONFIG-LAYERS-01-REVIEW.md), `e1e1ef8` |4cells; single tokens+4.65%/time+2.26%, multiple+0.38%/−1.28%. Helper unused in both current sessions. Multiple/current incorrectly denies baseline reuse. | No efficiency promotion or unqualified task pass. Native checks/preservation hold; reporting defect retained. |
| [Packaging specifier01](PACKAGING-SPECIFIER-01-REVIEW.md), `c8fd471` |4cells; single tokens−18.53%/time−5.06%, multiple+5.39%/+13.84%. Helper unused; original806-test suite and requested faults run. | Mixed correlated pair, not a broad saving. Original initial-index identity is unproven. |

These are small author-selected/development experiments, not independent
generalization evidence. All attempts, adverse outcomes, original output gaps and
reviewed reconciliations remain in the linked reports. No replay substitutes for
original model evidence. The [regression04 cost analysis](ALL-EIGHT-04-INPUT-COSTS.md)
separates extra reads and legitimate verification; its arithmetic is not causal
or recoverable savings.

한국어: 전체 비교의 토큰 증가, 단일/다중 과제의 혼재된 결과, 스킬의 재사용 보고
오류를 모두 유지한다. 유리한 한 쌍이나 프로세스 감소를 전체 개선율로 확대하지 않는다.

## Implemented capabilities and local validation

These changes are implemented; their model-cost effect is not established:

- [Complete decorator excerpts](PYTHON-REGIONS-DECORATORS-01.md), parent`7d67eff`:
  multiline decorator openings no longer disappear from supposedly complete
  regions. Four new regression tests fail before repair; all18 region tests pass
  on3.11 afterward. This repairs source evidence, not model efficiency.
- Con Artist entrypoint now mentions localized exact edits in its existing
  optional four-check recipe route. In transfer01, predecessor/current entrypoints
  were identical and all four skill sessions stopped at that body without reading
  the supporting guide. This makes the capability visible earlier, not mandatory;
  it does not establish why models chose custom harnesses or that routing is fixed.
  The new wording is unmeasured; frozen results/charts remain unchanged.
- [Exact native probe edits](AUDIT-PROBE-EDITS-01.md), parent`23f06d2`:
  localized test changes need not resend unchanged file contents; four native
  checks and full materialized-byte budget/cache identity remain.128 audit controls
  pass on3.11; full checkout1,162/1,162 and archive new group7/7.
  No measured model adoption or efficiency effect.
- [Audit special-input rejection](AUDIT-SPECIAL-INPUTS-01.md), parent`74b674a`:
  initially selected FIFO/socket entries no longer disappear silently from copies;
  rejected before execution.121 audit and80 mutation-helper controls pass on3.11.
  Fresh source archive121/121 as well; correctness repair, not model-efficiency evidence.
- [Local CLI installation03](SKILLS-CLI-INSTALL-03.md), resource`8114957`:
  eight skills/51 resources match after actual local CLI copy; nine Python
  entrypoints and selected installed behaviors pass. Initial mount error retained;
  no remote-install, hosted-CI or model-efficiency claim.
- [Focused history hunk selection](HISTORY-HUNK-SELECTION-01.md), parent`c96730d`:
  slices retained hunks instead of copying every omitted body; exact evidence
  matches the old selector. Large sparse input reduces intermediate allocations,
  tiny-input memory increases;56 history controls pass. Not a model-cost result.
- [Mother request-entry cancellation](MOTHER-ENTRY-CANCEL-01.md), code`c00276d`:
  reproduced on Python3.9/3.11, then repaired without consuming pending requests.
  Native asset8/8 on both versions,38 Mother controls on3.11; source archive8/8.
- Con Artist reporting clarification at`eed4ff7`: a correct run used against
  several faults is reused evidence even in a custom harness, counted once.
  Addresses the configuration report defect; no favorable rerun or extra check.
- [Returning stronger-probe cache](AUDIT-PROBE-CACHE-02.md), code`b6df5f6`:
  bounded batch-local retention; authored alternating example25→19 native
  processes, adjacent control9→9. All mutant checks remain. Archive audit118/118.
  **24% fewer processes in that example is not24% fewer model tokens or seconds.**
- [Pytest batch routing](AUDIT-PYTEST-BATCH-ROUTE-01.md), code`22c0300`:
  existing pytest support distinguished from unittest-only module mode.
- [Initial index capture](INITIAL-INDEX-CAPTURE-01.md), code`6db0788`:
  before-model/pre-collector identity now recorded; missing capture stays unknown,
  byte changes alone are not automatic scope failures. No historical rescore.

한국어: 위 항목은 도구·안내·측정의 구체적 수정이다. 각각의 로컬 검증 범위와
커밋을 구분하며, 아직 측정하지 않은 모델 성능 효과를 주장하지 않는다.

## Avoid repeating rejected approaches

Reviewed [existing-file probe transfer01](PROBE-EDIT-TRANSFER-01-REVIEW.md):
all six use custom harnesses; the optional exact-edit API is not adopted.
Author preflight's smaller serialized requests are not model savings. Do not
force helper usage or rerun the same full/prefix tasks for a favorable outcome.

Reviewed [natural routing-boundary screen02](ROUTING-BOUNDARY-02-REVIEW.md):
three ordinary requests, unchanged bundle`ba477ae`, auto-only. All satisfy the
requested outcome without observed body reads or extra audit work; all eight
descriptions are present in initial context. No routing defect supports a change.
No baseline comparison, population-rate estimate or efficiency gain follows.

Before another edit, inspect the mechanism and prior outcomes:

- [Global lean rewrite](results/lean-screen-01/README.md): lean7/8 versus current8/8;
  still costs more than baseline. Do not repeat broad compression without new evidence.
- Receipt read-order/support-routing and repeated ledger tuning did not consistently
  lower cost. [History](CANDIDATE-HISTORY-2026-09-21.md) retains these attempts.
- [ZIP](ZIP-AUDIT-01-INPUT-COSTS.md), [slugify](SLUGIFY-NATIVE-01-INPUT-COSTS.md),
  and configuration audits do not justify forced helper adoption or another generic
  “read less/group more” rule. Native execution counts are not end-to-end costs.
- [EventEmitter](EVENTEMITTER-BOUNDARY-01-REVIEW.md) and
  [Hostage conditional](HOSTAGE-CONDITIONAL-01-REVIEW.md) candidates were not promoted.
  Required coverage must survive any reduction in output or test count.

Use existing `analyze_response_costs.py`, not another profiler. New performance
experiments need a distinct relevant workflow, frozen criteria, a simple control
and every scheduled attempt retained; exposed cases are not held-out validation.
Do not rerun a completed experiment until it becomes favorable.

## Release and publication boundary

[Current local checkpoint](RELEASE-VALIDATION-04741D7.md), source`04741d7`:
macOS/Python3.11 checkout1,179passes; Linux/Python3.12 archive1,150passes,
29historical skips, zero failures. Both exit0; overlapping durations are not
speed comparisons. Hosted main run35610526288 failed before all four jobs'
steps; Python3.11 again reports account payment/spending-limit alternatives.

[Combined local checkpoint](RELEASE-VALIDATION-9A84635.md), source`9a84635`:
1,155checkout passes on macOS/Python3.11.16; Linux/Python3.12.3 archive
1,127passes/28historical skips/0failures. Logs retained; overlapping durations
are not speed comparisons. This is not the complete hosted version matrix.
The newer [probe-edit resource](AUDIT-PROBE-EDITS-01.md),`37e62d2`, passes
all1,162 checkout checks on macOS/Python3.11.16 and its seven new archive checks;
the earlier Linux whole-suite result does not cover that new input form.
Earlier [macOS](RELEASE-VALIDATION-D97E971.md) and
[Linux](AUDIT-EMPTY-NATIVE-01.md) checkpoints retain their original revisions.

Hosted [run35604299489](https://github.com/SoonGwan/questionable-hires/actions/runs/35604299489)
at`9a84635`, rechecked2026-09-21, has four terminal failures with no executed
steps; its Python3.11 annotation cites payments/spending limit alternatives.
Do not change billing or visibility without owner direction.

Keep [featured.json](featured.json) tied to its frozen evidence. No result here
justifies replacing its graphs. Representative updates must synchronize both
README languages and generated charts using the existing synchronization script.

한국어: 전체 로컬 검사 결과는 명시한 이전 커밋의 결과다. 현재 전체 매트릭스,
원격 CI 성공, 공개 배포 승인은 별도 미완료 조건이다. 대표 그래프는 동결된
근거를 유지하며 수치만 독립적으로 바꾸지 않는다.

## Preserved history

[Full pre-reorganization status at bfcaae9](CANDIDATE-HISTORY-2026-09-21-B.md)
retains every former paragraph, including older positive, mixed and adverse
checkpoints, preparation notes and links.
[Earlier chronological history](CANDIDATE-HISTORY-2026-09-21.md) remains intact.
