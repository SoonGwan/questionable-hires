# Release readiness — development preview

Decision index,2026-09-22. **Not a completed public release or a claim of broad
performance superiority.** Each check applies only to its stated source revision.

## Required evidence

| Gate | Evidence / remaining work |
| --- | --- |
| Current local compatibility | [Combined checkpoint](../benchmarks/RELEASE-VALIDATION-2C7E036.md), `2c7e036`: macOS/Python3.11 checkout1,225 passes; Linux/Python3.12 archive1,195 passes/30 historical skips, zero failures. Includes Receipt multiple-before and Necromancer BOM support. Local checks do not replace the hosted matrix. Prior [ad72a3f evidence](../benchmarks/RELEASE-VALIDATION-AD72A3F.md) is retained. |
| Hosted Python matrix and archive | [Run35630364251](https://github.com/SoonGwan/questionable-hires/actions/runs/35630364251) at `2c7e036`: all four jobs failed before any steps. The Python3.11 annotation cites failed recent payments or a spending limit. The intended release commit still needs successful hosted execution. |
| Installable resources | [Local skills CLI checkpoint03](../benchmarks/SKILLS-CLI-INSTALL-03.md), `8114957`: eight hires/51 resources, nine Python entrypoints and selected installed behavior pass. This predates the special-input fix; not remote authenticated installation or host registration. |
| Whole-task performance | [Candidate evidence](../benchmarks/CURRENT-CANDIDATE-STATUS.md): broad20–30%+ improvement remains unproven. The all-eight comparison costs more tokens; configuration/packaging findings are adverse or mixed. Do not promote favorable pairs alone. |
| Model selection and realistic use | [Natural boundary screen02](../benchmarks/ROUTING-BOUNDARY-02-REVIEW.md), `ba477ae`: three ordinary requests stay scoped, with no observed skill-body reads. This is not all-eight positive recall, a population false-positive rate, generalization or browser QA. Historical checks remain below. |
| Public artifact review | [Bounded review01](../benchmarks/PUBLIC-HISTORY-REVIEW-01.md), `4174c18`:1,368 reachable commits/11,104 blobs checked with existing patterns. One key-header test marker, zero bearer-pattern matches,284 path matches require disposition. Future scratch-path exports repaired; historical cleanup and broader review remain open. Not a secrets-free certification. |
| Remote installation | [Authenticated checkpoint01](../benchmarks/REMOTE-INSTALL-01.md), `5e6beab`: GitHub helper and actual npx remote clone install all8/51 resources into fresh temporary destinations; selected installed behaviors pass. Existing Git credentials and cached CLI package used. Fresh npm download, anonymous public access and host discovery remain unverified. |
| Publication authority | Obtain owner approval before changing visibility or publishing a release. No billing, visibility or publication changes are made by local validation. |

[Installed-capability checkpoint](STANDALONE-ARCHIVE.md#installed-recent-capability-checkpoint--2026-09-22-resources-11d9a36)
at resource`11d9a36` additionally exercises installed BOM excerpts and actual
three-version native Receipt comparison after offline packaging/extraction.
Python3.9/3.11 and fresh-source-archive controls pass; this does not refresh the
older remote `npx` measurement or substitute for hosted CI.

The [documented installation routes](INSTALL.md) remain available to authorized
users. [Standalone archives](STANDALONE-ARCHIVE.md) provide an optional smaller
handoff; they do not change the `npx` clone path or imply a published package.

## Interpretation and maintenance

[Path derivative set01](../benchmarks/results/public-path-derivatives-01/README.md)
provides labeled reading copies of eight identified author-path/account artifacts.
Their original hashes and non-string values are retained, but originals remain
in the current tree/history. Do not mistake derivative availability for safe
public-clone disposition; no history rewrite or visibility change is authorized.
[Earlier-inventory classification](../benchmarks/PUBLIC-PATH-CLASSIFICATION-01.md)
covers all284 path-shaped object-lines, distinguishing real owner/account paths
from temporary shapes and retained test/documentation data. This does not replace
owner disposition or a current-source public review.

Preserve failure/skipped records and resource revisions. Skipped historical-source
checks in an archive are unavailable coverage, not passes; the checkout suite
must still exercise them. Local container tests are not hosted CI or a fresh
dependency install. Timings from overlapping regression suites are not a speed
comparison. Synthetic scheduler logs are unit-test controls, not model runs.

Keep `benchmarks/featured.json` tied to reviewed model evidence and synchronize
both README languages/charts through the existing script when that evidence
changes. Never update a plotted number just because a helper test improved.

한국어: 공개 배포 완료나 전체 성능 우위를 선언할 단계는 아니다. 로컬 호환성,
원격 CI, 실제 설치, 모델 성능, 공개 파일 검토와 게시 승인은 별도 조건이다.
과거 성공·실패 결과를 현재 결과로 바꾸지 않으며, 계정 결제·저장소 공개 설정은
사용자 승인 없이 변경하지 않는다. 전체 성능 목표와 대표 그래프는 기존 실증을 따른다.

## Preserved evidence

The [complete pre-reorganization readiness history](RELEASE-READINESS-HISTORY-2026-09-21.md)
retains all prior prose, failures, tables and links from `9a84635`, including
earlier Linux startup failures and their repairs. The same-directory location
preserves relative links. Historical references to private visibility, missing
tags or unavailable runtimes are dated observations, not fresh state checks.
