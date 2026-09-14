# Current candidate: whole-task performance remains unproven

The objective covers all eight hires: materially better real developer outcomes
at similar or lower token/time cost. Reliability fixes, passing tests and helper
microbenchmarks do **not** satisfy that objective. Recent work strengthens tools;
it has not established a broad 20–30% gain.

한국어 요약: 최근 오류 방지·도우미 개선은 검증됐지만, 8개 스킬 전체가 실제
개발에서 더 적은 토큰과 시간으로 좋은 결과를 낸다는 목표는 아직 미달이다.
개별 유리한 수치와 전체 성능을 구분하고, 불리한 결과도 그대로 보존한다.

## Friday cursor lifetime — 2026-09-15, parent `be44fb9`

[Bounded-reader regression](FRIDAY-CURSOR-LIFETIME-01.md): the helper's unfinished
reader could lock the next table replacement, misreporting a tool-induced failure
as a migration error. Six actual assertion failures before the correction become
42 passing helper tests after closing each cursor in `finally`. Boundary cases,
an intervening invalid reader, a genuinely invalid migration and the CLI are
covered. No extra skill-entry text, larger row cap or automatic retries. This is
a correctness fix, not measured whole-task savings; frozen charts stay unchanged.

한국어: 일부만 읽은 조회의 커서가 다음 테이블 교체를 막는 자체 잠금 오류를
재현하고 수정했다. 수정 전 실제 단언 실패 6건을 확인했고 수정 후 관련 검사
42개가 통과했다. 실제 마이그레이션 오류는 숨기지 않는다. 모델 성능 개선율은
이번에 측정하지 않았으며 기존 수치·이미지는 바꾸지 않는다.

## Old/new Exorcist discovery screen — 2026-09-15, launch `6464e84`

Restored source `adec236` passes the full local suite: **598 tests / 91.171s**,
no reported skips. Skill validation, metadata/local links, featured synchronization
and whitespace checks pass. 한국어: 복원된 소스 기준 전체 로컬 검사 598개가 통과했다.
이 검사는 스킬의 일반 성능이나 호스팅 CI 통과를 의미하지 않는다.

[New real-checkout query-construction task](results/httpx-query-build-01/README.md):
candidate `329d06c`, no-skill baseline and original skill `d90c1d4`, one fresh
session each. All reproduce the four required cases and explain repeated-value
and caller-precedence semantics correctly. Candidate versus original records
**+33.29% tokens / +3.14% time**; versus baseline **−10.90% / −6.85%**. Extra
mitigation probes/repeated constructions, outer-call grouping, baseline's missing
test-path error and n=1 limit causality. First-search adoption is not a whole-task
improvement. Reject performance adoption and restore the original Exorcist entry
exactly; no extra stronger discovery rule or favorable rerun. All 125 upstream
files per cell and original stored responses are retained; charts stay unchanged.

한국어: 새 실제 저장소 과제에서 수정 전·후·미적용 조건을 직접 비교했다. 진단은
모두 맞았지만 수정 후는 수정 전보다 토큰 33.29%·시간 3.14%가 많았다. 추가
검증·도구 호출 묶음·미적용 조건의 잘못된 파일 경로 등 작업 차이가 있으므로
문구의 인과 효과로 단정하지 않는다. 첫 검색이 바뀐 것만으로 개선으로 채택하지
않고 Exorcist 진입점을 기존 상태로 복원했다. 모든 결과와 한계는 보존한다.

## Real HTTPX stream diagnosis — 2026-09-15, launch `a2546a2`

Subsequent discovery candidate, parent `9d3ba59`: Exorcist now routes named APIs
or errors to content search instead of treating them as filenames; supplied
failure paths still take precedence and missing locations still allow inventory.
This corrects the observed uninformative first filter without adding a helper or
weakening diagnosis, controls, scope or stopping rules. Unmeasured at this earlier
checkpoint; the later query-construction screen above does not accept it and
restores the prior entry. The comparison below retains its frozen resources.

한국어: 후속 후보는 API·오류 이름이 주어졌을 때 해당 심볼을 내용 검색으로 먼저
찾도록 보정했다. 이미 주어진 경로와 필요한 파일 탐색은 유지하며, 검증이나
진단 범위를 줄이지 않았다. 당시에는 미측정이었으며, 위 후속 직접 비교에서는
개선으로 채택하지 않고 기존 지침으로 복원했다. 아래 결과는 그대로 보존한다.

[Full-checkout stream-preview comparison](results/httpx-stream-preview-01/README.md),
Exorcist resources from `d90c1d4`: both reproduce three real Client/MockTransport
paths and correctly distinguish cached content from stream exhaustion/closure.
Skill records **−15.38% tokens / +7.83% time**, not overall efficiency acceptance.
Its first filename filter finds unrelated documentation images, followed by
another inventory and symbol search. Both preserve all 125 tracked upstream files.
Stored original tool responses retain two decisive outputs partially omitted by
skill's CLI records; no author rerun repairs those logs. Real library, authored
n=1 task and no live connection pool: not production diagnosis or all-eight proof.

한국어: 실제 HTTPX에서 응답 본문 보관 여부와 스트림 소진·종료를 구분하는 진단은
양쪽 모두 맞았다. 스킬은 토큰 15.38% 감소·시간 7.83% 증가로 전체 효율 목표는
미달이다. 첫 파일 검색이 문서 이미지만 찾는 낭비도 확인됐다. 두 원본 도구 응답은
일반 실행 로그에서 일부가 빠졌지만 같은 세션의 저장 기록으로 확인했고, 원본
파일 125개는 보존됐다. 라이브러리 기반 단일 과제로 실제 운영 장애나 일반 성능을
확정하지 않으며 대표 그래프는 유지한다.

## Snapshot QA transfer — 2026-09-15, launch `ff67561`

[New settings-snapshot workload](results/editor-snapshot-01/README.md), candidate
`1cb854d`, tests existing-support and missing-support conditions with one baseline
and skill session each. All four create valid native regressions: original nested
snapshot failure, clean normal save, and all three methods passing on a separate
author-copy deep snapshot. The existing-support branch skips unused transport
resources; missing support still loads its guide and produces valid native gates.
**Present: −18.91% tokens / +4.91% time. Absent: −17.90% / −13.29%.** Filename
inventory returns in both skill cells, so the earlier one-command preparation
does not generalize. Different support implementations/checks, n=1, shared
host/cache and authored scope limit attribution. Keep the functional routing
candidate, not a broad efficiency claim; featured charts stay unchanged.

한국어: 새 설정 저장 과제에서 기존 테스트 지원 유무에 따른 자료 선택이 모두
동작했고 네 세션 모두 실제 중첩 스냅샷 결함을 검출했다. 지원이 있는 조건은
토큰 18.91% 감소·시간 4.91% 증가, 없는 조건은 토큰 17.90%·시간 13.29% 감소였다.
한 조건의 시간 악화를 숨기지 않는다. 앞선 준비 명령 1회는 전이되지 않았으며,
단일 합성 작업과 구현 차이 때문에 일반적인 효율 향상이나 전체 목표 달성으로
판정하지 않는다. 원본 실행·별도 작성자 검증을 보존하고 대표 이미지는 유지한다.

## Native pager interval screen — 2026-09-15, launch `fa3c10d`

Post-diagnostic local regression at source `1cb854d`: **595 tests pass / 90.582s**,
no reported skips; skill/catalog/link, featured synchronization and whitespace
checks pass. 한국어: 전체 로컬 회귀 검사 595개가 통과했다. 호스팅 CI나 스킬 전체
성능을 입증하는 검사는 아니며, 아래 실제 모델 관측과 구분한다.

Subsequent candidate `1cb854d`: move the existing-project-support decision into the
entrypoint, before transport resources are read; batch supplied project inputs
and instructions before missing-path discovery. This follows the observed unused
reads, preserving native assertions, interval contracts, cleanup and QA-only
scope. No executable asset changes. [One exposed-task routing diagnostic](results/pager-routing-02/README.md)
adopts the gate: preparation shell commands fall 3→1, unused transport reads
disappear, and the four required native methods retain real interval failures
and recovery coverage. Versus the earlier skill session: **−28.33% tokens /
−26.16% time**, with different test organization and no final Git command. This
is not a contemporary baseline comparison, independent transfer or a causal
efficiency claim. Unchanged-suite author replay confirms the original failures
and guarded passes. The paired measurements below still describe the old entry.

한국어: 후속 수정은 기존 프로젝트 지원이 충분하면 transport 설명·자산을 읽지
않도록 진입점에서 먼저 결정하게 한다. 이미 주어진 파일과 프로젝트 지침을 함께
읽도록 바꿨고, 중간 상태 검증·정리·QA 범위는 유지했다. 노출 과제 재검사에서
준비 명령 3→1회와 불필요한 자료 읽기 제거가 확인됐으며, 이전 스킬 실행보다
토큰 28.33%·시간 26.16%가 적었다. 테스트 구성·최종 Git 확인 차이가 있고 단일
재검사이므로 일반 성능이나 인과 효과로 확정하지 않는다. 새 과제 전이 검증은
남아 있으며, 아래 비교군 수치는 수정 전 버전의 결과로 그대로 유지한다.

[Pager screen](results/pager-loading-01/README.md), Mother-in-law entrypoint
`c6d8ea0`: both arms deliver four native tests with two real loading-interval
failures and correct error/retry control, preserving production and existing
test support. Skill records **−12.30% tokens / +8.04% time**; baseline's recorded
WebSocket reconnection and different test organization remain included. This
authored n=1 pair is not an overall efficiency win. Persisted shell outputs match
CLI records; separate unchanged-suite author replays fail on original code and
pass on a generation guard. Skill still reads unused transport resources despite
adequate project support, identifying a concrete next routing correction.

한국어: 새 페이지 전환 사례에서 양쪽 모두 로딩 중간 상태 결함을 실제 assertion으로
검출했다. 스킬은 토큰 12.30% 감소·시간 8.04% 증가로 전체 효율 목표는 미달이다.
기존 프로젝트 지원을 재사용하면서도 불필요한 transport 자료까지 읽는 경로가
확인됐다. 연결 재시도·구현 차이·단일 합성 사례라는 한계를 보존하며, 대표 그래프는
바꾸지 않는다. 원본 실행과 별도 작성자 재검증을 구분해 공개 가능한 기록을 남겼다.

## Repository regression checkpoint — 2026-09-15, source `888c362`

Full local `python3 -B -m unittest discover -s tests` passes **592 tests / 90.302s**,
with no reported skips. This covers the repository's existing helper, fixture,
collector, installation and packaging tests, including the recent batching and
rollout-extraction changes. Eight-hire metadata/local-link validation, featured
English/Korean synchronization and `git diff --check` also pass; the test run leaves
the worktree unchanged. This is not hosted CI, a fresh live browser/model benchmark,
or proof of whole-task efficiency. Historical README checkpoint counts stay dated.

한국어: `888c362` 기준 전체 로컬 회귀 검사 592개가 90.302초에 통과했고 생략은
보고되지 않았다. 스킬 메타데이터·문서 링크·대표 결과의 언어 동기화도 확인했다.
설치·패키징을 포함한 기존 테스트 범위의 검증이며, 실제 모델 성능 개선이나
호스팅 CI 통과를 의미하지 않는다. 스킬 전체의 성능 목표는 여전히 미입증이다.

## Necromancer bounded source read — 2026-09-15, parent `7bb94b9`

The history collector previously checked current-file size and then read without
a byte bound. A real-file regression grows the file by 3 MB after the size check;
old code fails to reject it. The collector now requests at most 2,000,001 bytes and
rejects overflow before Git collection. Already-known overflow is rejected without
reading; an exactly 2 MB file preserves selected Unicode/CRLF text. All 28 history
helper tests and the collector benchmark regression pass. Metadata/link validation
and featured synchronization pass too. This bounds one source read, not total
memory, Git output or concurrent snapshot consistency; no model-cost gain claimed.

한국어: 크기 확인 직후 파일이 커지는 경우 기존 이력 도우미가 제한 없이 읽는
문제를 실제 파일로 재현했다. 읽기 자체를 2MB+1바이트로 제한하고 초과 시 Git
실행 전에 중단하도록 수정했다. 경계 크기·한글·CRLF 보존을 포함한 관련 29개
테스트가 통과했다. 전체 메모리 제한이나 모델 토큰·시간 개선을 입증한 것은 아니다.

## Capture localization — 2026-09-15, launches `d21d6f4` through `4a70281`

[Persisted CLI tool-response diagnostic](CLI-ROLLOUT-PROBE-01.md), launch `bcd761d`,
now retains both actual response chunks (92 bytes, witness hash match), tool
arguments and same-session polling. CLI completion still omits BEGIN. Four reviewed
tool records are exported; full private context remains local. Retain CLI transport
and use explicit equivalent persistence across future comparison arms. No skill
gain or historical rescore; 27 runner and four extraction/reconciliation tests pass.

한국어: 세션 저장 기록에서는 실제 도구 응답 두 조각과 호출 인자를 보존했고
92바이트 원본 해시가 일치했다. 앞으로 비교군에 동일한 저장 설정을 적용할
근거가 생겼다. 전체 비공개 문맥은 로컬에만 남기며 스킬 성능 개선 주장은 아니다.

[Native streaming preflight](APP-SERVER-NATIVE-CAPTURE-01.md) now retains the full
delayed payload, genuine assertion diagnostics, cap flags and timeout output.
Four native evidence-reconciliation tests pass. This preflight covered standalone
command execution only; the benchmark transport and featured claims are unchanged.

[Subsequent model-route diagnostic](APP-SERVER-MODEL-CAPTURE-01.md), launch `de00a23`,
does **not** reproduce that success: incremental and completed command output both
lose BEGIN while the final answer retains its nonce. One model turn, one command;
personal hooks and built-in app initialization remain. Reject this transport as a
demonstrated capture fix. Five combined reconciliation tests pass, not performance tests.

한국어: 별도 명령 실행 사전 검사에서 전체 출력·실제 실패·잘림 표시·시간 초과를
보존했다. 증거 대조 4개가 통과했으며 그 범위는 모델 없는 명령 실행에 한정된다.

후속 모델 검사에서는 중간 출력에도 앞부분 누락이 남았다. 개인 훅·내장 앱 연결도
있어 기존 실행기와 동일 조건이 아니다. 이 방식을 검증된 해결책으로 채택하지
않고 실패 결과까지 보존했다. 통합 증거 대조 5개 통과는 성능 개선 주장이 아니다.

[Four baseline-only diagnostic sessions](CLI-OUTPUT-LOCALIZATION-01.md) preserve
six immediate outputs fully, but both delayed 92-byte outputs lose the leading
47 bytes from CLI command events. Final answers correctly report fresh nonces
from those missing prefixes. Thus incomplete retained output is not proof the
model did not observe it. Exact internal cause and actual tool yield/budget
arguments remain unverified. All four runs are retained; no skill-performance
claim, retrospective rescore or featured-chart change follows.

한국어: 출력 수집을 따로 실험한 결과, 시간 간격을 둔 출력의 앞부분은 명령
기록에서 누락됐지만 모델 답변에는 정확히 반영됐다. 기록 누락과 모델 관측
실패를 구분해야 한다. 원인 코드를 특정한 것은 아니며 기존 판정·그래프는
그대로 보존한다. 스킬 성능 개선 수치가 아니라 측정 기록의 한계에 대한 실증이다.

## Exorcist reporter diagnosis — 2026-09-15, launch `3c7721a`

[Reviewable-observation candidate](EXORCIST-OBSERVATION-02.md), parent `e5c9ef2`,
was [rejected after screen 02](results/reporter-observation-02/README.md), launch
`3105de1`, and its paragraph reverted. Source inspection separated, but event
output still lost its prefix; tokens/time increased 42.67%/23.91% against historical
skill. Cancellation ordering and a complete independent native four-test run are
retained, not the full final observation table. No fresh baseline or causal claim.
Investigate capture separately rather than expanding guidance on this exposed task.

한국어: 출력 안내 수정은 앞부분 누락을 해결하지 못하고 이전 스킬보다 비용도
증가해 되돌렸다. 실제 실패·취소 삭제 순서는 일부 확인됐지만 최종 관측표 전체는
검증되지 않았다. 같은 과제에 안내를 더 붙이지 않고 출력 수집 문제를 따로 확인한다.

[Reporter lifecycle screen](results/reporter-diagnosis-01/README.md): unchanged
Exorcist records −41.41% tokens / −44.07% time against one fresh baseline. Baseline
repairs its own probe error; skill's leading diagnostic output is missing, so its
full observation table is unverified. Recovered native failure/counts and original
preservation are retained. Unequal work/incomplete capture: no accepted performance
win. The collector now flags programmatic verbose-count mismatches using this exact
retained case; 26 runner tests pass. Historical metadata and skills remain unchanged.

한국어: 스킬 기록 비용은 낮았지만 기본 모델의 추가 오류 복구와 스킬 출력 누락이
있어 성능 승리로 채택하지 않았다. 실제 실패·원본 보존과 누락 범위를 기록했다.
Python 코드 내부 테스트의 출력 누락 후보를 놓치던 검증기를 수정했고 관련 26개
테스트가 통과했다. 기존 수치·메타데이터와 스킬 지침은 그대로다.

## Con Artist conditional example — 2026-09-15, parent `eca85cd`

Usability follow-up, 2026-09-15, parent `8e94a97`: batch instructions now have a
dedicated [installed reference](../skills/con-artist/references/python-audit-batch.md)
instead of loading unrelated advanced modes; the old anchor still routes correctly.
A [runnable selection example](../examples/con-artist.md#compare-required-test-selections-without-repeating-recipe-setup)
demonstrates four native checks with separate normal baselines, missed versus
detected lost writes, real assertion diagnostics and unchanged originals. Both
example integration tests pass. No new model measurement or runtime algorithm change.

한국어: 일괄 실행 안내를 별도 문서로 분리하고 모델 계정 없이 실행 가능한 테스트
선택 예제를 추가했다. 네 번의 실제 검증에서 정상 통과·결함 누락·결함 탐지와
원본 보존을 확인했으며 두 예제 통합 테스트가 통과했다. 모델 성능 수치는 아니다.

[Test-selection batching candidate](CON-ARTIST-TEST-SELECTION-01.md), parent
`f7d91dc`, allows per-entry native test arguments so required test-specific exits
can share recipe setup without skipping executions. Different selections run new
correct baselines; matching adjacent ones retain explicit reuse. Actual assertion
detection, surviving weak tests, integrity and later-invalid-input behavior are
covered by 78 passing helper tests. Not yet measured in a model task; no new
performance claim or change to the featured benchmark. Subsequent
[ledger selection screen](results/ledger-selection-01/README.md), launch `dde6b61`,
records −17.69% tokens / +9.04% time, with six valid requested checks in each arm.
Both use native orchestration; the new helper API is not exercised. Stored tool
responses retain all six summaries and the real persisted-value failure. No causal
claim or generalized efficiency win follows from this single mixed pair.

한국어: 테스트별 실행이 필요할 때 공통 설정을 한 번에 제출하도록 확장했다.
선택 변경 시 정상 코드 재실행과 실제 결함 탐지를 확인했고 도우미 테스트 78개가
통과했다. 실행 자체를 줄이거나 모델 성능 개선을 입증한 것은 아니다.

후속 원장 감사에서는 양쪽 모두 여섯 검증을 수행했고 스킬 토큰 −17.69%, 시간
+9.04%였다. 새 도우미 API는 사용되지 않아 해당 변경의 효과로 돌릴 수 없다.
실제 도구 응답을 보존했으며 단일 혼합 결과로 전체 성능 개선을 주장하지 않는다.

[Proportional tooling candidate](CON-ARTIST-NATIVE-ROUTING-01.md), parent `03c5963`,
changes only helper routing: small audits use native facilities; choose the helper
when its capabilities remove needed orchestration, not for compatibility alone.
All verification/scope obligations remain. [Native screen 02](results/installer-native-02/README.md),
launch/resources `89a45f5`, observes direct native tooling in both skill cells with
actual detection. Fresh baseline token/time changes: rollback +9.57%/−10.72%,
cancellation −11.59%/−25.73%. Cancellation baseline repairs a diagnostic failure;
n=1, exposed related tasks, mixed costs and unequal work prevent general claims.
Keep provisionally and move beyond the installer cases, including helper-needed work.

한국어: 작은 작업의 도우미 우선 도입을 제거했다. 검증·권한 경계는 유지하며
실제로 필요한 처리를 줄여줄 때만 선택한다. 새 비교에서 두 스킬 실행에 반영됐고
실제 결함 탐지도 유지됐다. 비용은 혼합 결과이며 기본 모델의 오류 복구 비용도
포함돼 일반화하지 않는다. 잠정 유지하고 도우미가 필요한 다른 작업까지 확인한다.

[Installer transfer 01](results/installer-audit-01/README.md), launch `8955cb1`,
resources `07166bf`: four fresh baseline/skill sessions on two related real-code
tasks all establish native defect detection. Skill tokens increase 97.28% / 75.32%;
time changes −3.49% / +6.28%. Work volume differs, n=1, no efficiency win. Repeated
helper recipes and implementation reads remain observed friction. All original
commands/usage reconcile, supplied file bytes and installed resources are preserved.

한국어: 설치 오류·취소 작업에서도 실제 결함은 잡았지만 스킬 토큰이 97.28%·
75.32% 증가했다. 동일 구현의 관련 과제 2개·각 1회이고 실행량도 달라 일반적
성능 개선 근거가 아니다. 원본 증거를 남기고 반복 호출·사용법 확인 비용을 개선한다.

[Evidence-first routing candidate](CON-ARTIST-ROUTER-02.md), parent `1fa11f3`,
reduces the common entry 4,155→3,419 bytes and routes Python details conditionally.
Tracing is bounded by the actual effect and unresolved bindings, not a complete
wrapper itinerary. Native proof, stronger assertions, runtime context and scope
are retained. 121 targeted tests pass; the adverse installer screen above now measures this candidate.
Instruction size is not a performance result; next comparison must change workflow.

한국어: 공통 안내를 줄이고 Python 상세는 필요한 경우에 읽도록 재배치했다.
필수 검증·바인딩 불확실성·권한 경계는 보존했다. 121개 테스트가 통과했고 이후
위 설치 비교에서 불리한 모델 비용을 관측했다. 지침 바이트 감소는 토큰 절감이 아니다.

[Provenance adoption 02](results/httpx-provenance-02/README.md), launch `670e708`,
resources `b044a19`: one fresh skill session has native 24-pass / 4-fail evidence,
without a new pytest plugin or setup retry. Historical skill costs fall 31.38%
tokens / 43.83% time, but tokens remain 93.27% above the historical baseline.
No fresh baseline or causal/general gain. Keep provisionally and transfer to
another workflow; stop tuning this exposed task. All original evidence reconciles.

한국어: 새 실행에서 중복 진단 플러그인·재시도 없이 실제 검증을 유지했다.
이전 스킬 대비 비용은 줄었지만 과거 기본 모델보다 토큰은 93.27% 많아 목표에는
미달이다. 새 기준군 없는 1회이며 이 과제 반복 대신 다른 작업 비교로 이동한다.

[Proportional provenance candidate](CON-ARTIST-PROVENANCE-01.md), parent `ec5d7d4`,
clarifies that the unittest precheck example does not demand a pytest plugin.
Extra binding instrumentation needs an explicit requirement or unresolved dispatch;
established copied-import/behavior evidence is reused. Actual wrong-consumer
controls still fail before tests, while correct binding retains native detection.
Ninety targeted tests pass. Entry +143 bytes, optional guide +259; model uptake
and net cost effects remain unmeasured. No helper logic or frozen result changes.

한국어: 불필요한 진단 플러그인 생성을 줄이는 후보 지침을 반영했다. 잘못된 실제
호출 연결은 계속 검출하며 관련 90개 검사가 통과했다. 지침 길이는 늘었고 모델
비용 절감은 아직 검증하지 않았으므로 과거 성능 수치를 바꾸지 않는다.

[HTTPX execution review](results/httpx-exception-example-01/README.md), launch
`d14e03b`, resources `bec12d6`: both original native audits establish 24-pass
correct / 4-fail mutant behavior. Skill costs increase **181.66% tokens / 67.95%
time**. Both omit stronger probes; skill adds full helper reads and a custom pytest
plugin that first fails during setup, then succeeds after repair. All scheduled
evidence is preserved and reconciled. No efficiency win or conditional-example
causality. Next work is proportional provenance guidance, not another unchanged run.

한국어: HTTPX 실제 실행 증거는 양쪽 모두 유효했지만 스킬 비용은 토큰 181.66%·
시간 67.95% 증가했다. 별도 pytest 진단 플러그인의 설정 실패·수정과 도우미
전체 읽기가 관측됐다. 실패도 공개했고, 다음은 출처 검증의 과도한 확장을 줄이는
수정이며 같은 후보를 다시 추첨하지 않는다.

[Executed documentation recipe](CON-ARTIST-CONDITIONAL-EXAMPLE-01.md) now selects
the existing conditional stronger-probe mode. Real native controls retain four
checks when existing tests miss the fault or unconditional probe validation is
required, and execute two when the existing assertion already detects it. The
prior guide reproduces two unnecessary executions in that case. Helper defaults
and the entrypoint are unchanged; model uptake and token/time savings are unmeasured.

한국어: 첫 예제가 조건부 추가 검증을 사용하도록 수정했다. 기존 테스트가 결함을
잡는 경우만 실행 4회를 2회로 줄이고, 놓치거나 추가 검증 자체가 요구되면 4회를
유지하는 실제 대조를 확인했다. 모델 성능 개선이나 전체 50% 절감 주장은 아니다.

## Con Artist input bounds — 2026-09-15, parent `f19186c`

[Bounded reads](CON-ARTIST-INPUT-BOUND-01.md) fix a reproduced size-check/read
gap in snapshot collection and unbounded final original comparison. Two new
controls fail before the fix; four pass after it, plus 76 helper and 12 build
tests. Actual reads honor remaining/original byte bounds even after file growth.
No model-cost claim, entry growth or new benchmark run; total memory and filesystem
races are not isolated. Existing baseline reuse already exists and is unchanged.

한국어: 파일이 커질 때 20MB 입력 제한을 넘기는 실제 재현을 고쳤고, 종료 시
원본 비교에도 읽기 상한을 적용했다. 관련 92개 검사가 통과했지만 모델 비용
절감은 미측정이며 전체 메모리·파일 경합 격리를 뜻하지 않는다.

## Friday consumer selection — 2026-09-15, parent `761a4b8`

[Configuration transfer 01](FRIDAY-CONFIG-01-REVIEW.md), launch `0723722`,
resources `636935e`: four completed sessions read nested instructions and use
actual Python consumers; both arms correctly classify both plans. Friday reuses
stateless observations, yet sum tokens increase **17.61%**, time falls only
**1.35%**, and B time regresses. No net efficiency win or helper adoption. Stop
adding read rules to these small pairs; target material repeated-work cost or
missing developer value rather than promoting fewer cheap function calls.

한국어: 새 설정 과제에서 지침 탐색과 정확한 판정·근거 재사용은 확인했지만,
합산 토큰 17.61% 증가·시간 1.35% 감소로 목표에는 미달이다. 오류 과제 시간도
증가했다. 같은 작은 과제에 규칙을 더 붙이거나 호출 수 감소를 성과로 포장하지 않는다.

[Discovery screen 02](FRIDAY-ACTIVE-02-REVIEW.md), launch `8e66077`, resources
`636935e`: both skill sessions use three commands with grouped reads and retain
correct active-reader/rollback evidence. Historical skill sums fall 12.15% tokens
and 8.80% time; B tokens increase by 68. Candidate remains 6.37% more tokens and
1.73% more time than the historical baseline. No fresh baseline/held-out tasks;
no causal or broad gain. Initial discovery precedes entry reading. Keep the small
candidate provisionally and move beyond the repeatedly exposed pair.

한국어: 두 새 세션의 명령이 각각 3번으로 줄고 기존 증거도 유지됐다. 이전 스킬
대비 비용 감소는 관측됐지만 오류 과제 토큰은 소폭 증가했고, 과거 기준보다도
여전히 비싸다. 신규 기준군·새 과제가 없어 일반 성능 개선은 미입증이다.

[Discovery candidate 02](FRIDAY-DISCOVERY-02.md), parent `a1700a3`, adds a
focused grouped-read/missing-path instruction after repeated inventory was
observed. The documented command preserves hidden project instructions while
excluding Git internals in an actual local test. Entry cost grows by 363 bytes;
model behavior and net efficiency remain unmeasured. No verification obligations
or helper routing are removed to make traces shorter.

한국어: 반복 탐색을 줄이는 후보 문단과 실제 파일 탐색 검사를 추가했다. 지침은
363바이트 증가했고 모델 행동·전체 비용 효과는 미검증이다. 검증 의무는 유지한다.

[Active-consumer review 01](FRIDAY-ACTIVE-01-REVIEW.md), launch `fc577c9`,
resources `8153fec`: all four original sessions distinguish compatible ordering
from a premature active old reader and preserve rollback values. Skill totals
increase **21.08% tokens / 11.55% time**. Neither skill session uses the optional
matrix; repeated discovery/read splitting is observable, not a proven cause.
Keep all adverse observations; do not promote helper adoption or broad savings.

한국어: 새 4세션은 양쪽 모두 정상/오류와 데이터 복구를 구분했지만 스킬 합산
토큰 21.08%·시간 11.55%가 증가했다. 도우미는 사용되지 않았다. 반복 탐색은
다음 개선 후보일 뿐 원인·절감률은 미입증이며, 불리한 결과도 보존한다.

[Phase-specific checks](FRIDAY-PHASE-SELECTION-01.md) allow the optional SQLite
matrix to execute explicitly named active readers per rollout/rollback phase.
Defaults remain all readers; absent observations are unrun, not passes. Actual
SQL tracing, fresh post-write/rollback values and an incompatible-reader control
pass with the 39-test matrix suite. Model adoption and cost effects are unmeasured;
this does not explain checkpoint 09's native-SQL cost or establish a broad gain.

한국어: Friday의 선택형 도우미에 단계별 활성 조회 선택을 추가했다. 기존 기본값은
유지하며 생략한 검사는 통과로 처리하지 않는다. 실제 SQL·쓰기 후 값·롤백·비호환
대조군을 포함한 39개 검사는 통과했지만 모델 성능 개선은 아직 미측정이다.

## History collector checkpoint — 2026-09-15, parent `dd4982f`

[Hunk lookup](HISTORY-HUNK-LOOKUP-01.md) replaces per-hunk scans with binary
search while retaining identical evidence. Twenty-five tests pass. Function-only
large-input timing improves, but actual Git collector medians are small/mixed
(rewrite 274.44→278.03 ms; scattered 239.46→237.83 ms). No whole-task/model gain
is established; keep all observations and stop treating helper timing as the goal.

한국어: 이력 도우미 내부 탐색을 개선하고 동일 출력·25개 테스트를 확인했다.
실제 Git 전체 실행은 차이가 작고 일부 악화되어 스킬 성능 개선으로 주장하지
않는다. 도우미 미세 측정 대신 개발 작업 전체의 개선으로 돌아간다.

## Refresh-owner checkpoint — 2026-09-15, launch `3c29443`

[Flag handoff 01 review](HOSTAGE-FLAG-01-REVIEW.md), launch `094cc69`, resources
`fe3faa8`: four completed sessions, all final native handoffs supported by actual
retained/read results. Skill uses the conditional evidence recipe without async
assets. Observed sum costs decrease 5.42% tokens / 14.00% time, with unequal
before-fix work and test breadth. Sixteen separate controls match. Useful adoption,
not a broad gain or actual-CLI-loss recovery demonstration. Move to other hires'
costly workflows; keep this result and prior adverse observations accessible.

한국어: 새 동기식 과제에서 증거 보존 기능의 실제 채택과 양쪽 최종 결과 근거를
확인했다. 토큰 5.42%·시간 14.00% 감소는 추가 작업·검사 범위 차이가 있는 관측치다.
대조 16회도 확인했지만 전체 성능 달성은 아니다. 이제 다른 스킬의 비용 개선으로
이동하며 과거 불리한 결과도 유지한다.

[Flag handoff transfer 01](HOSTAGE-FLAG-01-PROTOCOL.md), resources `fe3faa8`:
new synchronous parsing/handoff tasks, same durable-evidence contract for fresh
baseline and skill arms. Native preflight accepts correct behavior and detects
truthiness/invalid-input faults with real assertions; two fixture tests pass.
Four model sessions were preregistered; completed observations are linked above,
with no real-user claim.

한국어: 비동기 예제를 벗어나 문자열 설정 파싱·테스트 기록 전달 과제 2종을
추가했다. 양쪽 조건의 요구가 같고 정상/오류 사전 검증을 통과했다. 새 4세션
계획의 완료 결과는 위 기록을 따른다. 실사용자 성능 증거는 아니다.

[Optional native evidence retention](HOSTAGE-NATIVE-EVIDENCE-01.md), parent
`b9cb260`: a conditional single-run recipe stores native argv/output/exit in a
fresh permitted project directory when terminal capture is unreliable. Five
actual local controls pass, including lost display, real assertion failure,
empty discovery and preserved exit 37; 12 bundle tests pass. No CLI bug fix or
model/token improvement is claimed. Existing report reuse and scope stay first.

한국어: 출력 누락 때 같은 새 실행의 기록을 재실행 없이 읽는 선택적 방법을
추가했다. 로컬 검사 5개·배포 묶음 12개 통과지만 CLI 원인 해결이나 모델 성능
개선은 미검증이다. 기존 보고서 우선·파일 권한·개인정보 범위를 유지한다.

[Adoption screen 03 results](HOSTAGE-REFRESH-03-REVIEW.md), launch `37322ce`,
resources `6b6962c`: both sessions complete; whole-helper reads remain, one repeats
final checks, and one dedicated test command has empty original CLI output despite
a pass claim. Sum cost is 263,857 tokens / 221.094s; no fresh baseline. Eight
separate author controls match, but no complete adoption or performance win.
Investigate durable evidence and read-path uptake before another model run.

한국어: 새 2세션에서 전체 도우미 읽기·반복 점검·원본 출력 없는 통과 보고가
남았다. 합계 263,857토큰·221.094초이며 새 기본 모델 비교는 없다. 대조 8회는
예상대로 동작했지만 검증 완료로 올리지 않고 증거 보존·읽기 경로를 먼저 살핀다.

[Adoption screen 03](HOSTAGE-REFRESH-03-PROTOCOL.md) preregisters two fresh skill
sessions for resources `6b6962c`. No fresh baseline; historical costs cannot prove
superiority. Keep full behavioral/evidence requirements and both outcomes. Once
adoption is supported, move to different workflows rather than tuning this pair.

한국어: 읽기·점검 후보의 새 스킬 2세션 점검을 고정했다. 새 기본 모델이 없으므로
우위를 주장하지 않는다. 지시 채택이 확인되면 다른 작업 비교로 넓힐 계획이다.

[Read/review candidate 03](HOSTAGE-READ-BUDGET-03.md), parent `e659f0e`: concrete
complete-usage excerpt commands, missing-path-only discovery, combined non-test
review checks. Dedicated native evidence is preserved. Entry +16 bytes; usage
excerpts 2,382/5,388 Python and 2,918/7,835 JavaScript bytes. These are not token
savings. Existing 21 helper tests pass; actual model uptake remains unmeasured.

한국어: 반복 읽기·점검 비용 후보를 수정했다. 테스트 근거는 유지하고 사용법
전체만 읽는 명령과 필요한 탐색·점검 묶음을 안내한다. 기존 도우미 테스트 21개
통과지만 바이트 감소는 모델 토큰 절감이 아니며 실제 개선은 아직 미검증이다.

[Follow-up 02 review](HOSTAGE-REFRESH-02-REVIEW.md), launch `b237aae`, resources
`0a94dab`: both skill native transcripts now substantiate final pass claims, but
observed sum tokens **increase 58.57%**, time decreases 6.03%. Four sessions and
all adverse observations retained; 16 separate author controls match. Repeated
reads/review calls are the next cost target, not permission to weaken evidence.
Detailed test-path review remains; no broad gain or featured promotion.

한국어: 후속 4세션에서 스킬의 실제 테스트 근거는 확보됐지만 토큰 58.57% 증가,
시간 6.03% 감소로 성능 목표는 미달이다. 대조 16회와 불리한 원본을 보존했다.
다음은 근거를 유지하면서 반복 읽기·점검 왕복을 줄이는 일이다.

[Prospective follow-up 02](HOSTAGE-REFRESH-02-PROTOCOL.md) freezes candidate
`0a94dab` for four fresh baseline/skill sessions on the same exposed development
tasks. Separate original report evidence from retained-code controls and cost;
no held-out or broad performance claim is planned. This historical plan is now
followed by the completed observations above.

한국어: 명령 분리 후보의 후속 4세션 계획을 고정했다. 기존 개발 과제의 재확인이며
새 과제 일반화 검증이 아니다. 당시 계획의 완료 결과는 위 기록을 따른다.

[Refresh-owner review](HOSTAGE-REFRESH-01-REVIEW.md), measured resources `864005b`:
four completed sessions, observed sum reductions 10.61% tokens / 8.62% time,
but both skill answers claim passing tests without original native results.
Separate author controls confirm retained suites accept valid alternatives and
detect faulty cleanup (16/16); they do not repair original capture gaps.
The next candidate separates native-test commands from final diff/status instead
of prescribing one batch. Structure validation and two fixture tests pass;
model adoption is not yet measured. No featured-chart change or broad win claim.

한국어: 새 4세션에서 토큰 10.61%·시간 8.62% 감소가 관측됐지만 스킬 두 번
모두 원본 테스트 결과 없는 통과 보고가 있어 성공으로 인정하지 않는다.
별도 대조 16회는 정상/오류 구분을 확인했을 뿐 원본 누락을 보완하지 않는다.
다음 후보는 테스트와 최종 점검 명령을 분리한다. 로컬 검사만 통과했고
실제 모델 보고 개선은 미검증이다. 기존 대표 그래프는 유지한다.

## Reviewed checkpoint 09 — 2026-09-14, launch `3a7d972`

[Refresh-owner transfer preflight](HOSTAGE-REFRESH-01-PROTOCOL.md), resources
`864005b`: two new variants explicitly require concurrent callbacks, not duplicate
suppression. Native six-method oracle accepts the correct owner and detects older
success/failure/cancellation clearing pending (three actual assertions). Oracle is
not model-visible; two fixture tests pass. At this historical preflight, four model
sessions were planned; completed observations are linked in the checkpoint above.

한국어: 동시 실행을 유지해야 하는 새 과제 2종의 사전 검증을 끝냈다. 정상
구현 통과와 잘못된 상태 해제 3경로 실패를 확인했다. 정답 테스트는 모델에
주지 않는다. 당시 기본/스킬 4세션 계획이었으며 완료 결과는 위 새 기록에 있다.

[Hostage evidence/entry candidate 02](HOSTAGE-EVIDENCE-COMPACT-02.md), parent
`a43f4bf`: require locating native test evidence before pass claims; combine
runtime-specific asset routing without changing callbacks or task scope. Entry
−351 bytes (−7.62%), 46 related author tests pass. Model adoption, reporting
improvement and token savings are not yet measured; checkpoint 09 stays frozen.

한국어: 폼 스킬의 통과 보고 기준을 실제 테스트 증거 확인으로 바꾸고 중복
자원 안내를 줄였다. 안내 7.62% 감소, 관련 테스트 46개 통과지만 모델의 보고
개선·토큰 절감 실측은 아직 없다. 기존 평가 수치는 유지한다.

[Consolidated review](BUNDLE-CONTRACT-09-REVIEW.md): observed totals −13.65%
tokens / −19.54% time, but four token regressions, two time regressions, unequal
work and two original capture gaps. Final schema controls detect three actual
rollback data faults in both arms (8/8 outcomes). Checkpoint review is complete;
the broad usefulness/performance goal is not. No featured-chart promotion.

한국어: 이번 평가 검토는 끝났지만 전체 성능 목표는 미완료다. 토큰·시간 합계
감소와 함께 비용 증가·작업량 차이·원본 출력 누락 2건을 유지한다. 롤백 데이터
손실 대조 8회도 검증했다. 다음 개선 대상은 폼 비용과 근거 없는 통과 보고다.

The following dated partial notes preserve the order of review; their pending
whole-checkpoint statements are superseded by the consolidated review above.

아래 부분 검토 기록의 당시 미완료 표시는 위 종합 검토로 갱신됐다.

[Export verification](BUNDLE-CONTRACT-09-EXPORT.md): all 18 cells and 58 project
text files are available; raw usage/events/provenance reconcile. Exporter fixes
observed malformed temporary paths without consuming following evidence; 31
related author tests pass. Both original output gaps remain; consolidated review
and remaining controls are pending, with no featured-chart change.

한국어: 18세션·텍스트 파일 58개 공개본을 원본과 대조했다. 잘못된 임시 경로
가림과 증거 보존을 수정했고 관련 테스트 31개가 통과했다. 원본 출력 누락과
불리한 결과를 유지하며 종합 검토·남은 대조는 아직 진행해야 한다.

[Persistence/diagnosis review](BUNDLE-CONTRACT-09-AUDIT-REVIEW.md): four literal
replays finish. Con Artist captures all four missing-write checks without reading
helper source. Baseline persistence lacks its first original phase; replay only
matches the captured suffix and changes its copy's Git index. Both diagnosis
probes exercise actual transport/ordering and reproduce captured JSON, with
different artifact work. Two original gaps now known: form skill and persistence
baseline. Consolidation, publication and remaining independent controls are due.

한국어: 저장 감사·검색 진단의 실제 재실행 4개를 확인했다. 기본 저장 감사의
첫 원본 실행 출력 누락을 추가 발견했고 폼 스킬 누락과 함께 유지한다. 스킬
감사는 도우미 소스를 읽지 않고 네 결과를 확보했다. 전체 공개·추가 대조는 남았다.

[Boundary/formatter review](BUNDLE-CONTRACT-09-BOUNDARY-FORMATTER-REVIEW.md):
boundary original before/after evidence is present and final files match across
arms; 8 native adverse/positive controls match. Formatter recommendations are
supported, but baseline executes seven extra value checks while skill explicitly
uses static review. Preserve unequal-work and cost caveats. A malformed private
link in the formatter answer needs redaction before full-run publication.

한국어: 경계값 원본 증거와 대조 8회를 확인했다. 포매터 결론도 타당하지만
기본 모델만 추가 실행 검증을 해 비용 차이를 동일 작업의 효율로 보지 않는다.
전체 공개 전 로컬 링크 가림과 나머지 과제 검토가 남아 있다.

[History/schema review](BUNDLE-CONTRACT-09-READONLY-REVIEW.md): both arms reach
supported conclusions, four literal Python witness replays reproduce captured
stdout and preserve original files. Both skill pairs still cost more tokens/time.
Neither skill reads its helper; matrix misuse is not the observed cause. This
is not full-shell replay or independent fault validation; remaining review is due.

한국어: 이력·스키마의 실제 Python 검증 4개는 원본 출력과 일치하고 파일을
보존했다. 결론은 타당하지만 두 스킬 모두 토큰·시간이 더 들었다. 도우미를
읽지 않았으므로 도우미 남용을 원인으로 단정하지 않는다. 추가 검토는 남았다.

[Partial search QA review](BUNDLE-CONTRACT-09-SEARCH-REVIEW.md): four original
native captures contain decisive evidence; 12 retained-test controls match.
Both arms detect stale/retention faults and accept contract-valid alternatives.
Both skill pairs cost less, but different witnesses/artifacts and n=1 prevent
general claims. Original production bytes remain unchanged; other reviews remain.

한국어: 검색 QA 4세션의 원본 증거와 대조 12회를 확인했다. 두 모델 모두 실제
결함과 계약상 정상 대안을 구분했고 원본 코드는 유지했다. 스킬 관측 비용은
낮지만 검증 사례·산출물이 달라 일반화하지 않으며 나머지 과제 검토는 남아 있다.

[Partial form review](BUNDLE-CONTRACT-09-FORM-REVIEW.md): ten native retained-test
controls preserve originals. Both suites reject missing guard/cleanup, but baseline
rejects a contract-valid duplicate returning False; skill accepts it. Skill's
original native-test output remains missing despite later replay passes. This
narrow artifact benefit does not establish an equal-work or general efficiency win.

한국어: 폼 테스트 대조 10회를 끝냈다. 두 테스트 모두 결함을 잡았지만 기본
테스트는 유효한 False 반환을 잘못 실패시켰고 스킬은 통과했다. 후속 통과로
스킬 원본 출력 누락을 채우지는 않는다. 전체 과제 검토와 효율 판정은 남아 있다.

[Collection/arithmetic](BUNDLE-CONTRACT-09-INTAKE.md), resources `9071a1c`:
18/18 sessions ended, no timeouts; raw usage and installed resources reconcile.
Baseline 760,865 tokens / 572.922s; skill 657,044 / 460.983s (−13.65% / −19.54%).
Four pairs cost more tokens; history/schema cost more on both axes. Pending-form
skill lacks original native-test output. Full behavioral/scope review and author
controls remain pending; these are not accepted efficacy claims or chart updates.

한국어: 새 18세션의 실행과 사용량 대조는 끝났다. 합계 토큰 13.65%·시간
19.54% 감소지만 4개 과제의 토큰은 증가했고 이력·스키마는 시간도 증가했다.
폼 스킬의 원본 테스트 출력 누락이 있다. 전체 행동·범위·대조군 검토는 아직
진행 전이며 일반적 성능 향상으로 발표하거나 그래프를 바꾸지 않는다.

## Reviewed checkpoint 08 — 2026-09-14, launch `de3cbc0`

Receipt [Git review preservation](RECEIPT-GIT-REVIEW-01.md), parent `65c2340`:
native tests reproduce optional index writes after comparison. Command-local
status/diff controls preserve the tree with identical review output; optional
locks alone failed here. 27 related tests pass. Guide +295 bytes; no model-cost
measurement, universal read-only guarantee or change to frozen results.

한국어: 비교 후 Git 조회의 인덱스 변경을 실제로 재현했다. 두 명령별 갱신
제어를 함께 쓰면 변경 내역을 숨기지 않고 원본 목록을 유지했다. 관련 테스트
27개 통과, 안내 295바이트 증가. 모든 부작용 방지·모델 효율 향상 실측은 아니다.

Receipt [guide compaction 02](RECEIPT-GUIDE-COMPACT-02.md), parent `b55aa6a`:
single guide 7,563 → 6,953 bytes (−8.07%); runtime, examples and evidence
requirements unchanged. Author validation only; no model-token gain measured.
Historical results and featured charts remain unchanged.

한국어: 실행 안내의 중복을 줄여 파일 크기는 8.07% 감소했다. 실행 코드·예제·
검증 의무는 그대로다. 작성자 검증이며 모델 토큰 감소를 입증한 것은 아니다.
기존 측정과 대표 그래프는 유지한다.

Receipt [native adoption 01](RECEIPT-NATIVE-MODEL-01-REVIEW.md), launch `b2c7703`,
resources `bc3b225`: both sessions use the ordinary native-mode CLI, without
internal adapters/custom hashing. Correct complete/partial diagnoses, full native
five-test evidence. Sum 161,267 tokens / 86.526s: −27.34% / −38.67% vs prior
skill, **+14.67% tokens / −34.14% time vs prior baseline**. Replays match native
results/tree identities but retain diagnostic differences and later Git-index
changes. Exposed n=1, no contemporary baseline: no general gain or token parity.

한국어: 두 세션 모두 새 실행 모드를 그대로 썼고 내부 수정·별도 해시 코드는
만들지 않았다. 정상/불완전 수정 판정과 실제 테스트 5개 결과를 확인했다.
합계 161,267토큰·86.526초로 이전 스킬보다 27.34%·38.67% 감소했지만,
이전 기본 모델 대비 토큰은 14.67% 더 쓰고 시간은 34.14% 줄었다.
재실행의 진단 출력 차이와 이후 Git 인덱스 변경도 보존했다. 단일 기존 과제
실행이며 일반적인 향상·기본 모델 수준의 토큰 효율을 입증한 것은 아니다.

Receipt [native invocation candidate](RECEIPT-NATIVE-INVOCATION-01.md), previous
source `587fb84`: optional `invocation: module` executes literal `-B -m unittest`
with same-process copy provenance and existing execution supervision. This targets
the adapters written by both SQLite skill sessions. Thirteen new-mode tests plus
69 related existing tests pass, including real SQLite positive/partial controls,
startup bypass, configured-hook rejection and child cleanup. Guide +881 bytes;
adoption and adapter removal are reviewed above; broad efficiency remains unproven.

한국어: SQLite 평가에서 두 스킬 세션이 직접 바꿨던 실행기를 정식 선택 기능으로
추가했다. `-B -m unittest` 직접 실행과 같은 프로세스의 import 확인을 제공하며,
기존 시간·출력 제한을 유지한다. 실제 DB·시작 검증 누락·기존 설정 보존·프로세스
정리 등을 포함해 관련 테스트 82개가 통과했다. 안내는 881바이트 늘었다.
후속 실행의 실제 채택·추가 코드 제거·비용은 위에 기록했으며 일반적 효율은 미입증이다.

Receipt [SQLite transfer 01 review](RECEIPT-LEDGER-01-REVIEW.md), launch `2d8785d`,
resources `ec0cc28`: all four sessions finish and both arms distinguish complete
from incomplete fixes. Totals baseline 140,630 tokens / 131.371s, skill 221,949 /
141.093s: **+57.82% tokens / +7.40% time**. Both skill sessions adapt internals to
the requested native `-m unittest` command. Original tests are present; baseline a
has a leading prefix gap. Separate replays retain later Git-index changes, skill
a's outer assertion failure and b's diagnostic differences. No efficiency win.

한국어: 새 SQLite 과제 4세션은 모두 끝났고 두 모델 모두 완전·불완전 수정을
구분했다. 합계는 기본 140,630토큰·131.371초, 스킬 221,949토큰·141.093초로
스킬이 **토큰 57.82%·시간 7.40% 더 사용**했다. 지정된 `-m unittest` 실행에
맞추려 두 스킬 세션 모두 도우미 내부를 수정했다. 원본 테스트 결과는 있지만
일부 선행 출력 누락이 있다. 별도 재실행의 Git 인덱스 변경·외부 검사 실패·
진단 출력 차이도 보존했다. 일반적인 성능 향상이나 효율 개선 결과가 아니다.

Receipt [committed SQLite transfer preflight](RECEIPT-LEDGER-01-PROTOCOL.md),
resources `ec0cc28`, collector `4325a05`: two new correlated variants exercise real
committed writes/fresh reads and current tests on historical implementations.
Complete fix passes; acknowledgement-only fix still doubles balances. Native
preflight, same-input/import provenance, full original preservation and cleanup
pass (2 author tests / 0.760s). Four baseline/skill sessions were preregistered;
their adverse results are reviewed above. These are not independent production data.

한국어: 기존 파서와 다른 SQLite 수정 검증 과제 2종을 준비했다. 실제 커밋된
쓰기와 새 연결의 읽기로 완전한 수정과 반환값만 고친 불완전한 수정을 구분한다.
동일 입력·과거 구현·원본 보존·정리까지 직접 검증했고 작성자 테스트 2개가
통과했다. 고정 조건의 기본/스킬 비교 4세션 결과와 비용 증가를 위에 기록했다.
서로 관련된 자체 제작 과제이며 실제 사용자·운영 환경의 독립 증거는 아니다.

Collector [pre-add index retention](PRE-COLLECTION-INDEX-01.md), previous source
`3cbae6d`: future runs retain local index bytes/mode/hash after model timing and
before collector Git mutation. Actual child/Git tests show identical captured
pre-add bytes despite a changed final index; failures retain evidence too. Five
new and 25 existing runner tests pass. Binary stays local, metadata is exportable.
This is not a full snapshot, does not repair old evidence and proves no model gain.

한국어: 앞으로는 모델 실행이 끝난 직후, 수집기가 Git 인덱스를 바꾸기 전에
원본 바이트·권한·해시를 로컬에 보존한다. 실제 하위 프로세스·Git 검증에서
수집 전 상태 보존과 이후 변경을 구분했고 관련 테스트 30개가 통과했다.
바이너리는 공개 결과에서 제외한다. 전체 스냅샷은 아니며 과거 증거의 빈 부분을
복구하거나 스킬 성능 향상을 입증하는 변경은 아니다.

Receipt [tree adoption 01](RECEIPT-TREE-MODEL-01-REVIEW.md), launch `eb16150`,
resources `ec0cc28`: guard adopted without custom hash code/listing. 76,962 tokens /
46.154s: −6.43% / −14.46% versus output-choice 01, but +0.28% / −5.99% versus
guide 01. Original five-test native evidence is present. Separate replay matches
native/selected fields, **not full tree identity**: retained post-collector Git
state differs; original per-file inventory is unavailable. A leading command
prefix is also missing. Exposed n=1/shared cache/unequal work, no general gain.

한국어: 전체 변경 감지 기능을 사용했고 별도 해시 코드·목록은 만들지 않았다.
76,962토큰·46.154초로 직전 대비 6.43%·14.46% 감소했지만 더 이전 안내 실행
대비 토큰은 0.28% 증가했다. 원본 테스트 5개의 전후 증거는 확인됐다.
별도 재실행은 테스트·선택 파일 결과가 일치하지만 전체 파일 지문은 다르다.
수집 후 Git 상태를 재사용했고 원본 전체 파일별 지문이 없어 완전 동일성을
주장할 수 없다. 선행 명령 출력 누락도 남아 있다. 단일 기존 과제로 일반화하지 않는다.

Receipt [optional tree guard candidate](RECEIPT-TREE-GUARD-01.md), previous source
`41b5f28`: requested whole-project preservation can use bounded internal inventories
instead of a custom hash wrapper. Includes Git/ignored files, directories/modes
and link text; no target traversal or restoration, not a sandbox. Nine actual
native mutation subcases reject changes; eight guard tests plus 47 helper and 12
packaging tests pass. Guide +896 bytes and two opt-in inventory reads. Subsequent
adoption is reviewed above; general whole-task efficiency remains unproven.

한국어: 전체 원본 보존이 필요한 경우에만 켜는 변경 감지 기능을 추가했다.
모델이 별도 해시 검사 코드를 만드는 대신 내부에서 제한된 범위로 비교한다.
Git·무시된 파일·디렉터리 권한·링크 자체를 포함하며 링크 대상은 읽지 않는다.
실제 테스트 실행 중 원본을 바꾸는 9종을 탐지했고 관련 테스트 67개가 통과했다.
격리·복구 기능은 아니다. 안내는 896바이트 늘고 선택 시 전체 읽기가 추가된다.
후속 실행의 실제 채택·중복 코드 제거는 위에 기록했으며 일반적인 효율 개선은 미입증이다.

Receipt [output-choice screen 01](RECEIPT-OUTPUT-CHOICE-01-REVIEW.md), launch
`15a2e38`, resources `72e1ff2`: compact output adopted, but 82,253 tokens / 53.954s,
**+7.18% / +9.90%** versus prior skill execution. Six shell calls versus four,
including a separate full hash listing and another snapshot. Native five-test
before/after evidence and literal-recipe replay match; original files remain
unchanged. Original SPEC/PYTHON prefixes are missing, so exact version evidence
is not established there. Exposed n=1, unequal work: no efficiency claim.

한국어: 압축 출력 안내는 실제 채택됐지만 82,253토큰·53.954초로 이전보다
7.18%·9.90% 증가했다. 호출은 4회에서 6회로 늘었고 별도 전체 해시 출력과
추가 스냅샷이 있었다. 실제 기존 테스트 5개의 수정 전후 결과·별도 재실행·원본
보존은 확인됐다. 원본 로그의 설정·Python 버전 선행 출력 두 줄은 빠져 있어
정확한 버전 관찰을 입증할 수 없다. 기존 과제 1회이며 성능 개선 결과가 아니다.

Receipt [output-choice follow-up](RECEIPT-GUIDE-COMPACT-01.md#output-choice-follow-up--2026-09-14-previous-source-da5b10e),
previous source `da5b10e`: explicitly prefer existing compact JSON for agent use.
The retained measured helper object is 6,036 bytes indented / 5,516 compact
(−8.61%), with complete parsed equality. No runtime or integrity change; 47
helper and 12 packaging tests pass. This is output arithmetic, not model token
savings; the subsequent screen above observes adoption but higher overall cost.

한국어: Receipt가 이미 제공하는 압축 JSON을 에이전트 실행의 기본 선택으로
명확히 안내했다. 보존된 실제 결과는 모든 필드를 유지하면서 6,036 → 5,516바이트
(8.61% 감소)다. 실행 코드·원본 보존 검사는 바꾸지 않았고 관련 테스트 59개가
통과했다. 출력 크기의 계산이며 후속 실행에서는 실제 채택됐지만 전체 비용은 늘었다.

Receipt [single-guide adoption 01](RECEIPT-GUIDE-MODEL-01-REVIEW.md), launch
`885a1f5`, resources `723be6f`: 76,746 tokens / 49.094s. The compact guide and
helper are used; original native evidence shows two defect-specific failures
before and all five current tests passing after. Literal-recipe replay matches;
original files remain unchanged and comparison copies are removed. Exposed n=1,
no contemporary baseline: no causal cost claim. Pretty output and overlapping
integrity checks remain visible extra work; featured graphs are unchanged.

한국어: 짧아진 Receipt 안내를 실제 사용한 실행은 76,746토큰·49.094초다.
원본 출력에서 수정 전 결함 2개 실패와 수정 후 기존 테스트 5개 통과를 확인했다.
같은 설정의 별도 재실행도 일치했고 원본 보존·비교용 복사본 정리를 확인했다.
기존 과제 1회·동시 기본 비교 부재로 토큰 절감 효과는 입증되지 않았다.
긴 출력과 일부 중복 무결성 검사는 남아 있으며 대표 그래프는 변경하지 않는다.

Receipt [single-guide candidate](RECEIPT-GUIDE-COMPACT-01.md), previous source
`94392cc`: guide 6,215 → 5,713 bytes (−8.08%), no new resource or runtime change.
A split was rejected because demonstrated source-layout use would read more.
Actual committed/uncommitted examples pass; causal model cost effects remain unproven.

한국어: Receipt 안내를 한 문서로 유지하면서 8.08% 압축했다. `src/` 작업에서
읽을 양이 늘어나는 분리안은 폐기했다. 실제 커밋·미커밋 비교 예제는 통과했고,
실행 코드·기능·파일 수는 그대로다. 모델 토큰·시간의 인과적 개선은 아직 입증되지 않았다.

Whole-bundle [local regression](../docs/INSTALLATION-TEST.md#whole-bundle-regression--2026-09-14-source-a636475),
source `a636475`: 518 tests / 76.826s, no failures/skips. All-eight source/copy/
package inventory and installed behavioral controls pass after recent changes.
This is local distribution/runtime evidence, not hosted CI, remote installation
or a model-efficiency measurement; no installed user configuration was changed.

한국어: `a636475` 기준 전체 518개 테스트가 76.826초에 실패·스킵 없이 통과했다.
8개 스킬 복사본·패키지 일치와 설치된 도우미의 실제 동작 검사도 포함된다.
로컬 검증이며 공개 원격 설치·호스팅 CI·모델 성능 향상의 증거는 아니다.

Friday [sequence adoption 01](FRIDAY-SEQUENCE-MODEL-01-REVIEW.md), launch `70225a0`,
resources `b2925c9`: control 73,060 tokens / 65.347s, gap 93,445 / 72.019s.
Against previous skill, control tokens −19.08% but time +2.69%; gap −1.56% /
−12.79%. Actual entrypoints, representative sequences and all-record fresh reads
are observed; both exact-program replays match complete stdout. Exposed n=1 and
different work, no contemporary baseline: not a causal/general efficiency claim.

한국어: 새 지침 실행에서 정상 73,060토큰·65.347초, 결함 93,445토큰·72.019초다.
이전 스킬 대비 정상 토큰은 19.08% 줄었지만 시간은 2.69% 늘었고, 결함은
1.56%·12.79% 줄었다. 대표 시퀀스·매번 전체 레코드 확인과 별도 재검증을 확인했다.
단일 기존 과제·작업량 차이·동시 기본 비교 부재로 일반적인 개선 주장은 하지 않는다.

Friday [representative-sequence candidate](FRIDAY-WITNESS-SEQUENCE-01.md), previous
source `ae7f566`: combine coverage obligations without caching stale observations.
An author-written 12-write/72-mixed-read sequence preserves all-row checks and
detects five intended synchronization/recovery/cross-record faults. 54 Friday
tests pass. Entry grows 522 bytes; model adoption and cost effects are unmeasured.

한국어: Friday가 모든 값·버전·작업의 조합을 늘리기보다 대표 순서에 검증 목적을
묶도록 지침을 추가했다. 직접 작성한 12회 쓰기·72회 읽기는 매번 전체 레코드를
확인하면서 결함 5종을 검출했다. 관련 테스트 54개가 통과했지만 지침은 522바이트
늘었고, 모델의 검증량·토큰 감소는 아직 입증되지 않았다.

Reviewed [acknowledged-writer screen 01](FRIDAY-ACK-01-REVIEW.md), launch `76c251c`,
resources `f15f3ae`: four executions/replays complete. Control tokens +3.91% /
time −18.42%; gap +10.13% / +20.31%. Totals +7.01% tokens / −0.29% time: no
efficiency win. Both find the gap and no control defect; gap baseline searches
outside project scope. Skill control performs 2,510 mixed reads versus 280;
unequal work/shared cache/n=1 prevent causal or general claims.

한국어: 실제 커밋·독립 연결 과제 4세션과 별도 재검증이 완료됐다. 정상은 토큰
3.91% 증가·시간 18.42% 감소, 결함은 10.13%·20.31% 증가했다. 합계 토큰
7.01% 증가·시간 0.29% 감소로 효율 개선은 입증되지 않았다. 결함 발견·정상
판정은 일치하지만 기본 실행 하나의 상위 디렉터리 검색은 범위 이탈로 기록했다.

Friday [compact screen 02](FRIDAY-COMPACT-MODEL-02-REVIEW.md), launch `135c4df`,
resources `f15f3ae`: baseline 88,162 tokens / 96.665s; skill 69,840 / 54.054s
(descriptive −20.78% / −44.08%). Both meet the visible task and separate unchanged
program replays match. Skill uses native SQLite, not the compact formatter;
baseline creates extra durable artifacts and stronger intermediate assertions.
Exposed n=1, unequal work/shared cache: no causal or general efficiency claim.

한국어: 기본 88,162토큰·96.665초, Friday 69,840토큰·54.054초로 관측상
20.78%·44.08% 감소했다. 별도 재검증도 일치했다. 기본 실행은 추가 보고서와
더 많은 중간 검증을 만들었고 스킬은 직접 SQL을 실행했다. 단일 기존 과제와
작업량 차이가 있어 전체 성능 개선으로 일반화하지 않는다.

Friday [compact candidate](FRIDAY-COMPACT-01.md), previous resource `7f5a1fc`:
entry bytes −22.03%; lossless compact JSON on the retained matrix object −7.71%.
36 matrix and 12 packaging tests pass. Checks and result fields are unchanged;
model interpretation and whole-task efficiency remain unmeasured for this edit.

한국어: Friday 안내문은 22.03%, 기존 결과 객체의 JSON은 7.71% 작아졌다.
검증 횟수와 결과 필드는 유지하고 관련 테스트 48개가 통과했다. 파일 크기 기준이며
실제 모델의 지침 채택·토큰·시간 개선은 아직 검증하지 않았다.

Collector-only [capture persistence check](CAPTURE-PERSISTENCE-01.md), previous
source `b2993d2`: preserve received CLI streams before post-run Git inspection.
A real failing-Git control and 25 runner tests pass. This prevents a separate
post-processing loss; it does not resolve the original missing-output prefix or
establish a skill improvement. No new model run or chart update.

한국어: 실행 후 Git 검사 오류가 나도 이미 받은 원본 로그를 먼저 저장하도록
수집기를 수정했다. 관련 테스트 25개가 통과했다. 기존 출력 일부 누락의 원인
해결이나 스킬 성능 향상을 뜻하지 않으며 모델 재실행·그래프 변경은 없다.

Hostage [handoff evidence screen 01](HOSTAGE-EVIDENCE-01-REVIEW.md), launch
`fe62f84`, resources `6510712`: matching report 96,307 tokens / 40.542s, stale
97,260 / 43.977s, absent 74,656 / 31.630s. Matching reuses verified prior evidence;
stale restores exact tested inputs and validly reuses that report. Absent issues a
new suite command but the original native result is missing despite a final pass
claim. Four separate native replays match expected outcomes and original resource/
file inventories reconcile; they cannot fill that gap. It exists in raw CLI stdout,
not export. Model-visible output is independently unavailable, so root cause remains
unresolved. Skill-only authored scenarios do not establish efficiency or full adoption.

한국어: 보고서 일치 조건은 재실행 없이 근거를 재사용했고, 오래된 조건은 코드를
검증됐던 상태로 복구한 뒤 해시를 확인해 재사용했다. 보고서 없는 조건은 새 검사를
요청했지만 원본 로그에 테스트 결과가 빠져 통과 여부는 미확인이다. 별도 네이티브
검증 4회는 예상대로 동작했다. 누락은 공개 변환 전 CLI 원본에도 있으며 모델이
실제로 본 출력은 별도 확인할 수 없어 원인을 단정하거나 성공률로 표시하지 않는다.

Hostage [missing-evidence delivery candidate](HOSTAGE-MISSING-EVIDENCE-01.md),
previous source `ccca07e`, makes the recovery branch explicit: attributable existing
report, observe a live execution, safe scoped rerun, or unverified delivery. Never
repeat deployment/side effects just to recover output or relabel later evidence as
the original. The native retained six-test control demonstrates a green report
becoming stale after input changes and six intended failures in a separate run.
This is local evidence reasoning, not measured model adoption or a cost reduction.

한국어: Hostage에 출력 누락 시 기존 보고서 확인·실행 중 작업 관찰·안전한 검사만
재실행·미확인 보고의 선택을 명확히 했다. 실제 테스트 6개로 코드가 달라지면 과거
성공 보고서가 현재 검증이 될 수 없음을 확인했다. 모델의 오판 감소나 비용 효과는
아직 미측정이며 배포 등 부작용 있는 작업을 출력 복구 목적으로 반복하지 않는다.

Read-only [installed-copy comparison](../docs/INSTALLATION-TEST.md#read-only-installation-comparison--2026-09-14),
previous source `be6ddeb`: `scripts/install.py --check` identifies missing, changed
bytes/modes and extra files without updating copies or replacing personal edits.
20 installation tests and the full 509-test suite pass, including all-eight matching
and real CLI failure controls. This helps users verify which local resources they have; it is not
remote freshness, hosted installation/model discovery or performance evidence.

한국어: 설치 복사본과 현재 로컬 소스를 수정 없이 비교하는 `--check`를 추가했다.
누락·내용/권한 차이·개인 추가 파일을 구분하고 덮어쓰지 않는다. 설치 테스트 20개가
통과했고 전체 509개 테스트도 통과했다. 원격 최신 여부·모델 활성화·성능 향상의 증거는 아니다.

Con Artist [focused probe routing model 01](CON-ARTIST-PROBE-ROUTING-MODEL-01-REVIEW.md),
launch `bcc6713`, resources `708c7a8`: 96,455 tokens / 46.178s, four shell calls.
Actual project/common/focused-guide reads are captured, without advanced/source
reads; all four native phases and unchanged-recipe replay match. Descriptive
−3.42% tokens / −6.35% time versus previous skill, but still +11.96% tokens versus
the earlier baseline. Different verification/output, exposed n=1 and shared cache
prevent causal or baseline-superiority claims. Earlier baseline gap stays preserved.

한국어: 모델이 실제 프로젝트와 기본·네이티브 안내만 읽고 네 단계 검증을 수행했다.
96,455토큰·46.178초로 이전 스킬 실행보다 토큰 3.42%·시간 6.35% 낮았지만,
이전 기본 실행보다는 토큰이 11.96% 많다. 작업량·단일 표본·공유 캐시 차이 때문에
인과적 성능 개선이나 전체 우월성으로 주장하지 않는다. 원래 설정 재검증도 통과했다.

Con Artist [native-probe routing candidate 01](CON-ARTIST-PROBE-ROUTING-01.md),
previous source `bf571bc`: common + focused native-probe guide is 7,785 bytes,
versus the previous 15,136-byte common/advanced read path (−48.57%). Total guide
inventory increases 3.89%; this is not model-token reduction. Old deep links and
conditional modes remain; runtime/entry unchanged. 12 packaging and 76 helper
tests pass, including execution of the new shipped example with an intended
native binary-row failure. Subsequent routing and limited cost evidence is above.

한국어: 네이티브 테스트 안내를 별도 문서로 분리했다. 필요한 두 문서만 읽으면
문서량이 48.57% 줄지만 전체 문서는 3.89% 늘었다. 기존 링크·기능은 유지하며
실제 배포 예제의 정상·결함 검사를 포함한 88개 테스트가 통과했다. 모델이 이 경로를
선택한 후속 모델 기록과 비용 비교의 한계는 위에 구분했다.

Con Artist [SQLite transfer 01](CON-ARTIST-SQLITE-01-REVIEW.md), launch `360775f`,
resources `8e3bdc4`: baseline 86,152 tokens / 69.112s; skill 99,868 / 49.308s
(+15.92% tokens, −28.65% time). Skill reads actual sources/core/native-probe guide,
verifies alias bindings, and captures all four native phases for a real disk commit
fault. Both unchanged programs replay expected outcomes; binary literals decode
identically. Baseline's original correct-existing section is missing and remains
unverified. Skill loads the whole advanced guide; targeted routing remains costly.
New authored n=1 task, unequal work/shared cache: no causal or broad efficiency win.

한국어: 새 SQLite 과제에서 스킬이 실제 파일·함수 연결과 디스크 커밋 누락을
검증했다. 토큰은 15.92% 늘고 시간은 28.65% 줄었다. 원래 프로그램 재검증도
예상대로 동작했지만 스킬 미적용 원본의 첫 정상 테스트 출력 누락은 그대로 남긴다.
스킬은 필요한 네이티브 테스트 안내뿐 아니라 상세 문서 전체를 읽었다. 다른 구조에
적용되는 것은 확인했지만 단일 작성자 과제의 결과를 일반적인 성능 향상으로 주장하지 않는다.

Con Artist [short-guide screen 01](CON-ARTIST-CORE-GUIDE-MODEL-01-REVIEW.md), launch
`da333ab`, resources `8e3bdc4`: 73,679 tokens / 35.540s, three recorded shell calls.
All four actual audit phases and copied binding/integrity evidence are captured;
unchanged-recipe author replay reproduces them. However, no project-source or guide
read is recorded, so **guide adoption is unverified**. Descriptive −28.12% tokens /
−7.79% time versus checkpoint 08 is not an accepted causal gain: exposed n=1,
unequal reads/work and shared cache. Frozen exports remain, featured unchanged.

한국어: 새 Con Artist 실행은 73,679토큰·35.540초였고 네 단계 검증 결과와
복사본 바인딩·원본 보존을 확인했다. 하지만 기록에 프로젝트 코드와 수정 안내를
읽은 단계가 없어 안내 채택은 미확인이다. 이전 단일 실행보다 토큰 28.12%·시간
7.79% 낮았지만 수정 효과로 인정하거나 전체 성능 그래프에 반영하지 않는다.

Con Artist [core-guide candidate 01](CON-ARTIST-CORE-GUIDE-01.md), previous source
`58d31fb`: routine guide 7,189 → 5,190 bytes (−27.81%), core plus advanced −9.27%.
Repeated prose is compressed; cleanup mechanics remain in the routed advanced
section. The executable recipe, binding/evidence/integrity limits and legitimate
source inspection remain. 76 helper and 12 packaging tests pass, including the
actual shipped recipe's positive/fault checks. Runtime/entry unchanged; model
adoption remains unverified in the subsequent screen above; no accepted token-saving claim.

한국어: Con Artist 기본 안내를 27.81% 줄였고 상세 문서까지 합치면 9.27%
감소했다. 필요한 결함·바인딩·실행 결과 검증은 유지했으며 실제 배포 예제를 포함한
도구·패키징 테스트 88개가 통과했다. 문서 크기 감소이지 모델 토큰 절감률은 아니며,
이후 실행에서도 안내를 읽은 기록이 없어 모델 채택과 수정 효과는 미확인이다.

[All-eight checkpoint 08](BUNDLE-CONTRACT-08-REVIEW.md), resources `ecff8a8`:
all 18 scheduled sessions complete; summed tokens 747,430 baseline / 743,068 skill
(−0.58%), process time 533.487s / 453.064s (−15.08%). Six pairs use more tokens,
three cost more on both axes. Two original native-output gaps remain unverified:
protected-search baseline and pending-form skill. All raw usage/resource hashes,
original modes and full retained inventories reconcile; 22 separate unchanged-test
controls match expected outcomes, including valid duplicate-return alternatives.
Replay cannot repair capture gaps. Exposed authored tasks, n=1, shared host/cache
and unequal extra work do not establish causal or broad real-developer gains.
Friday adopts the shorter guide but still uses more tokens in this pair; Con Artist
prints its entire implementation. No featured promotion or hosted release claim.

한국어: 8개 스킬·9개 과제·18개 세션을 모두 완료했다. 전체 토큰 합계는 0.58%,
실행 시간 합계는 15.08% 낮았지만 과제 6개는 토큰이 늘었고 3개는 두 비용이
모두 늘었다. 원본 테스트 출력 누락 2건은 미확인으로 남긴다. 별도 검증 22개는
정상·허용 가능한 대체 구현 통과와 결함 검출을 확인했지만 원본 누락을 채우지 않는다.
기존에 사용한 작성자 과제·조건별 1회·작업량 차이 때문에 일반적인 성능 향상이나
공개 배포 준비 완료로 주장하지 않는다. 기존 그래프 수치는 변경하지 않았다.

## Earlier focused checks — 2026-09-14

Friday [short-guide model 01](FRIDAY-CORE-GUIDE-MODEL-01-REVIEW.md), launch `37686ac`,
resources `ce82fcb`: 89,545 tokens / 54.127s, four shell calls. Reads only the core
guide; API executes once and retained results drive full column/value assertions.
All four phases/eight reader outputs captured, original files/resources unchanged.
Separate exact-program replay reproduces observations and rejects rollback row
loss. Descriptive tokens −18.13%, time +19.88% versus checkpoint 07: unequal work,
n=1/shared cache, not causal or all-axis improvement. Git-internal discovery remains.

한국어: 짧은 Friday 안내만 읽고 한 번의 SQL 결과로 열·값·롤백 데이터까지 확인했다.
89,545토큰·54.127초이며 이전 단일 실행보다 토큰은 줄고 시간은 늘었다. 원본 출력과
별도 데이터 손실 검증은 확인했지만 전체 성능 개선으로 주장하거나 그래프를 바꾸지 않는다.

Friday [core-guide candidate](FRIDAY-CORE-GUIDE-01.md), previous source `c1f639c`:
routine reference 4,884 → 3,645 bytes (−25.37%); core plus details 7,387 → 7,205
(−2.46%). Conditional BLOB/rejection diagnostics stay in the existing routed
details file. CLI/API examples and 35 native matrix tests pass; runtime and skill
entry unchanged. These are document bytes, not model token or performance gains.
Subsequent adoption and mixed cost evidence is above; no historical/featured changes.

한국어: Friday 기본 안내를 줄이고 조건부 상세 설명은 기존 문서로 옮겼다.
기본 문서 크기는 25.37% 줄었지만 전체 문서는 2.46% 감소이며, 모델 토큰 절감률이
아니다. 실제 예제를 포함한 SQLite 검사 35개가 통과했고 실행 코드는 변경하지 않았다.

[Final batching model 01](HOSTAGE-FINAL-BATCH-MODEL-01-REVIEW.md), launch `d035f34`,
resources `fc557ad`: 95,992 tokens / 94.261s, four shell calls, final checks in one
failure-preserving call. Sequential dependent phases adopted. Original summary
says ten pass but only five headers are captured; preserve that gap. Six separate
unchanged-test replays accept final/alternate results and reject four faults,
without prior unbound-local errors. Descriptive −19.31% tokens / −8.63% time versus
keyed-import 01 is not causal: n=1, shared host/cache and unequal verification.
No featured promotion or all-eight performance claim.

한국어: 새 모델이 최종 검사를 한 호출로 묶고 의존 단계도 실패 시 중단하도록
작성했다. 95,992토큰·94.261초로 이전 단일 실행보다 낮았지만 작업량·캐시 조건이
달라 일반적 절감으로 주장하지 않는다. 원본의 테스트 이름 일부 누락은 보존했고,
별도 재실행은 정상·대체 구현 통과와 결함 검출, 부차적 오류 해소를 확인했다.

Hostage [final-check batching candidate](HOSTAGE-FINAL-BATCH-01.md) addresses three
separate finalization calls in the keyed-import trace and masked intermediate
statuses. Native controls exercise six unchanged retained tests, real cmp and Git:
normal batch passes; test/copy/original-test/whitespace faults return nonzero,
while semicolon chains end in zero. Initial cmp-message assertion error disclosed.
No new runtime; this local check alone does not measure adoption or gains.
The subsequent model screen and its limits are above.

한국어: 마지막 테스트·복사 확인·diff/status를 판단이 필요한 중간 단계가 없을 때
한 호출로 묶도록 안내를 구체화했다. 실제 명령 검증에서 4종 실패를 최종 성공
상태가 가리지 않음을 확인했다. 이후 모델 채택 결과와 측정 한계는 위에 구분했다.

Python [dependent-phase guidance](HOSTAGE-DEPENDENT-PHASES-01.md), author control
on `e8ab180` artifacts: unwrap only two continuing subtests around dependent
phases. Twelve native runs preserve final/alternate passes and all four fault
detections, while removing secondary unbound-local errors from three fault
variants. Assertions/waits/cleanup and independent subtests remain. Optional
Python asset docstring only; runtime unchanged. Subsequent adoption evidence and
cost/capture limitations are above, separate from this author adaptation.

한국어: 서로 의존하는 콜백 단계는 앞 단계 실패 후 정리로 빠지도록 Python 사용
안내를 보완했다. 작성자 적용본의 12회 실행에서 정상·대체 구현 통과와 결함 검출을
유지하며 3개 결함 실행의 부차적 오류를 없앴다. 이후 실제 모델 채택은 위에 별도로
기록했으며 원본 모델 테스트와 그래프는 변경하지 않았다.

[Keyed import transfer 01](HOSTAGE-KEYED-IMPORT-01-REVIEW.md), launch `6d0d108`,
resources `c0aa9a1`: one skill-only cell, 118,971 tokens / 103.161s. Original six
native tests pass; unchanged-test replay accepts a valid False-returning duplicate
and detects missing guard/cleanup and all-key blocking. Faulty variants also reveal
secondary unbound-local errors from continuing dependent subtests. The task
explicitly clarifies unspecified returns, so this does not isolate the instruction
effect or establish efficiency/general real-project gains. No skill/featured change.

한국어: 다른 키는 계속 처리하는 2단계 가져오기 작업에서도 새 API를 사용했다.
정상·대체 반환값 구현은 모두 통과하고 중복·복구·키별 독립성 결함을 검출했다.
다만 실패 뒤 다음 단계까지 진행하는 subtest 구조에서 추가 오류도 발견했다.
과제가 반환값 계약을 명시하므로 스킬만의 효과나 비용 절감으로 주장하지 않는다.

Python [callback adoption 01](HOSTAGE-PYTHON-ENTRY-MODEL-01-REVIEW.md), launch
`08a8f6e`, resources `4b79eb9`: 114,248 tokens / 87.024s, one skill-only cell.
Actual task-aware API use and original 6/6 native passes are confirmed. Separate
replays detect missing guard/cleanup but reject a valid False-returning duplicate
suppression path: the generated test invents a None-return contract. A narrow
post-run instruction correction is subsequently exercised by the transfer screen
above, with an explicit-task-clarification confound. Full-asset reading
and deadline-based missing-guard failure remain; no efficiency/featured claim.

한국어: Python 새 API 사용과 원본 테스트 6개 통과를 확인했지만, 정상 중복 차단의
반환값까지 None으로 강제하는 과잉 검증을 발견했다. 이를 막는 지침을 수정했고
이후 다른 과제에서 사용했지만 지침만의 효과는 분리하지 못했다. 114,248토큰·87.024초로 비용 절감을
입증하지 못했고 기존 결과·이미지는 그대로 보존한다.

Distribution check: [all-eight skills CLI install](SKILLS-CLI-INSTALL-01.md),
source `45fe88e`, `skills@1.5.26`: all 38 files/modes match in a network-disabled
disposable project. Seven Python entrypoints and installed Python/JS task-aware
callbacks execute. The initial checker catalog-scope error is preserved. CLI
package/dependencies were downloaded with lifecycle scripts disabled into ignored
scratch only; no global install, host registration or remote-authentication claim.

한국어: 실제 skills CLI로 임시 프로젝트에 8개를 설치해 38개 파일·권한 일치와
실행 파일을 확인했다. 설치 안내에 테스트한 CLI의 Node 버전 요구사항을 명시했다.
전역 설치·계정 설정·공개 전환은 하지 않았으며 모델 성능 수치와는 별개다.

Release check at `57d48fd`: [network-disabled Linux source archive](LINUX-ARCHIVE-497-01.md)
discovers 497 tests, 494 pass, three explicit Git-provenance skips, 28.060s.
The first `7087e52` archive error is preserved; only the unavailable Friday
history comparison is skipped, while schedule checks still run. Checkout CI now
requests full history. Hosted run `34821858042` at `7087e52` still has zero steps
in all four failed jobs (payment/spending-limit annotation); private visibility
unchanged. Local archive behavior is not hosted CI or model efficiency evidence.

한국어: Linux 배포 아카이브에서 497개 중 494개가 통과했고, Git 이력 비교 3개는
명시적으로 건너뛰었다. 첫 실패는 보존하고 이력 없는 배포본의 검사 전제를 고쳤다.
일반 CI는 전체 이력을 받도록 했지만, 호스팅 CI는 계정 제한으로 실행 전 실패
상태이며 저장소 공개·계정 설정은 변경하지 않았다.

Current Friday preparation optimization: [shared reader snapshot](FRIDAY-READER-SNAPSHOT-01.md).
Multiple literal queries from one module share a validated read/parse within one
matrix call. A native three-check case goes from three parses to one; SQL still
runs after every phase, new invocations reread changed files, and repeated inputs
still consume the full byte budget. This does not target the older two-file
rolling-schema pair and is not model-level efficiency evidence.
macOS suite at `7087e52`: 496 passed in 69.115s, no failures/skips.

한국어: 한 Python 파일의 여러 쿼리를 검사할 때 읽기·구문 분석을 한 번만 하도록
개선했다. SQL 결과는 재사용하지 않아 단계별 데이터 변경을 계속 확인한다.
로컬 처리 최적화이며, 기존 모델 실험의 토큰 증가가 해결됐다는 뜻은 아니다.

Current Python Hostage runtime addition: [task-aware entry](HOSTAGE-PYTHON-ENTRY-WAIT-01.md).
An optional wait detects an already-finished application rather than spending its
entry deadline. Local tests cover exact outcomes, both cancellation directions,
queued-entry preservation and competing consumers; correct two-stage behavior
passes and skipped decode yields the actual completed payload. This local check
does not measure model adoption/cost; the subsequent adoption screen is above.
No historical score or featured change.
Local suite at `6d57e68`: 494 passed in 68.746s, no failures/skips.

한국어: Python에도 앱 작업 종료를 확인하는 선택형 콜백 대기를 추가했다. 대기만
취소해도 앱 작업은 유지하고, 취소와 콜백 진입이 겹쳐도 콜백을 잃지 않는지
검증했다. 이 로컬 검사는 모델 효과를 측정하지 않으며, 이후 채택 실험은 위에
별도로 기록했다.

Measurement review improvement — 2026-09-14: the runner flags direct `node --test`
commands without complete TAP/spec count summaries for manual review. Retained
entry-wait model evidence flags `item_8` only, not its final 45-pass command.
Native success/failure reporter controls pass; diagnostics never rescore results
or rewrite frozen metadata. This improves evidence review, not skill performance.
Local suite at `4ca29d1`: 486 passed in 68.961s, no failures/skips.

한국어: Node 테스트 요약 출력 누락을 자동 검토 대상으로 표시한다. 기존 결과를
실패로 바꾸거나 출력 누락을 복구하는 기능은 아니며, 성능 향상 수치도 아니다.

Hostage [fresh task-aware entry adoption](HOSTAGE-ENTRY-WAIT-MODEL-01-REVIEW.md),
launch `e26ea1d`, resource `328bc1f`: 151,437 tokens / 156.115s, one skill-only
session. Actual tests use the API with their corresponding application tasks.
Final native 45/45 passes; first test command output is empty despite exit 0,
preserved as a capture gap. Twelve unchanged-test replays match, including
eight skipped-decode failures in 0.0992s without entry deadlines and valid mutable
updates passing 45/45. Full-module rereading persists. No baseline, broad model
efficiency claim or featured update.

한국어: 새 모델이 작업 종료 감지 API를 올바른 요청에 연결해 사용했다. 마지막
원본 테스트 45개 통과는 확인했지만 첫 테스트 명령의 출력 누락은 그대로 남겼다.
별도 재실행에서 누락된 콜백 8건을 약 0.10초에 검출했다. 모델 전체 속도 개선이
아니며, 151,437토큰·156.115초를 사용했고 구현 전체 읽기도 남아 있다.

Current Hostage runtime addition: [task-aware callback entry](HOSTAGE-ENTRY-WAIT-01.md).
Optional `startedBefore(task)` reports early task settlement instead of waiting
for an impossible entry until timeout. Author-adapted retained tests preserve
43/43 final passes and eight skipped-decode detections; fault diagnosis changes
from 8.1120s to 0.1024s. First adaptation error is preserved; corrected native
timing overlaps author regressions, n=1; that local result is not model evidence.
Local suite at `328bc1f`: 483 passed in 67.999s, no failures/skips.

한국어: 앱 작업이 끝났는데 콜백 진입을 계속 기다리던 비용을 줄이는 선택형 API를
추가했다. 작성자 적용본은 정상 43개 통과·결함 8개 검출을 유지하면서 실패 진단이
8.1120초에서 0.1024초로 줄었다. 첫 적용 스크립트 오류도 보존했다. 모델 전체
성능 수치가 아니며, 이후 모델 채택 결과는 위의 별도 기록으로 구분한다.

Current Hostage [copy-check model review](HOSTAGE-COPY-CHECK-MODEL-01-REVIEW.md),
launch `b2b213a`, resource `ee1fa12`: 148,517 tokens / 166.259s, one skill-only
session. `cmp` succeeds as the final shell command, but full implementation is
still printed after the usage header. Copy verification adopted; cheap reading
not established. Original 43/43 native passes; 12 separate replays match,
including valid mutable updates and rejection of stale in-place changes.
Unequal extra work, deadline-based detection of skipped decode, no baseline or
efficiency claim. No favorable retry or featured change.

한국어: 새 모델이 복사본 비교를 실제로 사용했지만 그 전에 구현 전체를 읽었다.
148,517토큰·166.259초, 원본 테스트 43개 통과와 별도 결함 재실행 12개를 확인했다.
복사 확인 채택과 중복 읽기 해소는 다르며, 절감 효과를 입증한 결과는 아니다.

Current Necromancer runtime correction: [Git physical lines](NECROMANCER-PHYSICAL-LINES-01.md).
LF-only parsing and byte-preserving UTF-8 decoding keep current source, blame
and patch rows aligned. All 27 real-Git separator/ending combinations pass;
model adoption and cost remain unmeasured for this correction.
Local suite at `6806512`: 481 tests passed in 68.185s, no failures/skips.

한국어: 이력 수집기가 문자열 속 구분 문자나 CR 때문에 현재 코드와 Git 이력을
다르게 표시하던 오류를 수정했다. 실제 Git 저장소의 27개 조합을 검증했으며,
모델 성능 향상 수치로 해석하지 않는다.

Current Con Artist runtime correction: [physical source lines](CON-ARTIST-PHYSICAL-LINES-01.md).
Valid UTF-8 string separators previously shifted AST excerpts and silently
omitted source. The collector now uses Python physical line boundaries while
preserving raw hashes, cache and no-execution behavior. Targeted native Python
checks pass; model adoption/cost for this revision are not yet measured. Other
skill runtimes and historical results remain unchanged.
Local suite at `c7683ca`: 480 tests passed in 65.191s, no failures/skips.

한국어: 테스트 감사용 코드 수집기가 문자열 속 유니코드 구분 문자를 줄바꿈으로
잘못 세어 코드를 잘라내던 오류를 고쳤다. 원본 해시와 읽기 전용 동작은 유지했다.
로컬 재현·수정 검증이며, 새 버전의 모델 비용 개선을 주장하지 않는다.

[State-content model adoption](HOSTAGE-STATE-CONTENTS-MODEL-01-REVIEW.md), launch
`8bad531`, resource `691f896`: one fresh skill-only session completes in 130.943s /
171,403 total tokens. Actual generated snapshots compare state fields; original
58/58 native passes. Twelve separate replays match: correct guarded mutable
updates pass 58/58, stale in-place success/error fail 16/32 tests respectively.
Raw/resources/originals/copy reconcile; no observed scope/capture exception.
Some other faults hit individual deadlines; original-plus-broken replays use
90-second process bounds. The model also rereads the full module after its header.
Observed aliasing weakness is corrected in this output; no comparative efficiency
claim, no broad completion. Earlier failed results remain unchanged. Full local
preflight: 476 tests passed in 65.156s, no failures/skips.

한국어: 새 모델이 직접 작성한 테스트도 상태 필드의 전후 값을 비교했다.
정상적인 내부 수정은 58개가 통과하고, 오래된 요청의 내용 덮어쓰기는 성공·오류
경로에서 각각 16개·32개 실패로 잡아냈다. 이번에는 비교군 없는 동작 확인이며
171,403토큰·130.943초를 썼다. 전체 구현 재읽기와 일부 느린 실패 진단이 남아
있고, 이전 실패 기록이나 그래프를 새 성과로 바꾸지 않는다.

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
