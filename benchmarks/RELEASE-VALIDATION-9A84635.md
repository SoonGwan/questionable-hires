# Combined release regression — 2026-09-21

Measured executable/test/skill source `9a84635c601f218e339e1254429d1704f44cbe98`.
No new model sessions, workflow reruns, dependency downloads, billing changes or
publication actions. This is compatibility evidence, not a performance experiment.

## Local checks

| Environment | Discovery | Passed | Skipped | Failures | Native suite duration | Exit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| macOS checkout / Python3.11.16 |1,155|1,155|0|0|207.867s|0|
| Linux arm64 source archive / Python3.12.3 |1,155|1,127|28|0|86.977s|0|

Both run `python -B -m unittest discover -s tests -v`. The full
[macOS log](results/release-validation-9a84635/macos-suite.txt) and
[Linux log](results/release-validation-9a84635/linux-suite.txt) retain per-test
outcomes. The28 archive skips explicitly require absent project-owned historical
resources; they are not passes. The checkout executes those controls.
Synthetic scheduler output in the logs does not represent model execution.

The checkout was clean at launch. While it ran, only release-readiness documentation
was reorganized and validation artifacts collected; runtime, tests and installed
skills were unchanged. The original readiness document is preserved byte-for-byte
after its new four-line historical header, verified against `git show 9a84635`.
Repository validation and localized-featured synchronization pass afterward.

Linux uses an unmodified `git archive` with neither `.git` nor ignored local-run
artifacts. The existing offline validation launcher, pinned image and read-only
dependency mounts were reused. [Runtime record](results/release-validation-9a84635/linux-runtime.json)
contains image identity, exact command, process timestamps, exit and log hash.
Python3.12.3, pytest8.3.4, PyYAML6.0.3, Node24.20.0 and ripgrep15.2.0 report their
versions. Networking is disabled; installed dependencies are reused, not a fresh
dependency-resolution test. Source is copied into container-owned `/work` before
running unchanged validators and tests. Conventional startup behavior is retained.

These suites overlap on the same host. Neither duration is a speed comparison or
model-cost metric. Current Linux3.9/3.11 hosted execution is not established by
this pair. No test was retried to obtain a favorable outcome.

## Hosted gate

[Run35604299489](https://github.com/SoonGwan/questionable-hires/actions/runs/35604299489)
at the same revision has four terminal failures, all with empty step lists.
[Job records](results/release-validation-9a84635/hosted-jobs.json) and
[Python3.11 annotations](results/release-validation-9a84635/hosted-annotations.json)
retain the read-only check. The annotation says recent payments failed **or** the
spending limit needs increasing; it does not identify which account setting.
No code test executed in those jobs. Local success is not hosted-CI success.

## Decision

Recent cache, cancellation, hunk-selection and special-input fixes now have a
combined local regression checkpoint. The broad20–30%+ model-efficiency target,
fresh remote installation and intended-release hosted matrix remain unproven.
No featured graph, model measurement or release-publication claim changes.
[Release readiness](../docs/RELEASE-READINESS.md) separates these gates and links
the complete historical record instead of calling old results current.

한국어: 작업본1,155개 통과, Linux 압축본1,127개 통과·이력 관련28개 생략·실패0개다.
검사별 로그와 원격 CI의 실행 전 실패 기록을 보존했다. 동시에 수행한 회귀 검사
시간은 성능 비교가 아니며, 전체 모델 성능 개선이나 공개 배포 완료를 뜻하지 않는다.
