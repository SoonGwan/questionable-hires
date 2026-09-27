# Current candidate: whole-task improvement remains unproven

Decision checkpoint **2026-09-27**, namespaces01 execution `a69b63c1`, skill bundle `0333a084`.
The owner objective is better developer work across **all eight roles**, fewer
**whole-task input+output tokens**, and faster completion. It remains unmet.
No complete update or general efficiency claim is supported.

The [model-choice01 comparison](ALL-EIGHT-MODEL-CHOICE-01-REVIEW.md) measured
matching skills from `6701069f`, one per task: Sol tokens+39.23%, time−0.61%,
zero pairs improving both. The configuration is declined. The original
[integration05 review](ALL-EIGHT-CURRENT-05-REVIEW.md), resource `75183f2f`,
retains all16 attempts, unequal work, scope/criterion and preservation limitations.
Its [follow-up](INTEGRATION05-QUALITY-FOLLOWUP.md) separates original model
outcomes from later author controls. None measures subsequent skill changes.

한국어: 2026-09-27 판단에서 전체8개 역할의 품질·전체 토큰·시간 목표는 미달이다.
model-choice01(`6701069f`)은 토큰39.23% 증가·시간0.61% 감소로 채택하지 않는다.
integration05(`75183f2f`)의 불리한 결과와 범위·평가·보존 한계를 유지하며,
이전 측정이나 작성자 재검사를 현재 스킬의 성능으로 바꾸지 않는다.

[urllib3 transfer01 bootstrap correction](URLLIB3-INLINE-TRANSFER-01-PREPARATION.md#bootstrap-correction--2026-09-27-parent-baa7d088),
2026-09-27, parent `baa7d088`: fresh public and test-module imports fail for
missing generated version metadata although a unittest selector passes. Original
15 assertions remain recorded; no clean-bootstrap/helper-transfer claim and no
new model calls. A corrected future resource needs a supported build/import gate.
한국어: urllib3 전달 실험 준비에서 버전 파일 누락을 확인했다. 테스트 선택 실행
통과는 정상 import 증거가 아니며 기존 결과를 보존한다. 새 모델 호출은0회다.

[urllib3 transfer02 native build gate](URLLIB3-INLINE-TRANSFER-02-NATIVE.md),
2026-09-27,parent `ae2b681b`,candidate `80c06e2e`: separate supported backend
build yields genuine version metadata; fresh public import and15 observer calls
pass with preservation. Zero models; no cost/adoption claim. Missing metadata
was already qualified in the original September21 report, not a new discovery.
한국어: 별도 공식 빌드 자원에서 정상 import·15개 호출을 확인했다. 모델0회로
비용 절감이나 채택 증거는 아니며 과거에 확인된 결함 기록도 유지한다.

## Model evidence and decisions

| Checkpoint / date / resource | Observed result | Decision |
| --- | --- | --- |
| [Necromancer file regions01](NECROMANCER-FILE-REGIONS-01-REVIEW.md),2026-09-27,execution`b7f6a761`,candidate`97c15593` | Tokens−7.76%,time−0.096%(0.105s),one numerical joint pair;both complete15 values/caller/contracts/history/preservation and response sums. | No adoption;neither invokes parser despite recorded exact initial skill exposure. Speed delta lacks variance evidence;exposed n=1/fixed order/shared host/unequal optional work;no all8 gain. |
| [Necromancer retained matrix01](NECROMANCER-RETAINED-MATRIX-01-REVIEW.md),2026-09-27,execution`c9d618d4`,candidate`837988d5` | Two original cells;tokens+28.33%,time+4.20%;0/1 joint. Both15 values/caller/contracts/ancestor history/preservation and response sums reviewed;original session output recovery retained. | Declined;candidate does not invoke new API. Both direct probes call15 once;exposed n=1/fixed order/shared host/unequal optional reads;no all8 gain. |
| [urllib3 inline transfer02](URLLIB3-INLINE-TRANSFER-02-REVIEW.md),2026-09-27,execution`d8c894d2`,candidate`80c06e2e` | Two original real-source cells;tokens+23.22%,time+12.76%;0/1 joint. Both15 values/caller/contracts/ancestor history/preservation reviewed;partial CLI output recovered from original sessions. | Declined;candidate reads but does not invoke observer. Exposed n=1/fixed order/shared host/unequal optional work;no all8 gain. |
| [Necromancer inline matrix01](NECROMANCER-INLINE-MATRIX-01-REVIEW.md),2026-09-27,execution`bf4d19ca`,candidate`80c06e2e` | Four original cells;tokens−3.82%,time−13.50%;1/2 joint reductions,invoice both worse. Both candidates actually call observer;required behavior/history/tests/preservation and response sums reviewed. | No general adoption;ordinary skills unchanged. Exposed n=1/unequal optional work/error recovery/shared host limits retained;no all8 gain. |
| [Necromancer call matrix01](NECROMANCER-CALL-MATRIX-01-REVIEW.md),2026-09-27,execution`71798c5f`,candidate`c889175e` | Four original cells;tokens+2.24%,time−14.65%;0/2 joint reductions. Required caller/history/tests and source preservation reviewed;both render authoring errors/recovery charged. | Declined;neither candidate invokes helper,so no tool efficacy/all8 adoption. Per-response sums reconcile;ordinary skills unchanged. |
| [Necromancer decision checks01](NECROMANCER-DECISION-CHECKS-01-REVIEW.md),2026-09-27,execution`1178cd88`,candidate`e5061da5` | Four original matching-skill cells; tokens+18.42%,time+3.04%;0/2 joint reductions. Required native behavior/history/source preservation reviewed; candidate probe error/recovery retained. Original per-response sums reconcile:invoice5/5 responses,render5/6; count alone is not savings. | Declined; ordinary skills unchanged. Exposed n=1/unequal optional work/shared host; no all8 saving. |
| [Namespaces01](ALL-EIGHT-NAMESPACES-01-REVIEW.md),2026-09-27,`0333a084`,execution `a69b63c1` |16 matching-skill apps-only/namespace-excluded cells; tokens−12.73%,time−2.73%;5/8 joint reductions. | No general adoption/all8 gain: Necromancer both worse,Receipt/Exorcist slower; repeated exposed n=1 tasks,shared host/cache,unequal tracing/coverage. Original native capture gap retained; author replay separate. |
| [Apps01](ALL-EIGHT-APPS-01-REVIEW.md),2026-09-27,`6701069f`,execution `5cf3504b` |16 matching-skill default/apps-off cells; tokens−9.49%,time+0.52%;4/8 joint reductions. | No adoption; exposed n=1 tasks,shared host/cache and unequal optional work. Scoped native outcomes and original preservation reviewed; no general quality or skill-version gain. |
| [Model-choice01](ALL-EIGHT-MODEL-CHOICE-01-REVIEW.md),2026-09-27,`6701069f` |16 same matching-skill Astra/Sol cells; Sol tokens+39.23%,time−0.61%; all8 higher tokens,0 joint gains. | Configuration declined; Sol scope violations, unequal host catalogs, matching-skill-only protocol correction and exposed n=1 development tasks retained. |
| [Path-selection transfer01](PATH-SELECTION-01-REVIEW.md),2026-09-27,unchanged resource`9fdee801`,inputs`3ff3fa85` |4 scoped diagnostic outcomes supported; tokens+5.40%,time−18.75%; no pair improves both. Direct initial/final supplied-file modes match. | No optimization adopted or quality advantage; related authored fixtures,n=1,grouped order/shared cache and unequal optional work. |
| [Interpreter route01 review](INTERPRETER-ROUTE-01-REVIEW.md),2026-09-27,`e918d02d` |6 scoped tasks supported; versus no skill tokens+0.67%,time−8.39%; versus predecessor tokens−4.75%,time+1.73%. Unequal extra work and coordinator exit-vector limits retained. | Neither aggregate improves both; correlated exposed development/control pair. |
| [Integration05 review](ALL-EIGHT-CURRENT-05-REVIEW.md),2026-09-27,`75183f2f` |16 scoped outcomes reviewed; tokens+18.54%,time+9.06%; no pair improves both. Baseline SQLite outside scope, criterion mismatch and initial untracked-mode gaps retained. | Adverse cost result; exposed integration controls, not independent validation or unqualified quality score. |
| [Native-split02 costs](NATIVE-SPLIT-02-COSTS.json),2026-09-27,`6c099d68` |6 cells; summed tokens+43.05% versus no skill,−9.35% versus predecessor. [Original output follow-up](NATIVE-SPLIT-02-OUTPUT-REVIEW.md) retains391-token predecessor truncation. | [Scoped original review](NATIVE-SPLIT-02-REVIEW.md) retains binding-capture, criterion and index limitations; no whole-team efficiency promotion. |
| [Assertion-contract01](ASSERTION-CONTRACT-01-REVIEW.md),2026-09-27,`33530f98` |6 reviewed cells meet scoped contracts; tokens+36.43%,time−12.01% versus no skill. | No joint saving; retain correctness boundary. |
| [Receipt versions01](RECEIPT-VERSIONS-01-REVIEW.md),2026-09-22,`e075bdb` |6 cells; tokens+0.31%,time−13.77%; multi-version helper adopted. | Adoption without broad cost gain; [original response-cost review](RECEIPT-VERSIONS-01-INPUT-COSTS.md). |
| [External SWE-Lite pilot01](SWE-LITE-PILOT-01-REVIEW.md),2026-09-22,`8ee6c56` |4 cells; required Requests141/141 and pytest78/78 pass; tokens−0.71%,time+2.43%. Broader pytest check has fixture confound. | Public external authorship, not proven uncontaminated holdout; no general saving. |
| [All-eight regression04](ALL-EIGHT-CURRENT-04-REVIEW.md),2026-09-21,`0d12dd9` |16 cells; tokens+20.39%,time−5.17%; scope-inclusive7/8 baseline and8/8 current. | Historical resource; exposed tasks, not general quality advantage. |


All observations are dated, resource-specific development evidence. Reused
fixtures, n=1, shared host/cache, unequal verification and exposure limits prevent
independent generalization. Cached input is included once; reasoning is not added
again. The [featured pointer](featured.json) and frozen charts remain separate.

한국어: namespaces01(2026-09-27,`0333a084`)은 합계 토큰12.73%·시간2.73% 감소지만
동시 절감5/8이며 이력 추적은 두 지표 모두 악화됐다. 전체 목표 미달로 기본 설정을
채택하지 않는다. [이전 판단 기록](CANDIDATE-HISTORY-2026-09-27-BEFORE-NAMESPACE-TRANSFER.md)에
apps01의 시간 증가와 이전 불리한 결과를 보존한다.

[Effort01 original review](ALL-EIGHT-EFFORT-01-REVIEW.md),2026-09-27,
protocol`72f67ad6`,same candidate`7172b50c`:all16 original CLI outcomes reviewed
with required native assertions, scope, source/index guards and cleanup. Low
sums tokens−5.91%,time−17.20%;7/8 joint reductions, but Necromancer
 tokens+24.30%,time+20.71%. Both conditions support the scoped supplied outcomes;
unequal work, exposed n=1 tasks and shared host/cache preclude generalization.
Two omitted CLI native outputs were recovered from their exact original stored
tool responses; [four separate Editor author replays](ALL-EIGHT-EFFORT-01-EDITOR-REVIEW.md)
remain separate. No general low-effort adoption or all8 completion. Historical
[terminal16 checkpoint](ALL-EIGHT-EFFORT-01-TERMINAL16.md),
[in-flight8 snapshot](ALL-EIGHT-EFFORT-01-INFLIGHT8.md) and
[older adverse effort evidence](ALL-EIGHT-EFFORT-01-HISTORY-NOTE.md) remain.
[Receipt guide-first01 review](RECEIPT-GUIDE-FIRST-01-REVIEW.md),2026-09-27,
previous`e6d5e663`,candidate`f91d8ef0`,execution`96780deb`:four original outcomes
supported; tokens−2.17%,time+9.74%,zero joint reductions. Both candidate tasks
slower despite avoiding helper-source reads. **Declined; previous Receipt entry
and synchronized README guidance restored.** All native before/after failures,
source/context/counter guards and exposure/shared-host/unequal-work limits retained.

한국어: effort01(2026-09-27,후보`7172b50c`) 원본16개 과제의 네이티브 결과·범위·
보존을 검토했다. low 합계 토큰5.91%·시간17.20% 감소지만 이력 추적은 모두
증가하고 실제 작업량도 달랐다. 원본 세션 출력 복구와 별도 작성자 재검사를
구분하며 일반 low 기본 설정이나 전체8개 개선으로 승격하지 않는다.

## Functionality and delivery, not model savings

Solver RAM isolation01,2026-09-27,parent`ec04c803`:
[actual no-share Linux guest](SOLVER-RAM-ISOLATION-01.md) verifies/extracts all8
pristine source archives in RAM; no host shares/disks/network, grader path absent,
guest stop/executable0. No Python runtime/tool bridge/native issue tests yet;
zero models, not complete solver readiness or all8 quality/cost improvement.
한국어: 공유 없는 실제 게스트에서 8개 소스와 평가 경로 부재를 확인했다.
Python·모델 도구 연결·전체 비교는 미완료이며 효율 성과로 승격하지 않는다.

External bundle02 solver staging01,2026-09-27,parent`582a37b4`:
[all8 pristine source snapshots](EXTERNAL-BUNDLE-02-SOLVER-STAGING-01.md) preserve
base bytes/modes plus separately hashed genuine metadata; one Git commit/no remote/
no upstream object each, actual fresh public imports8/8. Initial path-alias guard
failure retained. Host-only staging is not OS isolation or native grading readiness;
zero models/issue tests, no all8 efficiency claim.
한국어: 평가 패치 없는 8개 원본 소스의 import·보존을 확인했다. 같은 Mac의
별도 폴더로 격리 완료가 아니며 전체 평가·품질·비용 비교는 아직 미완료다.

Native status config01,2026-09-27,parent`f3abda01`:
[actual compatibility regression](NATIVE-STATUS-CONFIG-01.md) reproduces modern
config-consuming hook failure; corrected call passes actual2.8.7/4.0.2/8-dev runtimes
and Git-free copies. Original failure retained; separate next private driver only.
Cohort unexecuted,zero models; no all8 quality/cost/time claim.
한국어: 현대 훅의 config 누락 실패를 재현하고 세 런타임에서 수정 후 통과를
확인했다. 전체 과제·모델 비교 결과로 승격하지 않는다.

Native completion01,2026-09-27,parent`0024be51`:
[execution gate controls](NATIVE-COMPLETION-01.md) accept actual pytest0/1 completion,
reject collection errors/wrong runtime and synthetic incomplete/timeout/exit
mismatches on two native versions and Git-free copies. Next private driver separates
completed execution from item satisfaction; full cohort unexecuted,zero models.
한국어: 실행 완료와 항목 만족을 분리 검증했다. 테스트 실패 종료1을 통과로
세지 않으며, 전체8개 개선·외부 평가 준비 완료 증거는 아니다.

Native cache inventory01,2026-09-27,parent`68570943`:
[prospective guard controls](NATIVE-CACHE-INVENTORY-01.md) distinguish actual native
cache writes from source changes, retaining both maps/full equality. Byte/mode/
deletion/link faults detected in checkout and Git-free controls; separate next
private driver syntax checked, cohort unexecuted. Zero models; original flags kept.
한국어: 실제 cache 쓰기와 소스 변경 검출을 분리 검증했다. 전체 비교·효율·품질
증거는 아니며 원본 검사 결과를 유지한다.

Native status capture01,2026-09-27,parent`8588e20b`:
[native hook controls](NATIVE-STATUS-CAPTURE-01.md) pass on actual pytest2.8.7/4.0.2
and Git-free copies. XPASS is natively `failed` versus `passed`, category `xpassed`
in both. Separate next private driver updated but not executed; original driver and
grades preserved. Zero models; cache guard/cohort/isolation remain incomplete.
한국어: 실제 두 pytest 버전의 XPASS 판정 수집을 검증했다. 다음 드라이버는
미실행이며 원래 결과를 보존한다. 전체8개 효율·품질 개선 증거는 아니다.

| Checkpoint / date / resource | Evidence and limit |
| --- | --- |
| [Necromancer inline matrix API01](NECROMANCER-INLINE-MATRIX-NATIVE-01.md),2026-09-27,parent`e109ae4a`,candidate identities JSON | Actual inline run_path loader/caller matrices reproduce0/15/0/9;required4tests/9boundaries pass under native parent deadline. | Zero models; unmeasured candidate only. Prior unused helper adverse results retained;ordinary skills and all8 efficiency claim unchanged. |
| [Call matrix prototype02](CALL-MATRIX-PROTOTYPE-02.md),2026-09-27,parent`a4ce4ee0`,source hashes in identities | Version2 retains prior observations on unsupported returns; attempted/evaluated/unrun/ungraded counts and9 native boundary controls pass in checkout/Git-free copy;required4tests pass. | Zero models;standalone only. Interruption/process-loss/primitive limits remain,no installed skill or all8 efficiency claim. |
| [Call matrix prototype01](CALL-MATRIX-PROTOTYPE-01.md),2026-09-27,parent`02fa0904`,source/control hashes in Git | Actual27-case independent native callback matrices reproduce0/15/0/9 deviations;required4tests and6 boundary controls pass in checkout/Git-free copy. | Zero models; primitive/exception/partial-output/timeout limits explicit. Standalone only,no installed skill or all8 efficiency adoption. |
| [Owned official grade01](OWNED-OFFICIAL-GRADE-01.md),2026-09-27,protocol`75e46735`,image/script/patch/parser hashes in outcomes | Actual official-script base/gold both pytest1,154PASS/8FAIL; required F2P11PASS+1FAIL,P2P137PASS+5FAIL both. Script0 masks pytest failure; Original-log audit:153 PASSED+1 nonrequired XPASS+8 FAILED; parser omits XPASS, no canonical collisions. Required grades unchanged. | Declined,zero models. Original pair/author parser errors/service and trust limits retained; no same-resource grading retry or all8 efficiency adoption. |
| [Owned Linux TLS01](OWNED-LINUX-TLS-01.md),2026-09-27,protocol`f5c9886a`,scheme fix`89b2e640`,cert/wheel/source hashes in outcomes | Same-port HTTP/trusted HTTPS200 and untrusted-CA/hostname SSLError controls pass; per-request WSGI fix corrects echoed scheme; cleanup0. | Zero models/selected tests; first wrong-scheme echo retained. Short-lived cert validity/default-trust/official grading/all8 efficiency remain separate. |
| [Owned Linux service01](OWNED-LINUX-SERVICE-01.md),2026-09-27,protocol`0b2e8aaf`,wheel/module/probe hashes in outcomes | Offline separate-prefix native HTTPbin/MarkupSafe load and real /get200/args/echoed URL succeed; client package absence/source preserved, service cleanup0. | Zero models/selected tests; no TLS/official grading/all8 efficiency readiness claim or older grade rescore. |
| [Owned Linux service wheels01](OWNED-LINUX-SERVICE-WHEELS-01.md),2026-09-27,protocol`76bb73a4`,PyPI/wheel/native-header hashes in outcomes | Exact11 separate-service wheels acquired/verified; MarkupSafe cp39 Linux x86_64 header confirmed. Client packages unchanged. | Zero models/tests/install/import/service execution; target tags/metadata are not runtime/TLS/grading/all8 efficiency readiness. |
| [Owned official HTTP01](OWNED-OFFICIAL-HTTP-01.md),2026-09-27,protocol`b643b7d2`,native/source hashes in outcomes | Actual project Requests loopback HTTP200/exact health body and thread/socket cleanup pass; five service-related package imports absent. | Zero models/selected tests. Narrow transport calibration only; separate verified Linux HTTPbin/TLS environment still needed, no official grading/all8 efficiency gain. |
| [Owned official collection01](OWNED-OFFICIAL-COLLECTION-01.md),2026-09-27,protocol`26e8b1a6`,native/plugin/script hashes in outcomes | Actual unchanged-source pytest collects161,exit0,no collection errors/skips/test calls. Official embedded patch content matches private grading patch apart from one terminal newline; distinct hashes retained. | Zero models/test calls/patch application; no script/services/official grading/all8 efficiency readiness claim. |
| [Owned official source01](OWNED-OFFICIAL-SOURCE-01.md),2026-09-27,protocol`065760ad`,direct comparison`fcadd5a8`,archive/map/source hashes in outcomes | All132 selected-base contents match;129 executable-mode differences and different image HEAD. Internal tracked Git consistency passes. | Zero models/case tests; strict HEAD/mode gates remain failed. Original collector-prefix error recovered from exact original log without replay; no full source/runtime/grading/all8 efficiency parity. |
| [Owned native pytest01](OWNED-NATIVE-PYTEST-01.md),2026-09-27,protocol`7eeed75a`,device intervention`7e7a117c`,source hashes in outcomes | Actual native pytest exit1/one failed+one passed vs exit0/two passed; identical tests, assertion41/42, nested native children pass. Guest devtmpfs restores capture. | Zero models/selected-case tests; first capture gap and startup failures retained. Authored runtime calibration only, no official grading/all8 efficiency claim. |
| [Owned guest binfmt01](OWNED-GUEST-BINFMT-01.md),2026-09-27,protocol`ad2432df`,frozen modloop/probe hashes in outcomes | Same actual x86 Python child changes errno8 to exit0/stdout42 after guest-only module/handler setup; project source identity unchanged. | Zero models/case tests; three setup failures retained. No full OCI/native pytest/official grading/all8 efficiency claim. |
| [Owned official project01](OWNED-OFFICIAL-PROJECT-01.md),2026-09-27,protocol`b2e6f8b1`,source/probe hashes in outcomes | Actual testbed Requests source imports in readonly reconstructed root; automatic native Python child fails OSError errno8. | Zero models/case tests; observation exit0 is not child success. Guest x86 routing remains prerequisite; no source-tree/OCI/native grading/all8 efficiency parity. |
| [Owned official root01](OWNED-OFFICIAL-ROOT-01.md),2026-09-27,protocol`33d6616f`,pinned blob/source hashes in outcomes | All10 layers apply exit0 in owned Linux chroot; exact-path Python/core/installed Requests imports and guest stop pass,57.44s. | Zero models/cases; Requests came from site-packages, not testbed source. UID/GID/capability/amd64-kernel/binfmt/native grading/all8 efficiency parity remains unverified. |
| [Owned official layers01](OWNED-OFFICIAL-LAYERS-01.md),2026-09-27,protocol`cb39b28f`,pinned manifest/blob hashes in outcomes | All10 exact blobs acquired/verified,68,884 headers inventoried; missing3 download635,410,855bytes,17.651s total. | Zero models/cases/extraction; symlink/hardlink and independent-parent-watchdog gap retained. No OCI filesystem/native grading/all8 efficiency proof. |
| [Owned official Python01](OWNED-OFFICIAL-PYTHON-01.md),2026-09-27,protocol`905eb299`,pinned layer/source hashes in outcomes | Official-image Python3.9.20 runs via Rosetta in owned ARM Linux; ssl/OpenSSL3.0.15,pytest7.4.4,pluggy1.0.0 actual imports and paths pass. Initial case-insensitive extraction failure retained; unchanged extraction succeeds on temporary case-sensitive volume. | Zero models/external cases. Selected relocated runtime only; no full OCI parity, project/native grading, all8 quality or token savings. |
| [Owned Linux x86 control01](OWNED-LINUX-X86-01.md),2026-09-27,parent`ef69f7c7`,ELF/kernel/source hashes in outcomes | Actual Rosetta static x86 ELF uname/workload exit0 in owned ARM guest; matched-owner/mode readonly write rejection and writable positive control, fixture preservation and guest poweroff pass. | Zero models/external cases; author collector/errno errors and earlier unequal modes preserved. No dynamic libraries/binfmt/official OCI/native grading/all8 efficiency proof. |
| [Owned Linux VM01](OWNED-LINUX-VM-01.md),2026-09-27,parent`55c97a7d`,kernel/source hashes in outcomes | Actual owned ARM Linux boot/uname/proof/poweroff with Apple VZ; initial EFI ZBOOT input fails, same decoded raw kernel succeeds. Scoped process deadlines/exit verified; existing Rosetta availability queries installed. | Zero models/external case reruns; ARM RAM-disk only. Guest x86 execution/official images/native grading/all8 improvement unverified. No bundled dependency, host Rosetta install or persistent VM. |
| [Receipt supplied-tool routing01 review](RECEIPT-TOOL-ROUTING-01-REVIEW.md),2026-09-27,previous`08a18aed`/candidate`44c4ff5e`,execution`02313209` | Four original cells/ten native six-test processes/70 arguments support scoped verification; tokens+96.49%, CLI+93.57%, CLI plus lifecycle+92.14%. | Declined; candidate attempts blocked by host never-approval policy, CLI recovery charged. Extra reference reads and failed discovery retained; entry restored. No all8/update gain. |
| [Receipt local tool routing01](RECEIPT-LOCAL-TOOL-ROUTING-01.md),2026-09-27,parent`08a18aed`,entry SHA in report | Historical conditional routing candidate; unchanged native helpers/other seven skills and local validators pass. | Subsequent review above declines it and restores the entry; no efficiency adoption/adapter installation/all8 gain. |
| [Receipt tool availability01 review](RECEIPT-TOOL-BRIDGE-01-REVIEW.md),2026-09-27,same resource`b081240e`,execution`38ca7353` | Four original cells/ten native six-test processes support scoped verification with70 actual argument records and preservation; tokens+4.61%, CLI+8.51%, CLI plus bridge lifecycle+9.77%. | Declined; both bridge hosts discover the tool but neither model calls it. Zero joint reductions, exposed n=1/shared-host limits; actual model full-schema exposure unverified. No all8 gain or adapter release. |
| [Direct tool host native01](TOOL-BRIDGE-HOST-NATIVE-01.md),2026-09-27,parent`23235ae1`,unchanged HTTP adapter hash in outcomes | Actual Codex0.157.1 host calls in both native invocation modes return before1/after0, six tests each, seven actual argument observations, copied imports and original/config/cleanup evidence. | Zero models; client-directed calls, not model tool selection or token/time/all8 gain. Initial author control field error retained; host cancellation/abrupt-loss limits remain. |
| [Direct tool HTTP cancellation01](TOOL-BRIDGE-HTTP-CANCELLATION-01.md),2026-09-27,parent`14f24558`,unchanged HTTP adapter hash in outcomes | Actual active/queued HTTP cancellation errors then same-session native1/0 recovery pairs, six unchanged tests, argument/import/source/cleanup evidence and settled listener exit pass. | SDK gate only; active work can finish before cleanup. Codex host/cross-instance/abrupt loss/whole-task/all8 benefit unverified; prior HTTP/stdio adverse outcomes retained. |
| [Direct tool HTTP exit01](TOOL-BRIDGE-HTTP-EXIT-01.md),2026-09-27,parent`06945ab9`,server hash in outcomes | Real HTTP normal native1/0 and PID-confirmed SIGTERM: child terminal/no scratch/originals unchanged before author cleanup. Interrupted RPC outcome unavailable with explicit4s client timeout; original10s failure retained. Prior cancellation checkpoints linked in report/history. | Partial SDK transport gate only; native result delivery/host error handling/HTTP cancellation/cross-instance/all8 efficiency unverified. Stdio adverse results remain. |
| [Direct tool forced exit01](TOOL-BRIDGE-FORCED-EXIT-01.md),2026-09-27,parent`b2a593da`,candidate hashes in outcomes | Actual server SIGTERM leaves native child/scratch; signal-to-interruption candidate fails with exit-wait timeout and buffered-stdin shutdown error. Both adverse results retained; exact owned child/project cleaned by author. | Declined; no lifecycle-ready bridge/registration/model trial. Prior normal cancellation results scoped separately; SDK transport/shutdown needs a distinct mechanism. |
| [Local release codec-v2](RELEASE-VALIDATION-CODEC-V2.md),2026-09-27,`5691d3fc`,skill`fab86ec1` | Checkout1,324/17 skipped and Git-free1,324/47 skipped pass; both actual CLI installs8skills/52files,8 verified CLI helps/26 command exits. API value/preservation controls and source parity retained; checker errors/historical count correction explicit. | Local functionality only, no model/remote/hosted or all8 efficiency claim. Prior adverse API01 measurement remains unchanged. |
| [Receipt value codec API02](RECEIPT-VALUE-CODEC-API-02.md),2026-09-27,parent`34fa7ed9`,candidate source hashes in report | Versioned opt-in primitive representation;7 helper tests,22 native boundary controls and both temporary installed modes pass. Default schema/native outcomes preserved; initial missing-version fallback failure retained/corrected. | Zero models; format migration explicit, external consumers/full release/whole-task efficiency unverified. Earlier adverse model result unchanged. |
| [Assertion value codec prototype01](ASSERTION-VALUE-CODEC-PROTOTYPE-01.md),2026-09-27,parent`c2ad2c35`,standalone source hash in report | Final8 local comparisons/20 native six-test processes preserve outcomes/imports/guards;70 argument records restore identically, report bytes−40.88%. Initial control error and separate evidence-retention run preserved; follow-up22 Python3.9/3.11 native budget/error/hook controls pass. | Zero models/installed changes. Bytes are not whole-task tokens/time; API migration and model efficiency remain unverified. |
| [Receipt assertion API01 review](RECEIPT-ASSERTION-API-01-REVIEW.md),2026-09-27,previous`60ced61d`/candidate`4b09097e`,execution`b635b6be` | Four original cells,10 native six-test processes: tokens+25.03%,time−5.05%,zero joint reductions. Custom observer authoring removed in candidates; actual outputs/resources/counters/preservation reviewed. | No efficiency adoption; repeated exposed n=1/shared host/cache and unequal passing-value observation work. Optional capability stays default off; no all8/update completion. |
| [Assertion observation API01](RECEIPT-ASSERTION-API-01.md),2026-09-27,parent `60ced61d`, candidate source hashes in report | Opt-in helper integration: six native observation controls and24 existing invocation/multi-version tests pass. Defaults retain schema; unavailable observations stop with check7 and preserve native outcomes. | Historical local-function checkpoint; subsequent model review above shows no token savings. Full release/hosted delivery unverified; adverse comparisons retained. |
| [Assertion observation native prototype01](ASSERTION-OBSERVER-NATIVE-PROTOTYPE-01.md),2026-09-27,pinned standalone observer/helper hashes | Twelve local comparisons/28 native six-test processes preserve actual outcomes, provenance, originals and hooks; ordinary20 report7 records each, hook8 report unavailable values. | In-memory adapter only; explicit API/result/incomplete handling, installation and model savings unverified. No skill runtime change or all8 completion. |
| [Bounded assertion prototype02](ASSERTION-OBSERVER-PROTOTYPE-02.md),2026-09-27,standalone final-source hashes | Twenty-two native controls across Python3.9/3.11 and four completeness/ownership controls pass; shared report byte budget, unavailable values and hook replacement explicit. | Local prototype only; native runner integration/model savings unverified. No installed skill change or all8 readiness. |
| [Assertion observation prototype01](ASSERTION-OBSERVER-PROTOTYPE-01.md),2026-09-27,standalone local source | Four native three-test pass/fail comparisons, existing-profile and two direct boundary controls retain assertion behavior; no model/skill runtime changes. | Prototype only: shared byte budget/native integration remain; no production readiness or token/time claim. |
| [Receipt optional-detail01 review](RECEIPT-OPTIONAL-DETAIL-01-REVIEW.md),2026-09-27,previous73b83d9d/candidate9b6d3295,execution5f32d1b7 | Four original cells retained; tokens+34.61%,time+84.67%; both pairs worse. Candidate adds assertion observation and three failed observer runs before three corrected native runs. | Declined; both reference files restored. Unequal work/exposed n=1/shared-host limits; document byte reduction is not model saving. |
| [Receipt guide-first candidate](RECEIPT-GUIDE-FIRST-CANDIDATE-2026-09-27.md),2026-09-27,parent`e6d5e663` | Entry guidance routes routine supported CLI use to its existing guide before implementation reads. Native preservation9/native-invocation17 controls pass; no runtime changes. | Measured candidate declined: tokens−2.17%,time+9.74%,both tasks slower; previous guidance restored. Older read-order adverse costs retained. |
| [Official row/runtime metadata01](EXTERNAL-BUNDLE-02-OFFICIAL-ROW-RUNTIME-01.md),2026-09-27,parent`af944167`,skills`7172b50c` | Eight pinned row scripts use Conda/pytest-rA; Requests parser alias matches. One official Linux image environment-layer metadata shows Python3.9.20/pytest7.4.4, differing from native preparation. Digest-verified inspection, no container execution or models; no repair contrast/runtime parity claim. |
| [Requests2674 default trust probe01](EXTERNAL-BUNDLE-02-REQUESTS2674-DEFAULT-TRUST-REVIEW.md),2026-09-27,protocol`2ba701dc`,skills`7172b50c` | Base/gold154PASS each, native0/0, source/runtime guards and service cleanup pass. No repair contrast: all12 designated failures already pass. Pair declined; stop same-runtime retries, retain fixed cohort and other unresolved gates. Zero models. |
| [Default trust controls03](EXTERNAL-BUNDLE-02-TRUST-CONTROLS-03.md),2026-09-27,parent`202ee64a`,skills`7172b50c` | Same native client: environment GET pass/direct send reject; explicit CA and copied extended default CA pass; wrong hostname rejected. No Python/source/global trust changes or models; full corrected Requests pair not yet established. |
| [Requests2674 TLS probe01](EXTERNAL-BUNDLE-02-REQUESTS2674-TLS-REVIEW.md),2026-09-27,protocol`77f669b0`,skills`7172b50c` | Native base/gold each11F2P PASS+1FAIL and142P2P PASS; both exit1, source unchanged, service cleanup0. Port mismatch removed but certificate error remains in direct Session.send; not accepted, zero models. |
| [pytest5103 cache probe01](EXTERNAL-BUNDLE-02-PYTEST5103-CACHE-REVIEW.md),2026-09-27,protocol`0ed7b8b6`,skills`7172b50c` | Original unpatched test fails with Apple default and passes with native empty cache prefix. Fresh base1FAIL/64PASS and gold65PASS, native1/0, inventories unchanged. Author runtime compatibility; zero models, original grade01 retained, other gates unresolved. |
| [Runtime distinctions02](EXTERNAL-BUNDLE-02-RUNTIME-CONTROLS-02.md),2026-09-27,parent`e1a34d5c`,skills`7172b50c` | Native controls distinguish HTTP-only/TLS endpoint mismatch and Apple bytecode-cache location. No case rescoring or models; [prospective pytest5103 cache protocol](EXTERNAL-BUNDLE-02-PYTEST5103-CACHE-PROTOCOL.md) freezes original-test control and fresh required pair. |
| [Requests40 verbose/v2 probe01](EXTERNAL-BUNDLE-02-REQUESTS40-V2-REVIEW.md),2026-09-27,protocol`acfc5efe`,skills`7172b50c` | Fresh native base/gold complete: designated1FAIL→PASS,75P2P pass both, source unchanged; native2XPASS per cell retained separately. Scoped author compatibility only: v2 is not official Requests mapped grader, zero models, other case gates unresolved. |
| [Requests40 probe01](EXTERNAL-BUNDLE-02-REQUESTS40-REVIEW.md),2026-09-27,protocol`8da0dd79`,skills`7172b50c` | Two native author cells complete; base1/gold0, source inventories unchanged, but all76 required labels missing to mapped parser. Small pass/fail controls locate report-format mismatch; separate prospective [verbose/v2 protocol](EXTERNAL-BUNDLE-02-REQUESTS40-V2-PROTOCOL.md). Zero models; no acceptance or savings. |
| [Audit import hash01](AUDIT-IMPORT-HASH-01.md),2026-09-27,`ff0fbd2a` | Complete source hashes/output preserved with64KiB reads; authored4MB hash-loop peak−96.57%,time difference<0.04ms. Native regression fails before;130 checkout/Git-free controls and installed8skills/51files/25commands pass. No model/total-RSS or all8 gain. |
| [Same-revision hunks01](SAME-REVISION-HUNKS-01.md),2026-09-27,candidate`c5121130`;original resource`0333a084` | Original namespace-cell4 identical hunks/1,326 repeated bytes; clarify unchanged-revision reuse and missing-context rereads. Metadata/owned all8 install parity pass. Unmeasured routing; no token/time/quality gain or relabeling old evidence. |
| [History body offset01](HISTORY-BODY-OFFSET-01.md),2026-09-27,candidate on `d8e39d5f` | Removes whole patch-body copy; identical excerpts and invalid-tail rejection. Author peak−90.45%,time difference<0.3ms;49 checkout/Git-free checks,8-skill/51-file local install. No model/remote release gain; original archive setup failure retained. |
| [Fast-surface01](FAST-SURFACE-01-REVIEW.md),2026-09-27,execution `150116f1` | Two no-skill native fixes:Fast-requested tokens+0.21%,time−29.50%. No returned-tier evidence or causal claim; higher advertised credit use. No adoption/larger Fast trial/all8 claim. |
| [Namespace-surface01](NAMESPACE-SURFACE-01-REVIEW.md),2026-09-27,execution `14a11f3a` | Two no-skill native fixes preserve real before/after2-test evidence and original files; namespace exclusion whole tokens−19.90%,time+8.80%. No adoption/all8 or skill-version claim; reused fixture,n=1. |
| [Tool-surface01](TOOL-SURFACE-01-REVIEW.md),2026-09-27,execution `e70238f6` | No installed skills. Apps-off first input−8.77%, whole tokens+21.06%, time+1.29%; host-off cannot execute. Neither adopted. Post-timing item-error diagnostics:36 checkout/Git-free controls; no automatic task rescoring. |
| [Receipt completion02](RECEIPT-UNITTEST-COMPLETION-02.md),2026-09-27,`6701069f` | Both unittest modes reject missing/contradictory completion.198 Receipt tests,17 Git-free controls and isolated all8 install resource checks. No model gain or remote/platform release claim. [Module-only predecessor](RECEIPT-NATIVE-COMPLETION-01.md) remains historical. |
| [Receipt guard I/O01](RECEIPT-GUARD-IO-01.md),2026-09-27,parent `d4bacdf6`,skill `6701069f` | Single-pass prototype misses a watched-file mutation; rejected and helper restored.15 native checkout/Git-free controls. Under1ms author savings are not model gains. |
| [Native transcript prototype01](NATIVE-TRANSCRIPT-FORMAT-01.md),2026-09-27,parent `8200cfc0` | Rejected:30 controls pass but retained observations grow265/805 characters. Original skill files restored; no token claim. |
| [Local release validation](RELEASE-VALIDATION-FD8B590D.md),2026-09-27,`fd8b590d`;checker repair`e9ab80e1` | Checkout1,290/17 skipped,Git-free1,290/47 skipped,zero failures. Actual CLI first fails on local cache expectation; checker-only repair passes8skills/51files/25commands and2 targeted tests per source form. Full suites precede repair; no model/remote/hosted gain. [Earlier1,250-suite checkpoint](RELEASE-VALIDATION-BA2713D5.md) remains historical. |
| [Installed behavior](INSTALLED-BEHAVIOR-75183F2F.json),2026-09-27,`75183f2f` | Historical8 skills/51 files,9 entrypoints/25 exits and scoped async/native checks. Not current remote installation. |
| [Landing token breakdown](../docs/LANDING-TOKEN-BREAKDOWN-2026-09-27.md),2026-09-27,deployed `1acaf4a4` | Bilingual whole-task cost display and website evidence. [Browser](../docs/LANDING-BROWSER-2026-09-27.md) and [evidence-delivery](../docs/LANDING-EVIDENCE-DELIVERY-2026-09-27.md) checks have their own older deployed resources; no skill-efficiency implication. |
| [Initial project capture](INITIAL-PROJECT-FILES-CAPTURE-01.md),2026-09-27,parent `ca71b596` |45 local controls; future initial byte/mode inventories. Historical untracked-mode gaps remain unknown. |
| [Remote install01](REMOTE-INSTALL-01.md),2026-09-22,`5e6beab` | Existing-authentication/cached CLI evidence, not anonymous or current remote release. [Public-history review](PUBLIC-HISTORY-REVIEW-01.md),`4174c18`,remains incomplete; [reading derivatives](results/public-path-derivatives-01/README.md) preserve originals. |

한국어: 로컬 기능 검사·설치·모델 측정·웹사이트 검증은 별개다. 도구가 막혀
작업하지 못한 실행은 절감이 아니다. 건너뛴 검사를 통과로 세지 않으며 과거
커밋의 검증을 현재 파일에 소급하지 않는다. 공개 이력·최종 출시 검증은 미완료다.

## Remaining work

Fresh [external-bundle02 author grade01](EXTERNAL-BUNDLE-02-NATIVE-GRADE-01.md),
2026-09-27,skills`7172b50c`,protocol`5623ca1a`,retains all16 base/gold cells.
Only1/8 pairs meets the frozen native contract; others have missing selectors,
preexisting passes or remaining gold failures. Three service teardown errors are
preserved; a separate corrected native cleanup control passes. Zero model calls.
The linked report preserves all bootstrap chronology; these are author checks,
not issue-solving/model savings or all8 role-quality evidence. [Selector diagnosis
and six-cell file probe](EXTERNAL-BUNDLE-02-FILE-PROBE-01.md),protocol`4f3e0c2c`,
resolves literal/native checks for two pytest pairs,including an ambiguous label.
Requests reporting identities remain incompatible; original XPASS/cache-accounting
limits are preserved with separate derivations. This does not replace grade01 or
establish full-cohort readiness. Repair and freeze future grading/runtime/isolation
before comparisons; do not replace selected cases.

Target an evidenced avoidable operation while preserving required native checks,
assertions, scope and artifact integrity. Search the linked reports and histories
before repeating an approach; compression, forced-helper, generic discovery,
model/effort switches and mutable-file guard merging have already been tested.
Do not repeat exposed tasks until favorable or duplicate the response-cost analyzer.

Freeze a distinct mechanism and representative workflows before measurement.
Inspect original contexts, actual tool outputs, required outcomes and every attempt;
prove lower whole-task tokens **and** faster time without losing developer quality
across all8 before claiming the requested update. Later author replay cannot repair
original evidence. Revalidate affected installation/platform/site behavior when
its inputs change. [Approved CI removal](../docs/PUBLIC-LAUNCH.md) does not imply
current hosted success. Synchronize both README languages for capability/claim
changes and use the existing featured sync script for featured evidence changes.

## Preserved chronology

The [complete pre-consolidation index](CANDIDATE-HISTORY-2026-09-27-BEFORE-INDEX-CONSOLIDATION.md)
preserves every preceding link, mixed/adverse observation and limitation unchanged.
Its same-directory links retain the per-tool chronology and preceding snapshots.
[Integration05 pre-cost index](CANDIDATE-STATUS-2026-09-27-BEFORE-INTEGRATION05-COSTS.md),
[2026-09-21 snapshot B](CANDIDATE-HISTORY-2026-09-21-B.md) and
[earlier chronological history](CANDIDATE-HISTORY-2026-09-21.md) remain historical.

[urllib3 inline transfer02 review](URLLIB3-INLINE-TRANSFER-02-REVIEW.md),2026-09-27,
`d8c894d2`:tokens156,290→192,583,time112.359→126.700s. Candidate does not invoke
observer despite reading its interface/code. Keep ordinary skills unchanged.
한국어: urllib3 실제 비교는 토큰23.22%·시간12.76% 증가로 채택하지 않는다.
필수 작업과 원본 보존을 검토했지만 관찰기 사용은 없으며 전체 목표는 미달이다.

[Retained matrix01 model review](NECROMANCER-RETAINED-MATRIX-01-REVIEW.md),2026-09-27,
execution `c9d618d4`,candidate `837988d5`:tokens188,127→241,430,time122.354→127.493s.
Candidate does not invoke new API;both direct probes observe15 calls once. Decline
adoption;[prototype](CALL-MATRIX-RETAINED-01.md) and
[candidate native gate](NECROMANCER-RETAINED-MATRIX-NATIVE-01.md) remain author-only
capability controls, not measured model savings. Original adverse evidence retained.
한국어: 실제 모델 비교는 토큰28.33%·시간4.20% 증가로 채택하지 않는다.
후보 API는 사용되지 않았고 양쪽15개 직접 호출에 중복은 없었다. 작성자 기능
검사를 모델 절감으로 바꾸지 않으며 전체 목표는 미달이다.

[Python regions file01](PYTHON-REGIONS-FILE-01.md),2026-09-27,parent `cb896543`:
ordinary static excerpt helper gains bounded `--path` input with unchanged stdin
schema. Actual upstream5-definition file/stdin parity and23 affected tests pass
in checkout/Git-free archive;source preserved. Zero models, not whole-task savings
or a complete caller/contract review. English/Korean capabilities synchronized.
한국어: 로컬 파일 직접 발췌 기능을 추가하고 실제 소스 일치·관련23개 검사를
확인했다. 모델 비용·전체8개 성과는 미입증이며 기존 불리한 결과를 유지한다.

[Python regions file01 installed check](PYTHON-REGIONS-FILE-01-INSTALL.md),2026-09-27,
parent `8b1d8163`: actual checkout and Git-free standalone installs each8 skills/
52 resources;installed isolated CLI normal0/missing1,source/resource preservation
and installer check pass. Zero models, no personal installation or hosted release.
Archive SHA/member identities retained; no efficiency or all8-quality claim.
한국어: 실제 설치본 두 경로에서 8개 스킬·52개 파일과 새 CLI의 동작·원본 보존을
확인했다. 모델 절감·전체 품질·공개 배포 성과로 승격하지 않는다.

[Necromancer file regions01 native gate](NECROMANCER-FILE-REGIONS-NATIVE-01.md),
2026-09-27,parent `f5a8b0e6`: separate unadopted inline `--path` CLI routing;
ordinary parser bytes unchanged. Candidate2-definition actual source selection/
preservation passes checkout and Git-free archive;previous23 tests/installed
checks reused explicitly. Zero models;not all8 quality/cost or adoption evidence.
한국어: 별도 발췌 CLI 안내 후보의 실제 두 함수 선택·원본 보존을 확인했다.
모델 비용·전체8개 성과·기본 채택 증거는 아직 없고 기존 결과를 보존한다.

[File regions01 model review](NECROMANCER-FILE-REGIONS-01-REVIEW.md),2026-09-27,
`b7f6a761`:tokens193,225→178,238,time108.875→108.770s. Neither invokes excerpt
parser;0.105s time difference does not prove reliable speed gain. Prepared resources
differ only in entrypoint;initial body exposure confirmed without publishing private
text. Keep ordinary routing unchanged;native file/installation checks remain separate.
한국어: 원본 한 쌍의 토큰7.76% 감소를 관찰했지만 시간 차이0.105초와 도구 미사용으로
신뢰할 속도 개선·전체8개 효능·기본 채택을 주장하지 않는다.
