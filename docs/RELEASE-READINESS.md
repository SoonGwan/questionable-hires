# Release readiness / 릴리스 준비 현황

Decision date: **2026-09-29**. Version **0.2.0**, development preview.
After reviewing the remaining limitations, the owner explicitly authorized merging,
publishing and deploying this version now. The quality/cost objective remains
unmet and stays a research objective; it no longer blocks this authorized preview.

| Requirement | Current evidence / remaining work |
| --- | --- |
| Whole-team quality, tokens and time | Integration07, measured `1be35120`: tokens **+1.67%**, CLI time **−9.63%**, only **2/8** lower both. Bounded outcomes preserved; superior quality and general savings unproven. [Complete costs](../benchmarks/ALL-EIGHT-CURRENT-07-COSTS.md). |
| Independent model execution | Guest tool invocation was rejected because approval is required while policy is `never`. An authorized execution environment is still needed; publication permission does not change this runtime policy. [Exact request](../benchmarks/SOLVER-EXECUTION-ENVIRONMENT-REQUEST-01.md). |
| Native external-case preparation | Separate Python 3.7 pytest5103 gate passes, while the official 3.9 gate and other selected-case failures remain adverse. This is author preparation, not model performance. [Evidence](../benchmarks/PYTEST5103-PYTHON37-NATIVE-01.md). |
| Local validation and installation | Source `a002981c`: checkout1,543 pass; Git-free archive1,513 pass/30 history skips, zero failures. Python3.9/3.11 actual packaged installs match. [Exact source, failures and artifacts](../benchmarks/RELEASE-020-CANDIDATE-20260929.md). Older test totals remain historical. |
| Bilingual documentation and numbers | Both READMEs use integration07 and the unchanged featured pointer. Current documentation is reviewed for the candidate; historical results retain their measured revisions. [Candidate notes](RELEASE-0.2.0.md). |
| Publication | [PR #2](https://github.com/SoonGwan/questionable-hires/pull/2) and [v0.2.0](https://github.com/SoonGwan/questionable-hires/releases/tag/v0.2.0) track the authorized publication. Four draft assets already downloaded back byte-for-byte; public verification follows publication. |
| Hosted site | [Dated delivery](../benchmarks/CONTEXT-INDEX-ALLOCATION-01.md) verifies deployed `281c3cf0`. A later release needs its own exact deployed-source check. Local tests do not refresh hosted evidence. |

GitHub Actions was removed and disabled at the owner's request. Hosted CI is not
a current release gate. Local validation commands are in [the publication guide](PUBLIC-LAUNCH.md).
Earlier account billing failures remain historical and are not a reason to change
account settings or enable workflows.

Friday review boundary: there is no application database migration. Skill updates
must preserve personal edits by backing up existing installed folders; the installer
refuses overwrites. Receipt's optional argument evidence is versioned `v:3`; consumers
must follow [its contract](../skills/receipt/references/existing-fix.md), rather than
assuming old v2 fields. The static site uses retained release directories and an
atomic current-release switch; [hosting recovery](LANDING-HOSTING.md) is separate
from restoring user-modified installed skills. Review is not a restore drill.

한국어: 2026-09-29 사용자가 현재 한계를 확인한 뒤0.2.0 개발 프리뷰의
머지·게시·랜딩 배포를 지금 진행하도록 승인했습니다. 전체 품질·토큰·시간 목표는
미달이며 후속 연구 과제로 유지합니다. 독립 모델
검증에는 정상 승인 가능한 게스트 실행 환경이 필요합니다. 이번 게시 권한으로
해당 실행 정책이 자동 변경되지는 않습니다. 로컬 검사·설치·공개 배포·모델 비용은
각각 별도로 검증합니다. 후보 브랜치 push·PR #2·0.2.0 릴리스 초안과4개 파일
재다운로드 확인은 완료했습니다. 실제 게시 상태는 위 PR과 버전 릴리스에서 확인합니다.

[Previous readiness snapshot](RELEASE-READINESS-HISTORY-2026-09-29.md) preserves
all older evidence and links, including the earlier publication approval, removed
CI requirements and dated installation/resource counts.
