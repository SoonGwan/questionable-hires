# Local release validation at 04741d7

2026-09-21. Source `04741d7c8992222311ebee09ec5e28b9afc1039d`, including exact
probe edits, transfer-runner controls and multiline decorator preservation.
No executable/test/skill files changed during either run. This is compatibility
evidence, not a model-performance result or completed public release.

| Environment | Discovered | Passed | Skipped | Failed | Duration |
| --- | ---: | ---: | ---: | ---: | ---: |
| macOS checkout / Python3.11.16 |1179|1179|0|0|211.490s|
| Linux source archive / Python3.12.3 |1179|1150|29|0|88.391s|

Both processes exited0. Runs overlapped; durations are not speed comparisons.
macOS used the existing `receipt-provenance-venv` interpreter and
`-B -m unittest discover -s tests -q`. Its terminal completion summary is the
retained observation, not a committed per-test verbose transcript.

Linux used the existing offline runtime and read-only source/dependency mounts;
the source archive was copied to disposable container storage, without `.git`
or `benchmarks/local-runs`. No fresh network dependency installation is implied.
[Complete Linux log](results/release-validation-04741d7/linux-suite.txt) and
[runtime identity, command, exit and log hash](results/release-validation-04741d7/linux-runtime.json)
are retained. All29 skips explicitly concern unavailable project-owned Git
history; the checkout run covers these checks. Catalog/document links and
featured synchronization also pass in the archive and checkout. Synthetic
scheduler messages in the suite are test controls, not fresh model sessions.

## Hosted checks remain unavailable

The main-branch [run35610526288](https://github.com/SoonGwan/questionable-hires/actions/runs/35610526288)
at this source has four completed failed jobs with empty step lists. The
Python3.11 check106368193830 annotation attributes non-start to recent account
payment failure or a spending limit; it does not identify which alternative.
Branch run35610524826 also reached terminal failure. No billing or visibility
settings were changed and no successful hosted matrix is claimed.

The [readiness index](../docs/RELEASE-READINESS.md) retains installation, public
artifact review, remote installation and publication gates. Whole-task cost
improvement remains unproven. No model measurements or graph values changed.

한국어: 최신 소스에서 macOS 전체1179개 통과, Linux 압축본1150개 통과와
이력 관련29개 건너뛰기를 확인했다. GitHub CI는 계정 결제 또는 한도 문제로
시작하지 못했다. 기능 호환성 검사이며 모델 성능 향상이나 배포 완료가 아니다.
