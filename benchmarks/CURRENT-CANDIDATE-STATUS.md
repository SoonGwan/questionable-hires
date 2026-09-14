# Current candidate: whole-task performance remains unproven

The objective covers all eight hires: materially better real developer outcomes
at similar or lower token/time cost. Reliability fixes, passing tests and helper
microbenchmarks do **not** satisfy that objective. Recent work strengthens tools;
it has not established a broad 20–30% gain.

한국어 요약: 최근 오류 방지·도우미 개선은 검증됐지만, 8개 스킬 전체가 실제
개발에서 더 적은 토큰과 시간으로 좋은 결과를 낸다는 목표는 아직 미달이다.
개별 유리한 수치와 전체 성능을 구분하고, 불리한 결과도 그대로 보존한다.

## Latest reviewed checkpoint — 2026-09-14, launch `b2816cd`

Current unmeasured instruction candidate: [state-content checks](HOSTAGE-STATE-CONTENTS-01.md)
address the preview aliasing blind spot below. Five native author-copy runs show
field snapshots accept both correct state replacement and correct in-place
updates, while detecting stale in-place success/error. Frozen original tests
still reproduce the escape. Runtime assets unchanged; no fresh model evidence
for the new instruction yet, so earlier costs/outcomes are not relabeled.
Full current local validation: 476 tests passed in 65.156s, no failures/skips.

한국어: 현재 지침은 상태 객체 자체가 아니라 관련 필드 값을 전후 비교하도록
보강했다. 작성자가 고친 테스트 복사본은 정상적인 두 구현 방식을 허용하고
잘못된 내부 값 변경을 잡는다. 새 지침을 모델이 적용한 결과는 아직 없으므로
이전 실패 기록과 성능 수치는 그대로 유지한다.

[Two-stage preview transfer reviewed](HOSTAGE-JAVASCRIPT-PREVIEW-01-REVIEW.md),
launch `4a064bc`, resource `f0b29dd`: baseline 109,445 tokens/214.251s; skill
125,009/146.851s, **+14.22% tokens / −31.46% time**. Both implementations correct;
original native final counts 33/33 versus 54/54. Skill first repairs two failures
in its own undefined-reason assertion helper. Eighteen initial replays match and
raw/resources/originals reconcile. However, a separate four-run counterexample
finds stale success mutating state in place: baseline detects 11 failures, while
skill remains 54/54 green. Object identity alone misses changed state contents.
No scope/capture exception observed. Do not promote timing as an accepted overall
gain; fix demonstrated regression weakness next. Full preflight 473/473 passed,
but local fixture tests did not themselves prove model regression strength.

한국어: 두 단계 미리보기 비교도 끝났다. 시간은 31.46% 줄었지만 토큰은 14.22%
늘었다. 더 중요한 문제는 상태 객체의 내용만 덮어쓰는 결함을 스킬 테스트가
놓친다는 점이다. 기본 실행은 11개 테스트로 잡았고, 스킬은 54개가 모두 통과했다.
최종 구현 자체의 오류는 아니지만 회귀 검증의 실제 약점이므로 이를 먼저 고쳐야
한다. 좋은 시간 수치만으로 개선 성공을 주장하지 않는다.

[JS usage-first screen](HOSTAGE-JAVASCRIPT-USAGE-MODEL-01-REVIEW.md), launch
`8d21e74`, resource `f0b29dd`: baseline 87,491 tokens/92.970s, skill 114,460/86.698s,
**+30.82% tokens / −6.75% time**. The 42-line usage read is actually adopted;
whole-task token reduction is not. Original native tests pass 6/6 versus 7/7
(different grouping), required transitions preserved, ten separate fault replays
match. Raw events/resources, exact inventories, unchanged originals and copied
asset reconcile; no scope/test-capture exception observed. Skill also prints its
new test file during final review. One exposed authored pair, unequal extra work,
shared host/cache. Move to a different workflow, not favorable-repeat fishing.

한국어: 사용법만 먼저 읽는 동작은 실제로 확인했지만, 이번 비교에서도 토큰은
30.82% 더 썼고 시간은 6.75% 줄었다. 요구 동작과 원래 테스트를 보존했고 별도
결함 대조군 10개도 확인했다. 이 과제에서 유리한 숫자가 나올 때까지 반복하지
않고 다른 작업으로 검증을 넓혀야 한다. 전체 효율 목표는 아직 미달이다.

[JavaScript lifecycle model screen](HOSTAGE-JAVASCRIPT-SCOPE-MODEL-01-REVIEW.md),
launch `330a17b`, resource `22bd929`: baseline 104,047 tokens/99.788s; skill
115,286/93.105s, **+10.80% tokens / −6.70% time**. Both capture seven native passes
and all required transitions. Skill actually uses the wrapper instead of writing
scenario/deadline machinery: new test file 136 versus 174 lines, but copied
support adds 162 lines; do not claim lower total code size. Ten separate fault
replays match; raw events/resources and unchanged original tests reconcile.
No scope/capture exception observed. n=1 exposed authored pair, unequal extra
witnesses and shared host/cache; no broad efficiency win. Full local preflight:
470 tests passed in 68.700s, no failures/skips, including helper/native controls.

한국어: 새 정리 도구를 실제로 사용한 비교도 끝났다. 토큰은 10.80% 더 썼고
시간은 6.70% 줄었다. 직접 작성한 테스트는 174줄에서 136줄로 줄었지만 복사한
도구 162줄이 추가되므로 전체 코드가 줄었다고 주장하지 않는다. 양쪽 기존
테스트 보존·7개 통과 및 별도 결함 대조군 10개를 확인했다. 과제 하나의 결과이며
일반적인 효율 개선은 아직 입증되지 않았다. 아래 결과는 이전 도구의 기록이다.

[JavaScript SubmitPanel review](HOSTAGE-JAVASCRIPT-PANEL-01-REVIEW.md), launch
`3949ef6`, resource `8ca9e70`: both sessions complete. Baseline 68,671 tokens/
92.478s; skill 132,886/102.947s: **+93.51% tokens / +11.32% time**. Both preserve
existing tests and capture seven native passes. Skill copies the JS asset exactly,
but still builds lifecycle setup and makes more separate discovery/read calls.
Ten separate final/original/guard/cleanup/signal replays match, all raw resources/
usage and reviewed inventories reconcile. No observed scope/capture issue.
Adoption is demonstrated; efficiency is not. One authored n=1 pair, unequal extra
witnesses and shared host/cache remain limitations. No browser/TypeScript claim.

Local capability/preflight: seven native asset tests, independent copy/installer
checks, and author panel contract/fault controls passed. Full repository preflight
was 469 tests in 70.708s, no failures/skips; that is not model performance evidence.
Python support and historical/featured measurements remain unchanged.

한국어: JavaScript 비교 두 세션이 끝났다. 기존 테스트를 보존하고 양쪽 모두
7개 테스트가 통과했지만, 스킬은 토큰 93.51%, 시간 11.32% 더 썼다.
도구를 그대로 사용했어도 별도 정리 코드와 반복 읽기가 남았다. 원본 사용량·
도구·파일을 대조했고 별도 결함 대조군 10개도 예상대로 동작했다.
도구 사용 성공을 효율 개선으로 보지 않으며, 브라우저 검증을 주장하지 않는다.

Friday compact candidate rejected after [direct comparison](FRIDAY-COMPACT-MODEL-01-REVIEW.md),
launch `ce6dd4e`: all six sessions complete. Original 235,749 tokens/172.655s;
candidate 285,990/170.225s: **+21.31% tokens / −1.41% time**. Raw usage/resources
and unchanged fixture inventories reconcile. Candidate's parent-rooted discovery
remains a scope exception; control's large combination count is not a utility
gain. Original's acknowledgment-before-commit concern is a supported condition
under missing caller semantics, not an invented synchronization defect.
Restoration `f73c0a3` returns Friday's entry to the measured original, with other
resources unchanged. No causal/general claim from n=1, unequal work or shared
host/cache; failed candidate and all metrics remain available.

Post-rejection local suite: 461 tests pass in 71.013s. Three additional
[commit-boundary author checks](FRIDAY-WRITER-PROTOCOL.md#post-run-acknowledgment-ambiguity--2026-09-14)
pass in 0.019s, verifying actual cross-connection visibility before/after commit,
committed gap/control rollback and a native wrong-claim failure. These checks
clarify the historical fixture's limits, not new model performance; no measured
input or score was rewritten.

한국어: Friday 축약본의 직접 비교 6개 세션이 끝났다. 합계 토큰 21.31% 증가,
시간 1.41% 감소로 효율 개선에 실패했고, 상위 폴더 탐색 문제도 남았다.
원본 사용량·도구·파일을 대조한 뒤 `f73c0a3`에서 기존 지침으로 복구했다.
조합 검증을 많이 했다는 이유로 더 유용하다고 보지 않으며, 실패한 후보와
응답·커밋 명세의 불명확한 부분도 보존한다. 아래 전체 비교는 여전히 유효한
역사적 측정이며, 새롭고 일반적인 성능 향상 주장은 아니다.
복구 후 전체 로컬 테스트 461개가 통과했다. 별도 추가한 3개 검증은 함수
반환과 커밋의 차이를 실제 연결 두 개로 확인하며, 과거 평가 점수나 모델
출력을 바꾸지 않는다.

[Checkpoint 07](BUNDLE-CONTRACT-07-REVIEW.md), resources `32bf8bd`: all 18 serial
sessions across nine fixed tasks completed, no timeouts/exclusions. Baseline
752,577 tokens/557.433s; skill 748,449/440.164s: **−0.55% tokens / −21.04% time**
by ratios of sums. Raw usage/resources and reviewed inventories reconcile;
20 separate native author controls match with retained tests unchanged. The
persistence baseline's tracing repair and missing output remain disclosed.
Three pairs are adverse on both costs; five use more tokens. Exposed authored
n=1 tasks, shared host/cache and unequal extra work do not establish a causal or
broad 20–30% efficiency gain. Featured figures remain fixed. Following targeted
screens and checkpoint 06 are historical evidence, not today's headline result.

한국어: 전체 8개 스킬의 9개 과제·18개 세션이 모두 완료됐다. 합계 기준
토큰 0.55%, 시간 21.04% 감소지만, 3개 비교는 양쪽 비용이 모두 늘었다.
원본 사용량·도구·파일을 대조했고 별도 결함 대조군 20개도 예상 결과와
일치했다. 반복 1회·작성자 제작 과제·추가 검증량 차이 때문에 일반적인
21% 성능 향상으로 홍보하지 않는다. 원본 출력 누락과 과거 결과는 보존한다.

Instruction `6d733b9`: [Hostage single-read interface](HOSTAGE-SINGLE-READ-01.md)
routes directly to the callback asset with usage/limits in its module docstring.
Executable AST matches frozen `d9e7711`; eight native asset and 15 installer tests
pass. Old reference links remain valid. [Model screen](HOSTAGE-SINGLE-READ-MODEL-01-REVIEW.md)
confirms batched project/entry/asset read without opening the redirect. Baseline
87,216 tokens/88.793s; skill 92,819/82.136s (**+6.42% / −7.50%**). Required
transitions remain covered despite grouped subtests; extra witnesses differ.
Both standalone test summaries pass but have partial headers. Eight separate
replay controls match and raw/resources/inventories reconcile. Not a general or
causal efficiency win; earlier adverse evidence and featured numbers stay fixed.

한국어: 호출 제어 도구의 사용법과 구현을 한 파일에서 확인하도록 연결을
줄였다. 새 모델은 프로젝트·지침·도구를 함께 읽고 필요한 검증을 유지했다.
토큰은 6.42% 증가, 시간은 7.50% 감소로 전체 효율 향상은 아직 아니다.
원본 개별 테스트 출력 일부 누락은 별도 재실행 결과로 대체하지 않는다.

Reviewed transfer probe: [keyed publication screen](HOSTAGE-KEYED-PUBLISH-01-REVIEW.md)
tests same-document suppression without blocking other keys/instances. The new
author-written fixture is not independent holdout. Launch `a1a258c`, skill
`7dd4b56`, callback asset `d9e7711`: baseline 104,309 tokens/92.624s; skill
130,644/99.704s (**+25.25% / +7.64%**). Both produce identical implementation;
asset adoption transfers but costs more. Skill captures standalone nine-pass
summary/exit with partial headers; baseline lacks the full-suite section. Eight
separate native replay outcomes match; originals/resources/usage reconcile.
Replay cannot repair original capture gaps and no efficiency win is accepted.

한국어: 같은 문서만 중복 발행을 막고 다른 문서는 동시에 처리하는 새 과제를
실행했다. 스킬은 도구를 활용하고 동일한 구현을 만들었지만 토큰 25.25%,
시간 7.64% 증가했다. 스킬의 단독 테스트 명령은 9개 통과 요약·종료 상태를
남겼으나 개별 출력은 일부 누락됐다. 별도 결함 대조군 검증은 원본 누락을
대신하지 않으며, 작성자 제작 과제를 독립 평가로 보지 않는다.

New Hostage instruction/collector candidate: [verification delivery](HOSTAGE-VERIFICATION-DELIVERY-01.md)
requires test-specific result evidence before a pass claim and adds a review-only
missing unittest summary diagnostic. The retained gap is detected without changing
old metadata, completion or scores; native/redirected/unrun controls remain distinct
from proof of capture loss. The keyed screen above observes standalone test
status, without isolating this instruction's causal effect or showing efficiency.
Full local suite: 454 tests pass in 80.333s, no failures/skips.

한국어: 테스트 자체의 종료 상태와 실행 결과를 확인하도록 마무리 지침을
보완했다. 벤치마크도 테스트 요약이 없는 명령을 검토 대상으로 표시하며,
출력 누락·테스트 실패를 자동 확정하거나 과거 결과를 수정하지 않는다.
위 문서별 발행 실험에서 단독 테스트 상태는 확인했지만 이 지침만의 효과를
분리하지 않았고 비용 절감도 입증하지 못했다.

Hostage candidate `d9e7711`: [controlled callback test support](HOSTAGE-CONTROLLED-CALL-01.md)
replaces repeated asyncio entry/release gates only where equivalent project support
is absent. Seven native tests and 15 installer tests pass, including standalone
copying and the retained real Form's valid/missing-guard controls. Application
assertions and owned task cleanup remain explicit test responsibilities. No model
cross-task efficiency evidence yet; featured data is unchanged.
Full local suite passes 452 tests in 71.363s with no failures/skips.
[Model screen](HOSTAGE-CALL-MODEL-01-REVIEW.md) confirms asset adoption and retained
actual Form tests. Baseline times out at 240.017s with unknown usage/no edits;
skill finishes at 89,337 tokens/112.795s but original test output is absent despite
a six-pass claim. Separate unchanged-test replay passes final and rejects original,
missing-guard and missing-cleanup controls. Raw/resources/inventory reconcile;
replay does not fill the original evidence gap. No efficiency comparison accepted.

한국어: 범위 협상가에 선택형 비동기 호출 제어 도구를 추가했다. 실제 호출의
시작·결과·오류를 제어하며 앱의 상태·중복 방지 판단은 테스트에 남긴다.
새 모델 실행에서도 도구를 사용했지만 기준 실행은 시간 초과했고, 스킬의
원본 로그에는 테스트 출력이 빠져 있다. 별도 재실행에서는 6개 통과와
결함 대조군 검출을 확인했으나 원본의 누락을 대신하지는 않는다. 비용 절감
비교는 인정하지 않으며 기존 프로젝트 도구가 있으면 그것을 우선 사용한다.

Instruction `e0956d5`: [Friday result reuse](FRIDAY-RESULT-REUSE-01.md)
moves the existing Python API/BLOB contract into the core interface so computed
comparisons can reuse the first execution. Runtime remains `e3bc342`; 41 Friday
tests pass, including the documented snippet with one SQLite connection and all
binary current-value comparisons. [Fresh screen](FRIDAY-RESULT-REUSE-MODEL-01-REVIEW.md)
confirms one API execution with retained-row comparisons. Baseline 66,530 tokens/
64.128s versus skill 92,665/65.436s (**+39.28% / +2.04%**), so efficiency is not
accepted. Both required outcomes are supported, but verification work differs;
one exposed pair is not causal/whole-bundle evidence. Both cells/resources/raw
usage reconcile. Earlier model outputs and featured data remain unchanged.

한국어: 첫 실행 결과로 값 비교까지 할 수 있도록 API 예제를 기본 안내로
옮겼다. 새 모델 실행에서도 API 결과 재사용과 중복 실행 제거를 확인했다.
다만 토큰 39.28%, 시간 2.04% 증가로 효율 향상은 아니다. 이 과제만 계속
최적화하지 않고 다른 스킬의 실사용 비용·실패 근거로 개선 범위를 넓힌다.

Runtime `e3bc342`: [Friday phase defaults](FRIDAY-PHASE-DEFAULTS-01.md)
allows omitted empty `files`/`sql`, correcting the observed API preparation
failure without relaxing unknown-key/type/path/budget checks. Native regression
fails on the preceding runtime and passes after the patch; 40 Friday tests pass.
Full local suite: 444 tests pass in 71.433s, no failures/skips.
[Fresh model screen](FRIDAY-PHASE-DEFAULTS-MODEL-01-REVIEW.md), launch `90d703a`,
confirms first-call adoption of omitted `sql` with no preparation repair. Baseline
66,514 tokens/68.346s versus skill 111,170/70.479s (**+67.14% / +3.12%**).
The skill then duplicates SQLite execution for native comparisons. Both outcomes
are supported; unequal work and n=1 prevent efficiency acceptance. All raw usage,
resources and original snapshots reconcile. No exclusions or featured changes.

한국어: 파일 또는 SQL만 실행할 때 빈 항목을 생략할 수 있게 수정했다.
이전 버전의 오류 재현과 수정 후 실행은 검증했으며 잘못된 입력 검사는
유지했다. 새 세션에서도 빈 항목 생략은 첫 실행에 성공했지만, 별도의
바이트 비교를 위해 SQLite를 다시 실행했다. 전체 토큰 67.14%, 시간 3.12%
증가로 효율 향상은 아니며, 중복 실행을 다음 개선 대상으로 확인했다.

Instruction candidate `1c483b9`: [Friday interface split](FRIDAY-INTERFACE-01.md)
keeps CLI contracts/limits in the core guide and routes API/BLOB/byte-accounting
details conditionally. Core 3,733 bytes versus previous 6,447; combined documents
6,554 bytes. This is file size, not model savings, and advanced use can cost an
extra read. 35 Friday and 15 install tests pass; runtime remains `bef0937`.

[Interface model screen 01](FRIDAY-INTERFACE-MODEL-01-REVIEW.md), launch `15797aa`,
runtime `bef0937`: all four cells complete across two exposed tasks, n=1 per arm.
Baseline 132,229 tokens/134.346s; skill 222,886/145.651s (**+68.56% tokens,
+8.41% time**). Core-only versus conditional advanced loading was adopted, but
the binary API probe needed a real in-session repair for omitted empty `sql`.
Unequal verification work and shared host/cache prevent causal attribution.
Raw usage, resources and exact unchanged fixtures reconcile. No efficiency win;
no exclusions, retries or featured changes.

한국어: 기본/고급 문서를 나누어 읽는 동작은 확인했지만, 두 과제의 전체
토큰은 68.56%, 시간은 8.41% 증가했다. 빈 `sql` 누락으로 전체 코드를 다시
실행한 실제 오류도 보존했다. 검증량 차이가 있어 원인별 효과는 단정하지
않으며, 개별 유리한 시간만 대표 성과로 쓰지 않는다.

New runtime candidate `bef0937`: [Friday literal-reader references](FRIDAY-LITERAL-READERS-01.md)
replace custom extraction code for declaration-only Python query files via the
existing matrix CLI/API. Static file/hash/line evidence and strict rejection of
dynamic modules preserve the boundary; runtime consumer binding is not inferred.
28 native matrix tests pass, including the existing release fixture through CLI;
the full local suite passes **438 tests in 77.427s**, no failures/skips.
[Model screen 01](FRIDAY-LITERAL-MODEL-01-REVIEW.md) now confirms CLI adoption:
baseline 65,534 tokens/55.285s versus skill 72,134/41.615s (**+10.07% tokens,
−24.73% time**). Both support the required outcomes, with unequal extra checks.
All originals/resources reconcile. One exposed task at n=1 is mixed evidence,
not causal or all-eight efficiency; historical/featured data stays unchanged.

Newer **candidate `07fa9e2`**: [discovery routing screen](DISCOVERY-ROUTING-01-REVIEW.md)
retains all four attempts. Atomic baseline 83,380 tokens/49.277s versus skill
89,568/87.526s (**+7.42%/+77.62%**, extra exception coverage). Store baseline
65,155/83.303s completes; skill times out at 240.027s after a connection-reset
event, with native checks but no final recommendation or terminal usage. No
aggregate token ratio, retries or inferred cause. All raw/resources reconcile;
four unchanged-test author replays match. No demonstrated efficiency improvement;
the all-eight measurements below still belong to `20ec916`, not this candidate.

한국어 후보 검증: 새 탐색 지침의 4개 시도 중 3개가 완료됐다. 파일 내보내기는
스킬의 토큰·시간이 늘었고, Store 검토는 연결 오류 후 제한 시간에 도달해 최종
답변·사용량이 없다. 네 가지 별도 재실행 검증은 통과했지만 성능 개선 증거는
아니다. 실패를 제외하거나 누락된 토큰을 0으로 집계하지 않는다.

Completed [all-eight checkpoint 06](BUNDLE-CONTRACT-06-REVIEW.md): all 18 cells,
zero timeouts/exclusions. Baseline **713,178 tokens / 511.591s**, skill
**686,327 / 418.570s**: ratio-of-sums **−3.76% tokens / −18.18% time**. Five pairs
are adverse on both costs. Original streams/usage/resources reconcile, and 12
post-timing controls match, including transient-fault rejection and acceptance of
valid guards with unchanged QA tests. Persistence baseline still lacks leading
native output. Unequal work, shared host/cache and nine exposed tasks at n=1
preclude broad/causal claims. Helper adoption is observed for mutation, controlled
QA and SQL matrix, but not isolated pipe-fix savings. Featured data is unchanged.

한국어 최신 현황: 18개 실행과 별도 대조 검증 12개를 완료했다. 합산 토큰은
3.76%, 시간은 18.18% 감소했지만 다섯 과제에서는 둘 다 늘었다. 작업량 차이,
baseline 한 건의 원본 출력 누락, 이미 노출된 소규모 과제라는 한계가 있어
전반적 20~30% 개선으로 주장하지 않는다. 대표 그래프도 그대로 유지한다.

## Earlier runtime checks and model checkpoints

2026-09-14 [Linux archive check](LINUX-ARCHIVE-430-01.md) at `a81692f`: **428 passed,
two explicit provenance skips out of 430**, 60.274s. Network-disabled source
distribution, existing dependencies, no Git/local-run state or overlays. The
initial one-test failure is preserved; a task-ownership assumption in the test
was corrected, with runtime skill code unchanged. No model-performance claim.

2026-09-14 Con Artist runtime update `ea28d0e`: [native audit pipe completion](CON-ARTIST-PIPE-EXIT-01.md)
fixes reproduced baseline timeouts after direct-runner exit. Weak-test survival
with stronger-probe rejection and sensitive-test mutant rejection now complete.
Five focused tests pass; full local suite passes 430 tests in 145.613s. Copied-import evidence, selected
original preservation and scratch cleanup remain. No model savings claim.

2026-09-14 Receipt runtime update `a869f62`: [inherited-pipe comparison completion](RECEIPT-PIPE-EXIT-01.md)
fixes a reproduced abort after the native before runner had already finished.
The same integration regression now obtains before AssertionError and after pass,
preserving copied-import output, originals and scratch cleanup. Five focused tests
pass; full local suite then passes 429 tests in 147.545s. Background lifetime changes explicitly; no
model-session speed/token result or Con Artist fix is implied.

2026-09-14 local regression checkpoint, launch `ead49db`: **428 tests passed in
169.970s** (macOS/Python 3.9.6). No failures/skips reported; no concurrent model
run or executable edits. This verifies local regression coverage, not broad model
performance. The [current hosted run](../docs/RELEASE-READINESS.md) still cannot
start test steps because of an account payment/spending-limit restriction.
No account settings changed; earlier platform checks remain historical.

2026-09-14 runtime update `b861c4e`: [Exorcist foreground-exit cleanup](EXORCIST-PIPE-EXIT-01.md)
starts group cleanup when the direct command exits, rather than waiting for an
inherited descendant pipe until timeout. Three local repetitions fall from about
2.003s to 0.107s while retaining direct exit/output; background lifetime is shorter.
15 runner and four related tests pass. No model adoption, general speed or token
savings claim; process-group/cleanup limitations remain.

Completed 2026-09-14: [Necromancer multi-decision screen](NECROMANCER-REGIONS-01-REVIEW.md)
at `667eb10`: two complete cells, **−15.85% tokens / −18.56% time**. Both support
all three decisions with actual history and a 27-combination consumer matrix.
Baseline adds per-variant native suites; skill still repeats discovery. No observed
capture gap, but unequal work and one exposed task at n=1 preclude causal or broad
efficiency claims. Previous entrypoint timeout remains preserved.

2026-09-14 harness update: [native transcript review diagnostic](NATIVE-CAPTURE-REVIEW-01.md)
flags possible verbose unittest summary/header mismatches for manual review.
It locates the two already-reviewed interval capture gaps without changing old
metadata or scoring. Nineteen local runner tests pass; this is not model evidence,
a capture-loss repair or skill efficiency progress.

Completed 2026-09-14: [Mother work-selection comparison](MOTHER-INTERVAL-02-REVIEW.md)
at `160ff71`: four cells, **−14.54% recorded tokens / +83.52% time**. Both skill
cells avoid unrelated repeated-key/assertion-library extras. Separate unchanged-test
replay retains fault rejection and valid-fix acceptance. One original test output
is absent; another skill cell records connection resets. Initial author discovery
missed nested tests; both that record and corrected explicit-discovery evidence
are preserved. No overall efficiency acceptance or broad claim; n=1 exposed tasks.

Completed 2026-09-14: [interval-contract comparison](MOTHER-INTERVAL-01-REVIEW.md)
at `14289df`: four cells, **+9.32% tokens / +10.58% time**. The skill adopts
continuous retention assertions without constraining permitted intermediate
display in the final-only task. Eight separate unchanged-test author replays
reject the transient fault and accept the guarded correction in both arms.
Both original skill transcripts lack earlier per-test output; replay does not
repair those gaps. Runtime helper code is unchanged. Specific coverage improves,
but efficiency remains unaccepted; prior evidence and featured charts remain.

Completed 2026-09-14: [Mother delivery-route comparison](MOTHER-ROUTING-01-REVIEW.md)
at `672e22f`: four cells, **+7.92% tokens / −23.35% time**. Both document routes
are followed, but native-test costs increase and unchanged-test author replay
exposes missing intermediate-retention assertions. Both original implementations
are correctly reported clean; that does not establish robust regression coverage.
No efficiency acceptance. Runtime helper code is unchanged; prior results remain.

Completed 2026-09-14: [three-case retention model comparison](MOTHER-RETENTION-MODEL-01-REVIEW.md),
six fresh serial sessions at `0e80f9b`: **−1.58% total tokens / −52.77% process
time**, 3/3 reviewed targets in both arms, no clean-case false positive. Skill
adopts the new option in every case; its clean-case token cost increases 34.35%.
Unequal extra checks, shared host/cache and three capability-selected authored
tasks at n=1 prevent causal or whole-bundle claims. All six native records retained.

2026-09-14 local capability update: [Mother retention option](MOTHER-RETENTION-01.md)
adds explicit success-path display checkpoints to the disposable component probe.
Native fault/normal controls and CLI checks pass; the targeted model results above
now establish adoption at their measured resource, not general savings.
Standalone project-test delivery still takes precedence. Full local
suite: 419 tests passed in 174.634s after correcting two startup-sensitive test
deadlines; the initial failures and unchanged production deadlines are disclosed
in that report. This is not hosted release verification.

Later [Necromancer entrypoint candidate](NECROMANCER-ENTRY-01.md) consolidates
decision guidance and moves conditional history procedures to its reference.
Collector behavior is unchanged. Its two-cell check at `d5c7150` ended with a
skill timeout (240.025s, no captured work or usage) and completed baseline
(63,924 tokens / 31.418s). No retries, instruction adoption or efficiency claim;
cause unknown. This does not relabel gate 05 history overhead as corrected.

The [all-eight checkpoint 05](BUNDLE-CONTRACT-05-REVIEW.md) completed all 18 cells
on resource `d4a52ef`: **−3.12% tokens / −8.53% process time** in aggregate.
It clarifies one QA display contract and preserves previous experiments unchanged.
Ten post-timing author replays confirm unchanged QA tests reject stale overwrite
and accept guarded Search, and final Form suites pass. One original skill QA
execution still lacks native output; replay is not replacement model evidence.

These are different tasks and frozen resources, not one pooled benchmark. Percent
changes compare skill with each report's own baseline. Favorable pairs do not
supersede adverse results or prove the performance of later resource edits.

| Evidence | Measured resource | Recorded tokens / time | Interpretation |
| --- | --- | --- | --- |
| [All-eight gate 05](BUNDLE-CONTRACT-05-REVIEW.md) | `d4a52ef` | −3.12% / −8.53% | Latest combined gate; nine exposed tasks, 18 cells. Unequal work and one missing native QA output; overall target unmet. |
| [All-eight gate 04](BUNDLE-CONTRACT-04-REVIEW.md) | `9081dfa` | +4.89% / −13.17% | Earlier combined gate preserved. Extra work, scope/capture issues and overspecified QA assertions remain. |
| [Receipt source-layout transfer](results/receipt-src-model-01/README.md) | `53b2765` | −12.39% / −41.67% | New import-root option adopted; required before/after tests captured. One exposed authored task; unequal extra work and baseline's missing leading output prevent a general efficiency claim. |
| [HTTPX duplicate-header audit 02](results/httpx-header-equality-02/README.md) | `89e4d61` | −5.40% / −32.42% | Native coverage-gap verification and helper integrity output adopted. Baseline scope violation and unequal checks remain; not equal-scope superiority. |
| [HTTPX cookie design transfer](results/httpx-cookie-design-01/README.md) | `e267919` | +12.35% / −16.53% | Both preserve runtime contracts; different extra probes. Later Landlord discovery edit is measured only on gate 05's static formatter review (−14.99% tokens / +28.48% time), not this runtime transfer. |
| [Landlord decision checkpoint](results/landlord-decision-01/README.md) | `fee77ff` | +43.35% / +56.67% | Appropriate static review but increased costs; subsequent instructions do not rewrite this adverse result. |

한국어: 최근 Receipt와 Con Artist의 개별 실험에는 비용 감소가 있었지만,
작업량·범위·출력 기록 차이가 있어 일반적인 성능 향상으로 확정할 수 없다.
최신 팀 전체 실험도 토큰 절감 목표를 충족하지 못했다. 아래의 이전 기록은
당시 버전의 근거이며, 오늘의 파일로 다시 측정한 결과가 아니다.

Recent native improvements are separate from those model percentages.
[Receipt lossless JSON formatting](RECEIPT-OUTPUT-01.md) follows the measured
`53b2765` resource: 8.75% fewer characters on one retained payload, identical
parsed values, optional human indentation. Gate 05 Receipt does not invoke this
helper; the formatting change's model-session impact remains unmeasured.
Other recent checks:
[Receipt import-exit correction](RECEIPT-IMPORT-EXIT-01.md),
[source-layout support](RECEIPT-SRC-01.md), and
[installed helper execution](../docs/INSTALLATION-TEST.md#installed-helper-behavior-check--2026-09-13).
The prelaunch full local suite passed **416 tests in 67.828 seconds** after
the prospective fixture preflight. This is not hosted-CI, remote-installation or model quality
evidence. Historical billing/visibility observations below have not been rechecked.

## Earlier evidence — preserved, not the latest resource snapshot

- [Duplicate-header equality audit](results/httpx-header-equality-01/README.md),
  Con Artist `400c7c3`: both arms verify the coverage gap and a real failing
  stronger assertion; **+65.33% tokens / −15.92% time**, n=1. Direct reading
  adopted, collector unused, substantial audit-helper source reads remain.
  The lower-token/all-eight objective remains unmet; earlier results stay intact.
  A [later reference-routing candidate](results/httpx-header-equality-01/README.md#later-reference-routing-candidate)
  moves conditional diagnostics out of the default read (22.18% fewer reference
  bytes, not model tokens); model adoption and savings remain unmeasured.
  The subsequent [automatic import provenance](results/httpx-header-equality-01/README.md#later-automatic-import-provenance)
  emits per-process interpreter/copy and module path/hash evidence without a
  handwritten hashing precheck. Helper regression/replay passes; net model cost
  remains unmeasured, and call/binding verification is still separate.
- [Real HTTPX URL audit](results/httpx-url-repr-01/README.md), Con Artist `1a75a03`:
  **+98.27% tokens / −14.35% time**. Both preserve all 125 originals and run the
  same 91-test correct/mutant selections plus normal controls. Precheck adopted,
  but full test-file reading, repeated excerpts and helper inspection remain.
  Later assertion-slice routing is unmeasured; real code is not an independent
  project holdout. This is an adverse efficiency result, not a broad success.
  A later lossless compact-JSON default reduces this same collector output by
  5.44% in characters; identical parsed values, not measured model-token savings.
- [Account-panel delivery transfer](results/mother-panel-01/README.md), Mother
  entry `eefc721`: **−40.38% tokens / −18.76% time**, five native tests pass per
  arm, direct project-test delivery without helper duplication. Author fault replay
  reveals both arms shadow unittest.fail and lose intended assertion diagnostics;
  not accepted equal-quality superiority. Name-only author repair verifies the
  cause. Later runner-method/failure-path guidance is not model-measured. N=1
  targeted synthetic task, not real-project or all-eight confirmation.
- Earlier [all-eight explicit-contract gate](results/bundle-contract-03/README.md),
  resources `557f012`: all 18 cells reviewed; **+16.17% tokens / −12.43% summed
  process time**. Core outcomes supported, one baseline scope violation and
  differing extra work retained. Exposed n=1 synthetic gate, not independent
  real-development confirmation or overall efficiency acceptance. QA duplication
  and caller-binding support are next concrete engineering targets.
- The earlier [nine-task combined comparison](BUNDLE-CURRENT-02-REVIEW.md)
  belongs to frozen revision `417bdac`, **not today's resources**. It records
  **+10.33% tokens / +23.08% summed process time**, with outcome differences.
  Revised-contract evidence above does not retroactively change it; old numbers
  cannot be relabeled as the newest version's performance.
- The recent [cookie audit pair](results/httpx-cookies-01/README.md), Con Artist
  `36e201c`, records **−13.93% tokens / −36.91% time** with correct core outcomes.
  Baseline repairs, different pytest settings/provenance and n=1 prevent an
  accepted equal-work or broad gain. The short test confirms routing adoption,
  not the large-file route's efficiency.
- [Receipt's current-bug pair](results/receipt-current-bug-01/README.md),
  `7e1e1db`, records **+34.16% tokens / +6.48% time** with more complete before
  evidence than baseline. Later helpers and final-check instructions do not
  retroactively improve this result; their whole-task cost effects are unmeasured.
- [Receipt frame parsing](results/receipt-frame-01/README.md), resources at
  `f13a097`: same supplied before/after coverage, 6 versus 3 shell calls, but
  **+4.01% tokens / +9.81% time**. Final-check batching is adopted without a
  measured saving on this new authored n=1 task. Instruction-loading overhead
  and applicability remain priorities; fewer commands alone are not acceptance.
- [Receipt seeded HTTPX fix](results/receipt-httpx-02/README.md), consolidated
  entry `f32de37`: identical final fix and required three-test before/after
  coverage; 8 versus 4 shell calls, but **+61.61% tokens / +112.05% time**.
  Extra context/inventory work, n=1 and shared conditions prevent causal claims;
  this actual-code seeded task does not support efficiency acceptance.
- [Uncommitted settings comparison](results/receipt-uncommitted-01/README.md),
  `75c8718`: both verify core failures/passes and preserve the initial working
  files; **+9.09% tokens / +3.38% time**. Receipt reads the new procedure but
  writes native comparison code instead of using its helper. Cleanup/extra-work
  differences and a missing output prefix remain explicit; no efficiency win.
- [Hostage atomic-export pair](results/hostage-atomic-export-01/README.md),
  `5867752`: −12.85% tokens / −8.43% time with correct core behavior. Both arms
  use two preparation calls; baseline cleanup work, additional skill exception
  coverage and fixture temporary-root inconsistency prevent a causal efficiency
  or strict-scope claim. Separate author contract replay passes both solutions.
- [Uncommitted graph comparison](results/receipt-graph-01/README.md), Receipt
  reference `077805c`: working-tree helper adopted, same six native tests and
  final cleanup, but **+15.49% tokens / +28.15% time**. Baseline interpreter
  repair and skill launcher-file cleanup remain included; n=1 is not acceptance.
- `benchmarks/featured.json` remains the source of the landing-page comparison.
  No recent reliability check replaces its frozen experiment or changes its
  charts. Historical adverse results remain available.
- [Range verification](results/receipt-ranges-01/README.md), `cf4c2c0`: watch/report
  adopted without a custom wrapper; same core seven-test coverage, **+43.79%
  tokens / −39.99% time**. Targeted synthetic n=1 and baseline's broader integrity
  work limit attribution; this tradeoff is not accepted overall efficiency.

## Earlier resource checkpoint and remaining gaps

Historically checked against Git at `1a7b72a`, with the Hostage candidate linked below. This table is not today's resource inventory. Entry/resource revisions are maintenance
identities, **not** necessarily the versions measured by linked experiments.
The eight characters and automatic selection remain intact; helpers are optional.

| Skill | Entrypoint / latest supporting-resource change | Evidence and unresolved work |
| --- | --- | --- |
| Necromancer | `51ce19e` / [presentation correction](NECROMANCER-PRESENTATION-01.md) after `3157ee2` | [Discovery](NECROMANCER-DISCOVERY-01.md), [packaging](NECROMANCER-PACKAGING-REVIEW-01.md), [decision gate](NECROMANCER-DECISION-GATE-01.md): configured consumer retained; favorable pairs have unequal work/capture limits; broader savings unproven. Git color/prefix regression is author-tested, not model-measured. |
| Receipt | `75c8718` / [reference consolidation](RECEIPT-REFERENCE-COMPACT-01.md) after `cf4c2c0` | [Ranges](results/receipt-ranges-01/README.md): earlier watch/report adopted, faster time but substantially more tokens; unequal extra work, no accepted overall gain. Smaller reference is not yet model-measured. [Graph](results/receipt-graph-01/README.md), [settings](results/receipt-uncommitted-01/README.md), [seeded HTTPX](results/receipt-httpx-02/README.md) and [frame](results/receipt-frame-01/README.md) remain adverse. |
| Landlord | `26a310d` / no separate resources | [Application-first discovery](LANDLORD-SOURCE-SCOPE-01.md), [compact regression](LANDLORD-COMPACT-01.md), [auth design](HTTPX-AUTH-DESIGN-01.md): useful consumer inspection but adverse comparisons/nonpaired costs; resource-path discovery remains. |
| Mother-in-law | [mode-specific routing](results/mother-repeat-01/README.md#later-mode-specific-reference-routing), [standalone native support](MOTHER-NATIVE-SUPPORT-01.md) `c6589ee` / helper `b7058c6` | [Repeated-query transfer](results/mother-repeat-01/README.md): asset adopted, native bug regression valid, +50.40% tokens / +14.09% time; later reference routing unmeasured. [Panel transfer](results/mother-panel-01/README.md), [whole gate](BUNDLE-CONTRACT-03-REVIEW.md), [native integration](results/mother-native-project-01/README.md) and [false-pass correction](MOTHER-SUCCESS-STATE-03.md) retain their historical limits. |
| Exorcist | `ca2e179` / `cb10067` | [Signal transfer](EXORCIST-SIGNAL-01.md), [provenance](EXORCIST-PROVENANCE-01.md): small favorable signal result has baseline repair/unequal work; normal path remains costlier in tokens. |
| Hostage Negotiator | `5867752` / no separate resources | [Atomic export](results/hostage-atomic-export-01/README.md): direct-read adoption, same preparation call count as baseline, qualified lower raw cost. [Packaging repair](PACKAGING-REPAIR-01.md) also has unequal coverage; [compact regression](HOSTAGE-COMPACT-01.md) and other tasks do not establish broad gains. |
| Con Artist | [collector applicability](results/httpx-url-repr-01/README.md#later-collector-applicability-correction) `400c7c3` / compact context `063db29`, [precheck](CON-ARTIST-PRECHECK-01.md) | [Equality audit](results/httpx-header-equality-01/README.md): direct reads adopted, gap verified, +65.33% tokens / −15.92% time. [URL audit](results/httpx-url-repr-01/README.md), [assertion-path checks](results/mother-panel-01/README.md#follow-up-con-artist-assertion-path-regression), [whole gate](BUNDLE-CONTRACT-03-REVIEW.md), [cookies](results/httpx-cookies-01/README.md) and [headers](results/httpx-headers-01/README.md) retain their qualified evidence. |
| Friday | `9cae27c` / [result-column observations](FRIDAY-RESULT-INTERFACE-01.md#later-result-column-observations), empty-reader correction | Ordered result labels now distinguish renamed view columns despite equal values; empty/comment-only SQL remains failed, real zero-row SELECTs valid. Native consumer witness and CLI parity verified, model efficiency unmeasured. [Input budget](FRIDAY-INPUT-BUDGET-01.md), [changed paths](CHANGED-PATHS-03.md) and [branch transfer](FRIDAY-BRANCH-01.md) retain their qualified results; broader improvement unproven. |

## Verification and release gates

- [Historical assertion-contract scan](TEST-CONTRACT-SCAN-01.md): 533 retained
  Python files, six candidates all belonging to already-qualified native/panel
  experiments. No new undisclosed case established; unresolved inheritance and
  other static limits remain. This is not an all-results correctness certificate
  or a new performance metric.
- [Future fixture scratch policy](HOSTAGE-ATOMIC-TEMP-PREFLIGHT.md) corrects
  project-local temporary-output control without editing the measured export
  task. Actual creation-path preflight preserves two before failures/four after
  passes. No new model run or improvement claim follows from this correction.
- Local checkout at `1a7b72a`: **330 tests pass** (45.072 seconds). Catalog,
  resource links and featured/localization checks pass. Test count is not a
  model-performance metric or proof of target-assertion coverage.
- [Linux source archive](../docs/RELEASE-READINESS.md), `5b78fef`:
  **326 pass / two Git-history skips** (328 discovered), Python 3.12.3,
  network disabled, existing image/read-only PyYAML mount. No Git/local-run
  state or overlays. This predates the unknown-field validation change and is
  not a fresh dependency install or current host registration.
- Hosted run `34743404198` at `5b78fef`: all four jobs have zero steps. The
  archive annotation reports failed payments **or** a spending-limit issue.
  Private visibility was verified then. Owner authorization is required for
  billing/visibility/publication changes; no release has been authorized here.
- [Executable example](../examples/con-artist.md) and historical
  [installation evidence](../docs/INSTALLATION-TEST.md) are usable references,
  not current remote-installation or universal-superiority claims.

## Next acceptance work — full scope retained

1. Reduce demonstrated end-to-end work on real developer tasks across all eight
   hires while preserving required behavior, scope and character identities.
   Prioritize observed unnecessary discovery, repeated setup and missing checks;
   do not substitute more helper tests for this outcome.
2. Freeze fewer than ten development tasks, versions and criteria before running.
   Compare contemporary baselines at equivalent requested outcomes; verify
   interpreter, runner settings and provenance requirements. Retain every cell,
   repair, failure and differing workload. Do not rerun exposed tasks for scores.
3. Use a separate confirmation set and a current combined all-eight gate.
   Inspect actual assertions, artifacts, scope, capture quality and costs. Total
   tokens include cached input once plus output; missing usage is not zero.
   Reused observations are not independent executions or causal savings.
4. Finish release/installation gates for the intended revision with owner
   authorization. Local tests cannot substitute for hosted CI or publication.

## Preserved detail

The [September 13 development archive](CANDIDATE-DEVELOPMENT-2026-09-13.md)
preserves the previous 400-line status page byte-for-byte, including all adverse
results and intermediate test counts. Its uses of “current” refer to their
historical entries. The [earlier development log](CANDIDATE-DEVELOPMENT-LOG.md)
and linked raw experiment reports remain intact. No experiment was deleted or
re-scored by this summary update.
