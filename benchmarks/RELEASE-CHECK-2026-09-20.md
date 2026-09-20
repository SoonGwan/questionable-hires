# Release check — 2026-09-20, source `21ed1a4`

**Not a release approval or performance benchmark.** The installed skill archive
and repository source archive are different deliverables; do not generalize one
passing check to the other.

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

기존 개발 폴더는 783개가 통과했고, 독립 스킬 패키지의 오프라인 설치 검사도
통과했다. 하지만 Git 이력·로컬 임시 폴더가 없는 소스 압축본 전체 검사는
56개 오류·3개 건너뜀으로 실패했다. 두 배포 형태의 검증을 혼동하지 않는다.

테스트 20개 파일의 임시 폴더 의존성을 수정했고, 별도 압축본 환경에서 실제
검사 12개를 실행하는 회귀 검사를 추가했다. 변경 관련 55개는 통과했다. 아직
Git 이력 의존 검사 분리와 전체 압축본 재검증이 남아 있으므로 배포 완료가 아니다.

GitHub 검사는 계정 결제/지출 한도 문제로 시작되지 않았다. 설정을 변경하지
않았으며 소유자의 해결이 필요하다. 이번 수정은 검증 재현성 개선이지 모델
토큰·속도 개선 근거가 아니다.
