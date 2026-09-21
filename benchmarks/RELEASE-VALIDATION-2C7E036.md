# Local release validation at 2c7e036

2026-09-22; source `2c7e0362e23fe9f4dbe08a427626681ca6a3f13d`.
Includes Receipt multiple-before comparison, the six-cell fixture/scheduler,
privacy export updates and Necromancer UTF-8 signature compatibility.
No skill, executable or test files changed while the suites were running.

| Environment | Discovered | Passed | Skipped | Failed | Duration |
| --- | ---: | ---: | ---: | ---: | ---: |
| macOS checkout / Python3.11.16 |1225|1225|0|0|217.166s|
| Linux source archive / Python3.12.3 |1225|1195|30|0|89.619s|

Both exit0. Suites overlapped; durations are not comparative performance evidence.
macOS used the existing receipt-provenance interpreter and `-B -m unittest
discover -s tests -q`; its terminal completion summary is retained here, not a
per-test transcript. Linux used the existing offline image/dependencies, a
read-only committed source archive copied to disposable container storage, no
network, no project Git history and no local-run artifacts in the tested copy.
No dependency download or model API call was made for these regression checks.

[Linux transcript](results/release-validation-2c7e036/linux-suite.txt) and
[runtime identity, command and log hash](results/release-validation-2c7e036/linux-runtime.json)
are retained. The30 skips concern absent project-owned history/checkout,
including the new pinned Receipt versions resource check. They are not passes;
the macOS checkout executes all1225. Synthetic scheduler output and deliberate
subprocess failures inside the tests are controls, not new model attempts.

Repository validation, localized featured/chart synchronization and diff
whitespace checks pass. Export path/credential pattern scan has zero findings,
not a complete secret-free certification. The
[previous checkpoint](RELEASE-VALIDATION-AD72A3F.md) is preserved unchanged.

## Hosted and release boundaries

Main [run35630364251](https://github.com/SoonGwan/questionable-hires/actions/runs/35630364251)
at this exact source has four terminal failed jobs with no executed steps.
Python3.11 check106434809544 says the job did not start because recent payments
failed or a spending limit must be increased. Which alternative applies remains
unknown. No billing change, hosted retry, visibility change, tag or release was
made. A successful hosted Python3.9/3.11/3.12 and archive matrix remains missing.

This is local compatibility evidence, not model efficiency, current remote
installation verification, completed public artifact review or publication
approval. The [Receipt versions experiment](RECEIPT-VERSIONS-01-REVIEW.md) remains
mixed: summed tokens+0.31%,time−13.77% versus baseline. Broad20–30%+ gains are not
established; featured graphs remain tied to their original evidence.

한국어: 현재 커밋의 macOS1225개가 전부 통과했다. Linux 소스 압축본은1195개
통과·이력/체크아웃 의존30개 건너뜀·실패0개다. GitHub CI는 결제 또는 사용
한도 문제로 시작하지 못했다. 로컬 호환성 검증이며 성능 우위나 공개 배포
완료를 뜻하지 않는다. 사용자 계정 설정과 저장소 공개 상태는 변경하지 않았다.
