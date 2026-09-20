# Release check — 2026-09-20, source `21ed1a4`

**Not a release approval or performance benchmark.** The installed skill archive
and repository source archive are different deliverables; do not generalize one
passing check to the other.

## Updated checkout and source archive pass — 2026-09-21, source `e874ace`

Full Python3.11 native discovery completed for the source containing the context
output-budget correction and new Friday/HTTPX pilot support:

- Checkout: **874 tests, 154.211 seconds, OK**, exit 0, no skips.
- Fresh `git archive e874ace` outside any repository: **874 tests, 145.148 seconds,
  OK (skipped=20)**, exit 0; neither `.git` nor `benchmarks/local-runs` is present.
- Metadata/local-link validation and featured synchronization pass in both;
  checkout whitespace check passes and the measured checkout was clean.
- Local logs: `/tmp/qh-e874ace-checkout.log` and
  `/tmp/qh-e874ace-archive.Gn8zFA/native-check.log`.

The suites ran concurrently. These times are not an efficiency comparison and
the result does not prove hosted installation, model performance or release approval.
The 20 source-archive skips remain explicit history/provenance availability checks;
no additional skip was introduced to accommodate the new changes.

Latest hosted [run 35527095454](https://github.com/SoonGwan/questionable-hires/actions/runs/35527095454)
at `e874ace` has four failed jobs with no executed steps. Source-archive check
`106121045882` again attributes non-start to failed account payments or a spending
limit. Billing/settings, repository visibility and workflows were not changed or
retried. Repository remains **PRIVATE**, default branch **main**. Hosted validation
requires owner action; broad whole-task efficiency remains unproven independently.

한국어: 최신 소스 작업본 874개가 모두 통과했고, Git 없는 압축본도 20개 이력
의존 검사를 명시적으로 건너뛴 채 통과했다. 회귀·배포 형태 검증 결과이며 성능
향상이나 공개 배포 완료를 뜻하지 않는다. GitHub CI는 여전히 계정 문제로 실행 전
실패하고 저장소는 비공개다. 계정 설정이나 공개 여부는 변경하지 않았다.

## Historical checkout and source archive pass — 2026-09-21, source `a2d0002`

Both full Python3.11 runs completed with `python -B -m unittest discover -s tests -q`:

- Checkout: **867 tests, 161.689 seconds, OK**, exit 0; no skips.
- Fresh committed source archive: **867 tests, 151.549 seconds, OK (skipped=20)**,
  exit 0. The archive has neither `.git` nor `benchmarks/local-runs`; absent-history
  checks are described in the historical isolation checkpoints below.
- Checkout and archive both pass metadata/document-link validation and featured
  benchmark synchronization. Checkout also passes `git diff --check` and is clean.
- Local logs: `/tmp/qh-a2d0002-checkout.log` and
  `/tmp/qh-a2d0002-archive.PY7lxa/native-check.log`; not published evidence files.

These are correctness/distribution checks, not model performance measurements.
The two suites ran concurrently; their runtimes are not a checkout/archive speed
comparison. This source includes the dynamic Receipt binding support and the
reviewed, unadopted Hostage input candidate experiment.

Fresh GitHub inspection at this source: [run 35524718593](https://github.com/SoonGwan/questionable-hires/actions/runs/35524718593)
has four failed jobs, each with no executed steps. Source-archive check
`106114769361` reports failed account payments or a spending limit requiring
attention. No workflow retry, billing/settings change or visibility mutation was
performed. Owner action remains necessary for hosted validation; it is not a
test-code failure established by CI. The repository remains **private**, default
branch **main**, MIT license. This does not prove unauthenticated remote install
or approve public release. Broad all-eight token/time improvement remains unproven.

한국어: `a2d0002`의 개발 체크아웃 867개 검사는 모두 통과했고, Git 없는
압축본도 867개 중 20개를 건너뛰고 나머지가 통과했다. 양쪽의 문서·메타데이터·
그래프 동기화도 확인했다. GitHub CI는 결제·지출 한도 문제로 실행 전 실패하며
계정 설정은 변경하지 않았다. 저장소는 여전히 비공개다. 로컬 검증 통과를 모델
성능 향상, 원격 설치 성공 또는 공개 배포 승인으로 표현하지 않는다.

## Checkout and source archive pass — historical, 2026-09-21, source `b78d4d4`

Both previously launched full runs completed on Python3.11.16, with
`python -B -m unittest discover -s tests -q`:

- Checkout: **848 tests, 147.830 seconds, OK**, exit 0; no skipped tests.
- Fresh committed source archive: **848 tests, 138.010 seconds, OK (skipped=20)**,
  exit 0. The 20 history-dependent checks cannot compare absent Git objects;
  synthetic behavior and native controls execute independently, as described below.
- Temporary local logs: `/tmp/qh-b78d4d4-checkout.log` and
  `/tmp/qh-receipt-source.vcUfiM/native-check.log`. They are not published artifacts.
- These concurrent local runs establish correctness at this source, not a relative
  performance comparison between checkout and archive.

After launch, an additional installed-helper regression was added (not included
in the 848-test totals). It installs Mother-in-law in a disposable project and
executes the installed script with isolated Python: guarded behavior exits 0,
stale overwrite exits 1, and pre-fetch setup failure exits 2 with its cause before
the two-second outer deadline. Installed bytes/modes and project source remain
unchanged; no leftover files. Both installed-recent-helper tests pass in **0.803
seconds**. Metadata/link validation and featured synchronization also pass.

Hosted CI is **not green**. Fresh inspection of
[run 35520919370](https://github.com/SoonGwan/questionable-hires/actions/runs/35520919370)
at `b78d4d4` shows all four jobs failed before any steps. The source-archive job's
annotation reports failed account payments or a spending limit requiring attention.
No billing/settings changes or workflow retries were made. This account-level
issue must be resolved by the owner before hosted validation can establish a pass.
Local success does not establish remote installation, publication readiness or
the outstanding whole-task model-efficiency objective.

한국어: `b78d4d4`에서 개발 체크아웃 848개와 Git 없는 압축본 848개 검사가 모두
통과했다. 압축본에서는 과거 이력 대조 20개만 건너뛰며 실제 동작 검사는 유지한다.
이후 추가한 설치형 도구 검사도 정상·결함·미완료를 구분하고 원본을 보존했다.
GitHub CI는 계정 결제 또는 지출 한도 문제로 실행 전 실패했다. 계정 설정은
변경하지 않았으며 원격 CI 통과·배포 승인·모델 전체 성능 향상을 뜻하지 않는다.

## Receipt copy/rewrite/schedule isolation — 2026-09-21, parent `bc4edd8`

Receipt read/route candidate transforms and read/route/startup/preserve schedule
tests now use explicitly synthetic Git objects while exercising the unchanged
copy/rewrite and runner logic. Real pinned read/route transformations and every
preserve snapshot byte/mode remain separate historical checks. Native controls
continue to run from hash-verified shipped code; no model/native result is mocked
as part of those native checks. Scheduling-only model calls remain mocked.

Related validation on Python3.11.16: **21 tests, 7.141 seconds, OK**. The independent
Git-free source wrapper now executes all six Receipt modules: **19 nested tests,
16 execute and three history-only checks skip**. This includes all four real
native preflights, both instruction transformations, schedule/exclusive execution
and tamper rejection. The wrapper verifies source preservation, scratch cleanup,
and rejection of a changed native helper. An initial sparse-copy check caught an
omitted `preserve.py` identity input; the wrapper now includes that actual file.

Frozen runners, fixtures, published measurements and production skills are
unchanged. Full checkout and source-archive suites must still be rerun before
claiming the previous remaining errors are resolved globally.

한국어: 남아 있던 Receipt 후보 변환·실행 순서 검사를 Git 이력과 분리했고 관련
21개 검사가 통과했다. Git 없는 소스의 19개 중 실제 동작 16개가 실행되고 과거
파일 대조 3개만 건너뛴다. 전체 재검사 전이므로 오류 0개나 배포 준비 완료를
아직 주장하지 않는다. 기존 측정값과 배포용 스킬은 변경하지 않았다.

## Full archive recheck and Receipt native controls — 2026-09-21, parent `954c685`

The previously launched fresh archive of `954c685` completed on Python3.11.16:
**843 tests, 126.868 seconds, 14 errors, 16 skips**, exit 1. Local temporary log:
`/tmp/qh-roundtrip-source.JBaj0y/native-check.log`. All remaining errors are Receipt
preserve (3), read (4), route (4) and startup (3) checks. This is an observed full
run, not subtraction from targeted results; source-distribution validation is
still incomplete.

The subsequent change separates four native preflights from historical Git
availability. Their shipped `compare.py` bytes have SHA256
`a94b827a6fd346a93adbfb6ea4b3606d66b26f7e5201a035da7fc853978c2fe7`;
a separate real-history test compares them with both `ca668a4` and `55fe666`.
The native controls execute unchanged in owned temporary roots, including real
before/after tests, complete/partial fixes, helper incompatibility, deliberately
disabled startup, source preservation and cleanup. No native result is mocked.
Supplying verified bytes to the preflight's Git-content lookup is explicitly not
a claim that archive-local Git history exists.

Four native checks pass in **2.806 seconds**. Two additional checks pass in
**3.305 seconds**: pinned-byte provenance and an independent Git-free source copy
that actually runs all four controls without skips. The archive check verifies
no source changes or leftover scratch, then modifies the disposable helper and
confirms all four controls reject its changed identity. Frozen runners, fixtures
and model evidence remain unchanged. This does not establish a post-change full
archive error count or model performance gain.

한국어: `954c685` 압축본 전체 843개 검사에서 오류 14개·건너뛰기 16개가 확인됐다.
이후 Receipt 네이티브 대조 4개를 Git 이력과 분리해 실제 실행을 유지했다. 별도
Git 없는 소스에서도 정상·결함·잘못된 시작 설정 대조가 실행되고, 도구 변조 시
4개 모두 거부된다. 전체 압축본의 수정 후 오류 수나 모델 성능 개선은 아직
새로 주장하지 않는다.

## Roundtrip and HTTPX schedule isolation — 2026-09-21, parent `ec4a538`

The rejected Hostage roundtrip candidate and historical HTTPX probe tests now use
explicitly synthetic Git objects for resource-copy/rewrite, execution-order,
exclusive-run and tamper-rejection behavior. Roundtrip additionally checks bad
rewrite anchors and retained incomplete limit-hit cells. Neither frozen runner
nor the original HTTPX source validator/native preflight was changed. Real pinned
resource comparisons remain separate checks and execute in the full checkout.

Targeted Python3.11 validation: **11 tests, 1.047 seconds, OK**. The included fresh
Git-free source-copy wrapper runs 25 nested tests: **19 behavior checks execute,
six history-only comparisons skip explicitly**. It checks passed test identities,
unchanged source bytes and no leftover scratch. No model calls were made; synthetic
token/time values in mocked scheduling tests are not performance measurements.
This is not yet a fresh full-archive error count or release approval.

한국어: 과거 roundtrip·HTTPX 실행기 검사의 Git 의존성을 분리했고 관련 11개가
통과했다. Git 없는 별도 소스에서도 동작 검사 19개가 실행되며 과거 파일 대조
6개만 명시적으로 건너뛴다. 기존 모델 측정·실행기·실제 HTTPX 검증은 바꾸지
않았다. 전체 압축본 재검사나 배포 승인, 성능 향상 수치는 아니다.

## Checkout recheck — 2026-09-21, source `fab7824`

Python3.11.16, `python -B -m unittest discover -s tests -q`: **830 tests in
141.759 seconds, OK**, exit 0. Working tree clean after test cleanup. Validation
also passes for all eight hires, UI metadata, plugin references, issue forms and
local documentation links; featured benchmark synchronization passes unchanged.
This is checkout validation, not a full source-archive rerun or model benchmark.

한국어: `fab7824` 개발 체크아웃의 전체 830개 검사가 통과했다. 8개 스킬 구조와
문서 링크·대표 벤치마크 동기화도 통과했다. 압축본 전체 재검사나 모델 성능 검증을
대신하는 결과는 아니다.

## Full archive recheck and mode-test isolation — 2026-09-21, parent `7f09841`

A fresh Git-free archive of `7f09841` completed **827 tests in 126.651 seconds:
23 errors, 13 skips**, exit 1, on Python3.11.16. The local log is
`/tmp/qh-bundle-source.05wj5L/native-check.log` (temporary, not published).
Remaining errors are Hostage modes (3), Hostage roundtrip (3), HTTPX probe (3),
Receipt preserve (3), Receipt read (4), Receipt route (4), and Receipt startup (3).
These are source-distribution validation failures, not measured model failures.

The subsequent mode-test change exercises the unchanged snapshot/split logic with
explicit synthetic Git objects. It checks preserved metadata/assets, rebased links,
missing/duplicate relocation anchors, tamper rejection, exclusive execution, and
retention of an incomplete limit-hit cell without restart. The actual historical
resource comparison remains a separate check, executed when owned history exists.
No frozen runner, fixture, model result, or production skill was modified.

Targeted checkout validation: **7 tests in 0.785 seconds, OK** on Python3.11.16.
This includes an independent Git-free wrapper with **15 nested tests: 11 behavior
checks execute and four history-only checks explicitly skip**. The targeted result
does not establish a new full-archive error count or prove model cost savings.

한국어: `7f09841`의 전체 압축본 검사 827개에서 오류 23개·이력 전용 건너뛰기
13개가 확인됐다. 이후 모드 후보 검사의 Git 의존성을 분리했고 관련 7개가 통과했다.
별도 Git 없는 소스에서도 동작 검사 11개는 실제 실행된다. 과거 모델 결과와 배포용
스킬은 바꾸지 않았으며, 전체 배포 준비 완료나 모델 성능 향상을 뜻하지 않는다.

## Bundle checks isolated from Git history — 2026-09-21, parent `d5c37e2`

All-eight current02 and Korean automatic-selection scheduling/tamper tests now
exercise the unchanged runner's snapshot logic with explicitly synthetic eight-role
Git object fixtures. They do not use invented historical evidence. Real pinned
snapshot bytes/modes are checked separately when the owned Git history exists.
Lean rewriting similarly runs an eight-entry/frontmatter/support-mode test without
history; its real pinned-resource comparison remains separate.

An independent fresh source-copy regression (no `.git`, no `local-runs`) discovers
nine selected checks: six behavior checks execute, three history-only checks skip
explicitly. It asserts actual passed test identities, snapshot source preservation,
and absence of leftover scratch. Native checkout validation across those modules
and both archive wrappers: **11 tests, 5.818 seconds, OK** on Python3.11.16.
The real historical checks execute in this checkout. Frozen model runners, cases,
results and production skills were not changed, and no model calls were made.

This repairs the five failing checks in these three modules from the `5b10619`
inventory; it does not establish a new remaining full-archive error count. A fresh
complete archive run is still required; do not subtract targeted results from the
older full-suite totals or call the release ready.

한국어: 8개 묶음·한국어 자동 선택·경량 후보의 동작 검사와 실제 과거 커밋 대조를
분리했다. Git 없는 별도 소스에서 동작 6개를 실행하고 이력 전용 3개만 명시적으로
건너뛴다. 개발 체크아웃에서는 실제 이력 대조까지 포함한 관련 11개가 통과했다.
전체 압축본의 남은 오류 수나 모델 성능 개선은 아직 새로 주장하지 않는다.

## Full recheck at `5b10619` — 2026-09-20

Python 3.11.16, `python -B -m unittest discover -s tests -q`:

- Existing checkout: **806 tests, 144.152 seconds, OK**, exit 0.
- Fresh `git archive HEAD` extracted outside the checkout, without Git metadata
  or pre-existing local-runs: **806 tests, 128.325 seconds, 28 errors, 10 skips**,
  exit 1. Native log retained locally at
  `/tmp/qh-source-check.7cF8OL/native-check.log` (temporary, not a published artifact).
- Remaining errors belong to the historical all-eight runner (2), Hostage modes
  candidate/runner (3), Hostage roundtrip candidate (3), HTTPX probe (3), Korean
  auto runner (2), lean schedule (1), Receipt preserve runner (3), Receipt read
  candidate/runner (4), Receipt route candidate/runner (4), and Receipt startup
  runner (3). They still attempt Git access from the source archive. This is an
  unresolved source-distribution validation defect, not 28 observed skill failures.

This recheck includes the expression-depth correction and the accumulated
native-control/schedule isolation changes. It does not change frozen model
results, prove token savings, or establish hosted CI/remote installation success.
No hosted check was rerun in this recheck. The earlier hosted failure below is
historical, not a newly verified account status.

한국어: `5b10619` 전체 재검증에서 개발 체크아웃은 806개 모두 통과했다.
Git 없는 새 소스 압축본은 같은 806개 중 오류 28개·건너뜀 10개로 실패했다.
남은 오류는 과거 커밋을 읽는 검사에 있으며, 실제 스킬 오류 28개라는 뜻은
아니다. 그래도 압축본 검증은 미완료다. 모델 성능·원격 설치·호스팅 CI 통과로
해석하지 않으며 기존 성능 그래프는 바꾸지 않는다.

## Observed checks before the scratch-parent repair

- Existing checkout, Python 3.11.16, `python -B -m unittest discover -s tests -v`:
  **783 tests, 137.521 seconds, OK**. This checkout has Git history and an existing
  ignored `benchmarks/local-runs` directory.
- This includes `test_reproducible_archive_installs_all_resources_offline`:
  deterministic standalone skill archive, manifest bytes/modes, all eight offline
  installs, installer `--check`, and installed scripts' `--help` pass. It is not
  hosted `npx` discovery or behavioral verification of every installed skill.
- A new `git archive HEAD` extraction outside any repository, without `.git` or
  `benchmarks/local-runs`: Con Artist subset **11 tests, 7 errors**. Expanded full
  archive discovery: **783 tests, 116.158 seconds, 56 errors, 3 skips**. Errors
  include assuming the ignored scratch parent exists, requiring historical source
  snapshots and obtaining checkout HEAD from an archive. Test output truncation
  in the review display does not replace the native final failed summary.
- [GitHub run 35514595778](https://github.com/SoonGwan/questionable-hires/actions/runs/35514595778)
  for `21ed1a4` completed as failure with no started test steps. The check-run
  annotation attributes non-start to account payment/spending-limit settings.
  This is **not a hosted test result**. Billing/settings were not changed. The
  owner must resolve that external condition before hosted matrix evidence exists.

## Repair completed in this checkpoint

Twenty test modules now create their owned temporary directory beneath the
tracked `benchmarks` parent instead of requiring a pre-existing ignored
`benchmarks/local-runs`. These 36 replacements change test scratch placement only;
no checks, assertions, skill resources, measured cases/results or model schedules
were removed or weakened.

`test_native_archive_scratch.py` copies the exact selected tests, assets and
fixtures into a fresh directory with neither Git metadata nor local-runs. Its
12 nested native tests cover FIFO/directory refusal, asyncio ownership and
failure/cleanup behavior, retained application assertions, and live configured
consumer contracts. All execute without skips, preserve source bytes and leave
no scratch files. Initial attempts at this new sparse test omitted required
fixture dependencies; those harness failures were corrected by including them,
not by skipping checks or changing the application assertions.

After repair, changed test modules plus the new archive regression pass:
**55 tests in 13.716 seconds**. Repository validation, localized featured-chart
check and whitespace check pass. Full archive discovery has **not** been declared
repaired: Git-dependent runner/preflight/provenance checks remain to be separated
from archive-runnable behavior. The earlier 56 errors are the pre-repair count,
not a claimed current remaining count. No full-suite post-repair result is inferred
from this targeted check.

Next: retain native controls in archive mode, isolate genuine historical-source
verification with explicit availability reporting, and exercise scheduling logic
using controlled snapshot fixtures. Do not hide all benchmark tests or supply
invented historical identities. Then rerun the complete clean-source checks.

## 한국어

후속 수정(부모 `22db7c6`): Con Artist 저장소 과제의 정상·결함 대조는 보존된
원본·테스트 해시 확인 후 Git 없는 압축본에서도 실행된다. 커밋과의 출처 대조만
별도 검사로 분리했으며 압축본에서는 그 한 개만 명시적으로 건너뛴다. 변조된
보존 원본은 거부한다. 관련 case/runner 6개와 압축본 회귀 2개가 통과했다.
다른 Git 의존 검사와 전체 압축본 재검증은 여전히 남아 있다.

기존 개발 폴더는 783개가 통과했고, 독립 스킬 패키지의 오프라인 설치 검사도
통과했다. 하지만 Git 이력·로컬 임시 폴더가 없는 소스 압축본 전체 검사는
56개 오류·3개 건너뜀으로 실패했다. 두 배포 형태의 검증을 혼동하지 않는다.

테스트 20개 파일의 임시 폴더 의존성을 수정했고, 별도 압축본 환경에서 실제
검사 12개를 실행하는 회귀 검사를 추가했다. 변경 관련 55개는 통과했다. 아직
Git 이력 의존 검사 분리와 전체 압축본 재검증이 남아 있으므로 배포 완료가 아니다.

GitHub 검사는 계정 결제/지출 한도 문제로 시작되지 않았다. 설정을 변경하지
않았으며 소유자의 해결이 필요하다. 이번 수정은 검증 재현성 개선이지 모델
토큰·속도 개선 근거가 아니다.
