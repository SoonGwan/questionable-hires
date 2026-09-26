# Evidence delivery and language links — 2026-09-27

Deployed source **`0c6223d3620cc715678508deb76f1cf21f96b4aa`**.
[Completed controls and original logs](../benchmarks/results/landing-evidence-0c6223d3/summary.json).
Public HTTPS health identifies this release. The prior release remains available
for rollback through the existing Mac deployment mechanism.

The public landing's integration05 cost link pointed at a report absent from the
remote main branch (`995c67f7` when inspected). The landing now hosts all eight
paired task costs and actual totals directly. The table and signed summary inputs
come from the frozen16-row comparison; missing, duplicate or inconsistent rows
are rejected. Cost analysis, scoped original review and original comparison JSON
are downloadable from the same site with identical source bytes. The featured
benchmark, its graphs and historical measurements are unchanged. This does not
publish new repository history or adopt an optimization.

The root page also reproduced a language-link failure: after its URL changed to
`/ko/`, the EN link resolved as `/ko/en/`. Links now resolve from the application
root. Actual modifier-click navigation opens the expected English page in a new
tab. The new comparison table stays open across language changes, and mobile
users receive a horizontal-scroll hint to reach both conditions.

Checkout16 landing/server tests pass; a fresh Git-free archive of the deployed
source also passes16 with no skips in2.105s. Existing browser controls pass14
bilingual layouts, selection, copy recovery, keyboard and reduced motion on the
preview. New controls pass14 open-table layouts on preview and public HTTPS,
eight paired tasks, table state after language changes, actual new-tab navigation
and three downloads whose bytes match the original sources. No page errors.
Browser runtime was unavailable earlier; controls use standalone Playwright with
installed Google Chrome. These are website checks, not model performance scores
or exhaustive browser/accessibility coverage.

The unchanged skill/installer resources retain their dated `ba2713d5` validation.
Approved CI removal remains in force; historical hosted failures are not current
release gates. All-eight quality/lower-token/faster-time improvement is still
unproven. Current integration05 costs remain adverse and visible.

한국어: 보고서가 없는 GitHub 링크를 랜딩 자체의 비교 표·동일 원본 다운로드로
대체했다. 루트에서 언어를 바꾼 후 새 탭을 열 때 잘못된 경로로 가는 문제도
실제 브라우저에서 수정 전 재현·수정 후 검증했다. 공개 배포와14개 펼친 표 화면,
자료3개, 아카이브16개 검사가 통과했다. 스킬의 토큰·시간 절감 성과는 아니다.
