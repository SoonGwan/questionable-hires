# Empty native unittest status: Python 3.12 correction

2026-09-21, parent `e86720f`. No model-performance measurement.

The complete offline Linux arm64 source-archive suite at `e86720f` discovered
1,112 tests: 1,085 passed, 26 skipped and **one failed** in 77.847s (exit 1).
[Original verbose log](results/release-validation-e86720f/linux-suite.txt) and
[runtime identity](results/release-validation-e86720f/linux-runtime.json) retain
that failure. The immutable existing image ran with networking disabled, using
read-only source/dependency mounts copied into its disposable filesystem. No
dependencies were downloaded or account settings changed. Python 3.12.3,
pytest 8.3.4 and PyYAML 6.0.3 were used. Repository and featured-sync validation
passed before the full suite. Historical-resource skips are not passing checks.

## Cause and scoped fix

`test_empty_skipped_and_help_are_not_passing_baselines` expected audit check 5
(no coverage) but received 7 (contradictory/incomplete execution). Native unittest
on this Python exits 5 for zero discovered tests while its empty result reports
`wasSuccessful() == True`. The recent shutdown-consistency check incorrectly
treated that combination as a shutdown contradiction. Both classifications stop
the audit as incomplete; this was an inaccurate diagnostic, not an accepted
empty test suite or fabricated regression detection.

Accept native 0 with a successful all-skipped/empty suite, or native 5 with a
successful **zero-test** suite, as check 5. Retain native exit, full output and
suite observation. Nonempty all-skipped exit 5 and empty/all-skipped exit 1
remain contradictions (check 7). Ordinary passing/failing suites, shutdown
contradictions, timeouts and missing observations retain their existing handling.
No extra processes, guide reads or model instructions are added.

A new actual-process control exercises the native-5 empty-result combination
on older interpreters too, plus three distinct shutdown contradictions. Each
asserts incomplete status, no next phase, unchanged source and owned-copy cleanup.
It uses a controlled shutdown handler, not a claim about real incident frequency.

- macOS Python 3.9.6 module-invocation suite: 17 passed, 3.111s.
- macOS Python 3.11.16 complete audit suite: 112 passed, 16.869s.
- Skill/repository validation, evidence pattern scan, featured sync and diff
  whitespace checks pass. Pattern scanning is not a security certificate.
- Corrected full Linux archive validation remains pending at this checkpoint;
  the original failing source/log is not relabeled.

## Hosted release gate remains separate

Read-only inspection of [run35594440490](https://github.com/SoonGwan/questionable-hires/actions/runs/35594440490)
at `e86720f` found all four jobs terminal with empty step lists. Check106315930370
reports execution prevented by failed account payments or spending limits.
This is not an observed hosted test failure, nor is offline testing a hosted pass.
No billing, publication or workflow bypass was performed.

한국어: 최신 배포 압축본의 Linux 전체 검사에서 1개 실패를 실제로 발견했다.
Python 3.12의 테스트 0개 종료 코드를 실행 모순으로 잘못 분류한 문제다.
검증 성공으로 오인한 것은 아니며, 두 경우 모두 불완전으로 중단했지만 진단을
정확히 수정했다. 기존 실패 로그를 보존했고 수정 후 macOS 감사 테스트112개가
통과했다. Linux 전체 재검증은 아직 남아 있으며 모델 성능 향상 수치는 아니다.
