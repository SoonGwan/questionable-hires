# Landing skill download — 2026-09-28

The installation section now offers the current source snapshot alongside the
GitHub installation command, with explicit Korean and English version wording.
The standalone packager supplies all eight skills (52 resource files), installer,
MIT license, bilingual installation guide and per-file hash/mode manifest.
There are no benchmark logs, repository history or experimental prototypes in
this archive. SHA-256 is a content identity, not a signature or performance score.

- Archive: `landing/downloads/skills.tar.gz`, 104,257 bytes.
- SHA-256: `b21309512acd79c9d42a2cf0fcb0268ce89aaaf2557d83883de9e7b0d604fc3b`.
- Ordinary skill/installer source: unchanged from `5d5f877a`.
- Packaging additionally includes [the bilingual snapshot guide](INSTALL-SNAPSHOT.md).
- Source checks: 16 landing + 4 standalone archive + 4 origin tests passed.
- Offline installation: extracted archive installs eight skills; read-only
  comparison matches every installed resource. A subsequent install refuses to
  overwrite an existing personal edit. Existing archive reproducibility and
  installed native helper behavior checks pass.
- UI: 16 combinations of KO/EN, widths 320/390/768/1440, JavaScript on/off,
  reduced motion; no document overflow or JavaScript page errors. Real browser
  download bytes match the archive. Root-route KO/EN switching keeps download
  paths correct; both 390px installation panels visually reviewed.
- Generated files/raster identities, catalog validation and featured benchmark
  synchronization checks pass. Frozen benchmark numbers remain unchanged.

These checks establish packaging and local UI behavior, not improved model cost.
The existing historical charts retain their dated measured resource IDs. No new
model experiment was run for this distribution change. Hosted checks are recorded
separately after deployment.

한국어·영어 설치 영역에 GitHub 공개 버전과 구분되는 개선본 다운로드를 추가했습니다.
압축 파일만으로 스킬 8개를 설치하고 기존 개인 수정 파일을 보존하는 동작을 확인했습니다.
반응형·언어 전환·JavaScript 없는 화면도 확인했습니다. 패키징 검증이며 토큰 감소를
입증한 실험은 아닙니다. 기존 그래프의 측정 리소스·수치는 그대로 유지합니다.

## Hosted verification and root navigation follow-up

Release `8482dbde` was deployed to the existing Cloudflare/Mac domain. Public
KO/EN pages have the expected canonical URLs and snapshot links; all three
hosted download files match local bytes. A real 390px browser download matches
`skills.tar.gz`, and KO→EN switches without overflow or page errors. The initial
Python urllib health request received HTTP 403; ordinary curl and browser checks
succeeded without changing site security configuration. This is a recorded
client discrepancy, not evidence that every client succeeds.

That UI pass exposed an existing root-navigation icon bug: after entering `/`
and switching to EN, the browser resolved the relative icon to
`/en/assets/favicon.svg`. A separate browser assertion failed on the hosted
pre-fix release. The fix resolves all icon links against the initial page URL
before language navigation; the same root→EN→KO assertion then passed locally.
Snapshot bytes and benchmark claims did not change in this follow-up.
