# Release check — 2026-09-20, source `21ed1a4`

**Not a release approval or performance benchmark.** The installed skill archive
and repository source archive are different deliverables; do not generalize one
passing check to the other.

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
