# Landing resolved-file boundary — 2026-09-28

The origin checked requested paths against the release directory, but the implicit
`index.html` and health manifest were selected afterward without the same boundary
check. Local GET requests could therefore return an owned outside-file canary
through a directory index symlink, or report an outside release manifest as healthy.
The inspected deployed site tree has no symlinks; this reproduction does
not establish public disclosure or a remotely writable deployment directory.

The fix checks each selected index/manifest's resolved location before serving it.
Outside indexes return404, including slashless directory requests; an outside
health manifest returns503. In-release links remain supported. Ordinary files,
conditional image responses, security/cache headers and release switching retain
their existing behavior. This is a stable-file path boundary, not a filesystem
sandbox or protection against concurrent privileged changes between checks/reads.

[Native evidence](../benchmarks/results/landing-index-boundary01/):

- Before source `d08436c2`:10 methods,8 intended failures. Root/nested GETs contain
  the outside canary, HEAD returns200, slashless paths redirect301, and health
  returns the outside identity instead of503.
- The identical10 methods pass after the production edit.
- An additional positive control preserves contained index/manifest links and
  the ordinary slash redirect. It passes against the old server in a Git-free
  copy; all11 origin methods pass against the fix on Python3.9.6.
- All30 landing/origin methods pass on Python3.11.6. Static151-file build check,
  repository validator, featured synchronization and whitespace checks pass.

Raw logs remain in owned local storage; published reading copies replace repository
and isolated-copy paths and retain both hashes. No new skill or model experiment,
benchmark metric, image, language copy or installation package changes. Pre-release
archive SHA256 remains
`59d6385f9e1a9f77ff67382ef2bfd1e84e0b39a3751c543422d1e555f050a215`.
Hosted verification is recorded separately after deployment.

한국어: 요청 경로 검사 뒤 선택되는 index.html과 상태 파일에도 실제 위치 검사를
추가했다. 배포 폴더 밖 파일을 가리키는 링크는 로컬에서 내용 반환으로 재현됐고,
수정 후404/503으로 차단된다. 기존 공개 배포 파일에는 이런 링크가 없었으므로
실제 공개 유출을 주장하지 않는다. 같은10개 검사와 추가 정상 링크 대조군,
양언어 랜딩 포함30개 검사를 통과했다. 스킬 토큰 절감 근거는 아니다.

## Loop compatibility correction and first hosted check

Source7d23ef44 deployed successfully, with eight public HTTPS routes matching the
release bytes and health identity. An additional control then finds a regression
in its newly added resolve calls: on Python3.9/3.11, self-referential final links
raise RuntimeError. Two native requests lose their HTTP response. The same control
passes against originald08436c2, so this is a new regression, not a pre-existing
server defect. Retain the two original errors. Catch RuntimeError at the existing
path boundaries so final index/manifest loops again return404/503.

All31 landing/origin methods pass after that correction, and all12 origin methods
pass in the Git-free Python3.9.6 copy. The extra compatible-link control also
passed against original source. No model calls or resource-efficiency claim.

The first hosted inventory check incorrectly equated the builder's reported151
outputs with the full served tree and stopped before HTTP requests. Its recorded
actual inventories contain157 static files in both releases, with zero changed
bytes. Removing that mistaken count assumption allows the byte-identity check;
the source and served tree are not altered to satisfy it. Preserve the original
precheck error and the completed7d23ef44 hosted record. A follow-up deployment
will verify the loop correction separately.
