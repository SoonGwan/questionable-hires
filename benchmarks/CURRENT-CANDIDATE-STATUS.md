# Current candidate: whole-task performance remains unproven

Checkpoint **2026-09-21, last model resource `99301e9`, ancestry launch `6baa5b7`**.
The earlier measured section-read candidate remains withdrawn, not relabeled.
This is a decision index, not a new
measurement. [Full chronological history](CANDIDATE-HISTORY-2026-09-21.md) preserves
every preceding checkpoint, including adverse results and preparation notes.
Use dated reports for exact tasks, resources, scope and capture limitations.

## Objective and unfinished requirements

All eight hires should improve real developer outcomes at similar or lower
token/time cost. Reliable helpers and passing tests do not establish that outcome.
A broad20–30% gain remains **unproven**. No independent generalization,
hosted-check success or public-release approval is claimed here.

한국어:8개 스킬 전체가 실제 개발에서 더 적거나 비슷한 비용으로 좋은 결과를 내는
목표는 아직 미달이다. 개별 과제·버전의 결과를 전체 성능으로 확대하지 않는다.
과거 실험과 불리한 결과는 이력 문서에 그대로 보존했다.

## Model evidence that governs claims

Reviewed checkpoint2026-09-21: [ancestry scope](ANCESTRY-SCOPE-01.md), all6
complete; all arms5/5 history and4/4 current-only. Current versus prior history
+26.06% tokens/+13.60% time, current-only−0.18%/−5.82%; versus baseline both cost
metrics increase on both tasks. One correlated authored pair, no advantage in
scope accuracy, no efficiency promotion. 한국어: 안내의 범위 준수는 확인했지만
비용 개선은 입증하지 못했다. 모든 시도와 원본 출력 대조를 보존했다.

Reviewed checkpoint2026-09-21: [urllib3 history](URLLIB3-HISTORY-01.md) retains
all three attempts. Prior/baseline5/5, candidate4/5 (non-ancestor history read).
Candidate versus prior−4.34% tokens/+4.56% time; versus baseline+39.55%/+26.14%.
Missing generated metadata affects all arms; import-retry preflight weakness and
capture/manifest omissions disclosed. Withdraw the candidate; no efficiency claim.
한국어: 수정본의 범위 위반·비용 증가와 준비 결함을 보존하고 후보 문구를 철회했다.

Reviewed checkpoint2026-09-21: [slugify history review](SLUGIFY-HISTORY-01.md)
retains both original attempts; both5/5. Current versus baseline tokens+34.32%,
time+13.97%; helper unused. Both invalid Git-option recoveries and current's
truncated whole-file read remain disclosed. No efficiency promotion.
한국어: 정확한 검토에도 비용이 증가했으며 새 전체 성능 개선 수치로 채택하지 않는다.

Reviewed checkpoint2026-09-21: [slugify native audit](SLUGIFY-NATIVE-01.md)
retains all three attempts; all arms5/5. Current versus prior tokens−22.19%,
time−1.80%, with fewer guide transitions; versus baseline tokens+36.55%,
time−15.53%. Keep recipe correction provisionally, not as a broad efficiency win.
한국어: 이전 안내 대비 개선을 관찰했지만 무스킬 대비 토큰 증가가 남았다.

Reviewed checkpoint2026-09-21: [dateutil native audit](DATEUTIL-NATIVE-01.md)
retains all three original attempts. All arms meet5/5; current uses the helper
and executes12 methods in8 rather than12 processes, but versus baseline total
tokens+51.37%, time−14.46%. No efficiency promotion. 한국어: 실제 도구 사용은
확인했지만 토큰 비용 목표에는 미달이며 전체 성능 향상으로 채택하지 않는다.

Reviewed checkpoint2026-09-21: [native edit audit](EDIT-AUDIT-01.md) retains all six
original attempts. Required outcomes hold, but helper use is absent and current
verified-request costs regress substantially. Setup recovery and different extra
checks remain included. 한국어:6회 검토 완료. 새 도구는 미사용이었고, 입증 과제의
비용 증가·복구·추가 검사도 보존했다. 전체 성능 향상으로 채택하지 않는다.

Transfer checkpoint2026-09-21, launch`557a021`: all six dependency-plan sessions
reviewed; originals/scope preserved. Prior's instrumentation repair and capture
prefix omissions remain in the [report](PLAN-AUDIT-01.md). 한국어:6회 검토를
마쳤고 기존 실행의 설정 실패·복구 비용까지 보존했다. 독립 평가로 주장하지 않는다.

| Dated checkpoint / resource | Observed result | Decision and limitation |
| --- | --- | --- |
| [All-eight screen03](results/all-eight-current-03/README.md),2026-09-20,`ee5eb28` | Both arms8/8; skill summed tokens+20.34%, time−3.61%; every pair uses more tokens | Efficiency target unmet. Eight exposed authored tasks,n=1; not a measurement of subsequent changes. |
| [Cachetools audit01](CACHETOOLS-AUDIT-01.md),2026-09-21,`b1875a0` | All three arms5/5; current versus baseline tokens−20.6%, time+30.9% | Changed helper unused; unequal extra checks. One source-excerpt task,n=1; no optimization attribution. |
| [Proposal boundary01](AUDIT-PROPOSAL-01.md),2026-09-21,`e17e13d` | Proposal: tokens−17.46%, time−8.48%,20→10 unittest processes. Verified: tokens+3.40%, time−3.34%; required assertions retained | Retain scope distinction provisionally. Two requests on reused development fixture,n=1; not independent validation. |
| [Plan audit01](PLAN-AUDIT-01.md),2026-09-21,`a3dee3b` | All arms meet5/5 proposal and6/6 verified criteria. Current versus baseline: proposal−11.39% tokens/−2.98% time; verified+12.83%/+9.02% | Scope distinction transfers in one fresh authored fixture; unequal probes and prior instrumentation repair. No broad efficiency win. |
| [Edit audit01](EDIT-AUDIT-01.md),2026-09-21,`e6aa16e` | All arms meet5/5 proposal and6/6 verified criteria. Current versus baseline: proposal+6.63% tokens/−18.67% time; verified+91.21%/+119.09% | Helper unused; current startup recovery and unequal extra work retained. No demonstrated efficiency improvement. |
| [Dateutil native01](DATEUTIL-NATIVE-01.md),2026-09-21,`387c53b` | All arms5/5; current helper used,12 methods in8 processes versus12; tokens+51.37%, time−14.46% versus baseline | Adoption but not efficiency target. Multiple guide reads; one author-inspected upstream subset,n=1. |
| [Slugify native01](SLUGIFY-NATIVE-01.md),2026-09-21,`a7dcbd8` | All arms5/5; current versus prior−22.19% tokens/−1.80% time; versus baseline+36.55%/−15.53% | Both skill arms use helper; baseline4 versus skill8 processes for12 methods. Recipe retained provisionally; broad efficiency unmet,n=1. |

한국어: 전체 비교에서는 토큰 증가가 남았다. 제안과 입증을 구분한 수정은 한 사례에서
추가 실행을 줄였지만 입증 과제의 토큰 증가도 공개한다. 독립적인 프로젝트에서
효과가 유지되는지는 아직 확인하지 못했다.

## Implemented capabilities and local validation

Checkpoint2026-09-21: [ancestry runner archive correction](ANCESTRY-ARCHIVE-01.md)
separates synthetic scheduling controls from real pinned-resource checks after
six source-archive setup errors were reproduced. Checkout10/10; fresh archive
Python3.9/3.11 each9pass/1historical skip. No skill or model-result change.
한국어: 압축본에서도 실행 제어 검증이 가능하도록 테스트의 Git 의존을 분리했다.

Checkpoint2026-09-21: [ancestry scope comparison preparation](ANCESTRY-SCOPE-01-PROTOCOL.md)
adds a merged-history request and correlated no-history control with native
pass/fail preflight. Nine fixture/runner tests pass; six-cell identity and exclusive
start controls are ready. This prelaunch checkpoint is not a model result.
한국어: 이력 안내 수정의 실제 효과를 검증할 두 과제와 실행 대조를 준비했다.
모델 성능 결과나 독립 실무 검증은 아니다.

Checkpoint2026-09-21: [explicit-base history recipe](NECROMANCER-ANCESTRY-01.md)
addresses observed invalid Git options and other-ref expansion with a native
command example. Real local merge-DAG controls verify command semantics, not
model adoption or cost savings. 한국어: 허용 이력 범위를 유지하는 명령을 안내하고
병합·다른 분기 대조로 검증했다. 모델 성능 개선은 아직 측정하지 않았다.

Checkpoint2026-09-21: [partial-package import correction](AUDIT-PARTIAL-IMPORT-01.md)
rejects cached listed submodules whose parent package is absent after failed
initialization. Local failing-first reproduction and valid-package control; no
new model measurement or efficiency claim. 한국어: 패키지 초기화 실패를 정상 감사로
오인하던 결함을 수정했다. 전체 성능 향상 수치로 환산하지 않는다.

- [Native bootstrap controls](URLLIB3-HISTORY-01.md): author diagnostics and
  two regression tests reproduce unittest import recovery hiding missing package
  metadata; the preparation rule now requires a separate fresh package import.
  Existing15 preflight assertions remain real, not cold-bootstrap proof.
  한국어: 실제 준비 취약점을 재현하고 검사 규칙을 보완했다. 모델 성능 수치와 구분한다.
- [Necromancer section-read candidate](NECROMANCER-SECTION-READ-01.md),`f53cb65`,
  withdrawn after the model result above. Prior entrypoint wording restored;
  helpers/probe safeguards unchanged. No favorable retry or chart promotion.
  한국어: 채택 조건을 충족하지 못한 문구는 원복하고 원본 측정은 보존했다.
- [Slugify history preparation](SLUGIFY-HISTORY-01-PREFLIGHT.md), checkout
  `79fb2e2`: nine native current/deletion controls and full-history attribution
  pass. New review task on the already-used project; no model sessions or skill
  change. Current compatibility and historical intent remain separate.
  한국어: 이력 검토 사전 검증이며 새로운 성능 향상 수치는 아니다.
- [Hostage entry-wait cancellation correction](HOSTAGE-ENTRY-CANCEL-01.md),
  parent `b9a2900`: plain callback-entry wait no longer swallows cancellation
  overlapping queue wakeup in the tested Python3.9/3.11 runtimes. Both reproduce
  the failure before the fix and pass18 controls afterward; owned-task11,
  usage1, build13/archive4 pass. No model-cost claim or new full-suite run.
  한국어: 취소 경계의 실제 결함 수정이며 전체 성능 개선 수치와 구분한다.
- [Whole-checkout validation](CHECKOUT-VALIDATION-2026-09-21.md), code/tests
  `79fb2e2`: Python3.11.16,1,054 tests in179.540s, no failures/skips. Includes
  both new entry-wait controls; the earlier1,052-test checkpoint is preserved
  in the report. Local regression evidence, not model or hosted validation.
  한국어: 최신 전체 로컬 검사 통과이며 성능 향상 증거와 구분한다.
- [Slugify transfer preparation](SLUGIFY-NATIVE-01-PREFLIGHT.md), helper
  `a7dcbd8`: unchanged pinned upstream tests establish correct/equivalent/fault
  outcomes in20 direct processes;8 helper processes execute12 methods with
  matching results and cleanup. No model calls at that preparation checkpoint;
  subsequent model comparison is above. 한국어: 준비와 이후 모델 측정을 구분한다.
- [Native existing-test recipe correction](AUDIT-NATIVE-RECIPE-02.md), parent
  `df072b3`: source-root and existing-witness selections are self-contained in
  the native guide. Real packaged weak/strong controls pass on Python3.9/3.11;
  no runtime change or model measurement at that checkpoint; see slugify above.
  This longer recipe aims to avoid
  unnecessary document transitions, not to establish token savings by byte count.
  한국어: 안내 수정 당시에는 미측정이었고 후속 slugify 비교는 위에 구분했다.
- [Dateutil native transfer preparation](DATEUTIL-NATIVE-01-PREFLIGHT.md),
  helper `387c53b`: unchanged pinned upstream test/source files pass25 direct
  controls and8 helper executions with matching selected-test outcomes, real
  assertion failures and cleanup. Author-selected development cases; no model
  sessions at that preparation checkpoint. Subsequent model comparison is above.
  한국어: 준비 당시에는 호환성 대조만 완료했고 이후 모델 비교는 위에 구분했다.
- [Native audit discovery correction](AUDIT-NATIVE-ROUTE-01.md), parent `1fa230c`:
  entrypoint exposes the supported module command and a complete batch recipe.
  The actual bundled recipe passes weak/strong assertion controls on Python3.9/3.11;
  build13/archive4 pass. That checkpoint had no model measurement; see the
  subsequent dateutil comparison above. Existing
  project support, simpler checks and justified inspection remain valid choices.
  한국어: 안내·예제 검증 완료이며 모델 성능 수치로 채택한 결과가 아니다.
- [Con Artist module invocation](AUDIT-MODULE-01.md), parent `04bf934`: optional
  instrumented `python -B -m unittest` checks preserve native result evidence,
  probes and batch reuse. Twelve controls pass on Python3.9/3.11, including the
  reused planner fixture. No new model session or token/time improvement claim.
- [Con Artist empty-mutant correction](AUDIT-EMPTY-MUTANT-01.md), parent `bd238f1`:
  five real-process control failures now stop as incomplete, including native
  probes and batches. Four Python3.11 test methods pass; Python3.9 skips the
  pytest-dependent method. Module invocation was unsupported at that checkpoint;
  the separately validated capability above follows it. No model-cost claim.
- [Receipt selected-read correction](RECEIPT-SELECTED-READ-01.md),`a3dee3b`:
  reproduced FIFO blocking plus accepted link/regular replacements; all three
  now reject at the observed open boundary. Python3.11 Receipt175/build13 and
  Python3.9 helper49 plus race test pass. Same-inode writes and parent races
  remain limitations. No token-saving claim.
- [Con Artist baseline reuse](AUDIT-SELECTION-REUSE-02.md),`b1875a0`: alternating
  selections reduce native executions16→10 while preserving all8 mutant checks.
  [Native timing](AUDIT-SELECTION-TIMING-01.md):0.7080→0.4525s on that authored
  workload. Not whole-task/model efficiency.
- Whole-checkout checkpoint at`c258570`: Python3.11.16,1,035 tests in175.415s,
  no failures/skips. Includes Receipt's selected-read correction, plan-audit
  fixture/runner controls and Con Artist's empty-mutant/module-mode corrections.
  Earlier module-mode run had a packaging failure, retained in its report; the
  final rerun passes. Local tests do not establish hosted CI success or improved
  model performance.
- Source archive at`ac1d17c`:994 discovered,22 skipped,no failures. This does not
  establish archive validation of`a3dee3b`. Both detailed test checkpoints remain
  in the [history](CANDIDATE-HISTORY-2026-09-21.md).

한국어: 도구 신뢰성과 특정 배치의 반복 실행은 개선했다. 관련 검사, 전체 검사,
소스 압축본 검사는 서로 다른 범위·커밋의 결과이므로 구분한다.

## Avoid repeating rejected approaches

The [all-eight lean experiment](results/lean-screen-01/README.md) already tested
a broad entrypoint rewrite: lean7/8 versus current8/8, with higher cost than the
baseline. Astra's [current design guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
supports contextual instructions, not treating another global compression as a
proven fix. Do not repeat that strategy without a distinct observed mechanism.

The [slugify remaining-cost diagnosis](SLUGIFY-NATIVE-01-INPUT-COSTS.md) reconciles
the31,063-token baseline gap with the existing response analyzer. It does not
attribute causal savings or justify a new grouping API from child-process counts.
Six roles changed since the last all-eight resource; do not relabel that old
measurement as current. 한국어: 실행 수 감소와 전체 비용 절감을 구분한다.

Reuse [the existing cost analysis](ALL-EIGHT-03-INPUT-COSTS.md) and
`analyze_response_costs.py`; no second profiler is needed. Its arithmetic is not
causal savings. Initial instructions, evidence, source reads and generated work
all contribute to repeated input.

- Receipt read-order/support-routing experiments and transfer limits remain in
  the history. Omitting implementation reads did not consistently reduce cost;
  do not retune the exposed ledger case with another generic “read less” rule.
- [EventEmitter completion candidate](EVENTEMITTER-BOUNDARY-01-REVIEW.md) passed
  criteria but increased both costs on both tasks; not promoted.
- [Hostage conditional candidate](HOSTAGE-CONDITIONAL-01-REVIEW.md) and historical
  reporter experiments retain adverse results. Smaller output or fewer methods
  do not establish equivalent coverage or measured savings.

Before another edit, identify an unresolved mechanism and check prior attempts.
New performance experiments need a different relevant task plus controls,
frozen criteria and every scheduled attempt retained. The known proposal case
is a regression control, not an independent test set.

한국어: 같은 읽기 안내·출력 축소 후보를 반복하지 않는다. 기존 실패 실험부터
확인하고 새 근거가 있을 때 수정한다. 다른 과제와 필수 검증 대조가 필요하다.

## Release and publication boundary

Hosted checkpoint inspected2026-09-21:
[run35584332665](https://github.com/SoonGwan/questionable-hires/actions/runs/35584332665)
at`faab9e2` has no executed steps in all four jobs; the Python3.11 annotation
cites payments/spending limit. Local results do not
establish hosted validation. Do not change billing/visibility without owner
direction; scoped local work can continue.

Keep `featured.json` tied to its frozen evidence. Representative changes require
reviewed data and synchronized English/Korean text/charts. No small checkpoint
above independently justifies replacing it.

한국어: 최신 확인 실행도 결제·한도 사유로 시작되지 않았다. 호스팅 검사 성공과
공개 배포 승인은 미확인이며 계정 설정·공개 여부도 임의로 바꾸지 않는다.
대표 그래프는 검토된 자료와 두 언어를 함께 갱신할 때만 변경한다.
