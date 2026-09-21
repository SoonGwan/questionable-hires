# Local release validation at ad72a3f

2026-09-22. Source `ad72a3f8dc8c2b4ce24dfa3c0aa58dca3e67b7e2`, including
Receipt captured-byte hash reuse and the optional isolated-scratch adapter.
No skill, executable or test file changed during the runs. This is compatibility
evidence, not model performance or a public-release declaration.

| Environment | Discovered | Passed | Skipped | Failed | Duration |
| --- | ---: | ---: | ---: | ---: | ---: |
| macOS checkout / Python3.11.16 |1203|1203|0|0|212.508s|
| Linux source archive / Python3.12.3 |1203|1174|29|0|88.627s|

Both exit0. Runs overlapped; elapsed times are not a speed comparison. macOS used
the existing receipt-provenance virtualenv with `-B -m unittest discover -s tests
-q`; its terminal completion summary is retained here, not a per-test transcript.
Linux used the same offline image/dependency setup as the
[04741d7 checkpoint](RELEASE-VALIDATION-04741D7.md), with the new committed source
archive mounted read-only and copied into disposable container storage. No Git
history or local-run state was present in the tested copy. No fresh dependency
installation, hosted runner or model API call is implied.

[Linux log](results/release-validation-ad72a3f/linux-suite.txt) and
[runtime identity/command/hash](results/release-validation-ad72a3f/linux-runtime.json)
are preserved. Its29 skips concern absent project-owned history/checkout;28
messages say history and one says checkout. They are not passes; the macOS
checkout exercises all1203. Native subprocess failures and synthetic scheduler
messages inside the log are test controls, not additional measured model attempts.
Repository validation and featured/localization synchronization pass too.

## Hosted CI and release limits

Main [run35625416269](https://github.com/SoonGwan/questionable-hires/actions/runs/35625416269)
at the same source has four completed failed jobs, each with no executed steps.
Python3.11 check106418468207 attributes non-start to recent payment failure or a
spending limit; it does not establish which alternative. No billing change or
retry is performed. A successful hosted version matrix remains unverified.

The repository was also checked as private, default branch main, not archived.
No visibility, tag or release was changed. Remote installation, public-artifact
review and publication approval remain separate gates in the
[readiness index](../docs/RELEASE-READINESS.md). Broad20–30%+ model improvement
is still unproven; original adverse results and featured charts remain unchanged.

한국어: 현재 소스의 macOS1203개가 모두 통과했고 Linux 압축본은1174개 통과,
이력·체크아웃 의존29개를 건너뛰었다. GitHub CI는 결제 또는 사용 한도 문제로
네 작업 모두 시작하지 못했다. 기능 호환성 검증이며 성능 우위나 공개 배포
완료를 뜻하지 않는다. 계정 설정과 저장소 공개 상태는 변경하지 않았다.
