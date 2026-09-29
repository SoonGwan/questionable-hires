# 0.2.0 delivery / 배포 확인 — 2026-09-29

[PR #2](https://github.com/SoonGwan/questionable-hires/pull/2) is merged.
[v0.2.0](https://github.com/SoonGwan/questionable-hires/releases/tag/v0.2.0)
is published as a development prerelease. The version tag and hosted site both
identify **`8f3e4e44c22a47d551c073fcab713a98f4380026`**. Later documentation
commits record this delivery without changing the deployed release identity.

The owner explicitly requested immediate merge, publication and deployment after
reviewing the incomplete performance objective. Integration07 remains tokens+1.67%,
CLI time−9.63%, only2/8 improve both; publication does not change those results.

The Mac origin and dedicated Cloudflare Tunnel were deployed using the existing
script. Both local and public health checks identify the release revision. Previous
release files remain available for rollback; no restore drill was performed.

Anonymous HTTPS checks passed for nine site routes: Korean/English pages, health,
sitemap, robots, two localized OG images, skill archive and checksum. Static
responses match the generated deployed files byte-for-byte. The downloaded skill
archive contains55 payload files, including52 skill resources, with matching source
bytes, manifest hashes and distribution permissions.

All four GitHub release assets also download anonymously and match their local
originals: plugin ZIP, standalone archive, SHA256SUMS and RELEASE.json. Their
original build sources remain recorded in RELEASE.json; no old measurement or
artifact identity was relabeled. GitHub's temporary untagged release tag was
replaced by v0.2.0 and the temporary tag removed.

[HTTP evidence](../benchmarks/results/release-020-candidate-20260929/public-verification.json) ·
[Earlier candidate tests and failures](../benchmarks/RELEASE-020-CANDIDATE-20260929.md).
The latter is a historical preparation checkpoint; its draft status describes the
state before this publication. Code tests at a002981c passed1,543 in checkout and
1,513 with30 history-dependent skips in a Git-free archive. Subsequent changes are
documentation only; these totals are not newly executed tests of the merge commit.

The Browser runtime reported no connected browsers. No new visual, mobile viewport
or interactive browser check was performed during delivery. HTTP checks do not
substitute for those checks or prove third-party social preview rendering.

한국어: PR #2 머지와v0.2.0 개발 프리뷰 게시를 완료했고 Mac·Cloudflare 랜딩도
같은 커밋8f3e4e44로 배포했습니다. 한영 페이지·헬스·사이트맵·robots·OG2개·스킬
다운로드·체크섬의9개 경로와 GitHub 파일4개를 비인증으로 내려받아 원본과
일치함을 확인했습니다. 스킬 리소스52개의 내용·해시·배포 권한도 일치합니다.
이후 문서 커밋은 이 결과를 기록하며 태그와 실제 배포 소스를 바꾸지 않습니다.
연결 가능한 브라우저가 없어 이번 배포에서 화면·모바일·상호작용을 새로 확인하지는
못했습니다. 전체 성능 목표와 독립 모델 검증 환경 문제는 후속 과제로 남습니다.

[한국어 랜딩](https://hires.no-money-do-you-have-money.com/ko/) ·
[English landing](https://hires.no-money-do-you-have-money.com/en/)
