# Comparison table readability — 2026-09-27

Source `277c8937`. Both existing evidence tables now use13px body text rather than
11px, with10px case identifiers rather than8px. Numeric columns align right with
tabular numerals; their column headers align accordingly. The Montage palette,
raw values, featured charts, whole-cohort arithmetic and evidence links are unchanged.

[Local browser outcomes](../benchmarks/results/landing-table-277c8937/result.json)
cover KO/EN at320,390,1440px. Both tables open, retain10 featured and8 checkpoint
rows, and remain contained without page overflow. Horizontal scrolling works;
footer values remain606,355 /507.824 /718,747 /553.853. Time chart switching passes
and no script error is observed. Computed number font13px, right alignment and
identifier font10px are recorded as observations, not assertions mirroring CSS.
The [Korean mobile table](../benchmarks/results/landing-table-277c8937/table-ko.png)
was visually inspected after scrolling to the last numeric column. Labels remain
available by scrolling left; this is not a sticky-row-header implementation.

All12 existing landing tests and featured synchronization check pass; the public
production build generates15 files. The [source identity](../benchmarks/results/landing-table-277c8937/source.json)
retains the exact stylesheet hash and the [browser control](../benchmarks/results/landing-table-277c8937/check.cjs)
is retained. These are local preview checks, not a new fourteen-layout sweep,
hosted release check, accessibility certification or model efficiency measurement.

## Hosted delivery

The dedicated Mac/Cloudflare origin now serves release `7b8a7f98`. Deployment
verified local and public health. [Subsequent public audit](../benchmarks/results/landing-table-public-7b8a7f98/public-audit.json)
matches the exact live stylesheet to the source and records the new public health
revision. The same browser control passes on ordinary public URLs in both locales
at320/390/1440px; actual number font13px/right alignment and identifier font10px
are observed in all six cases. Table totals, containment and time graph switching
remain verified. Public screenshots and exact control are retained beside the audit.
No measured value, benchmark pointer or graph data changed during deployment.

한국어: 비교 표의 본문11→13px·과제 식별자8→10px와 숫자 오른쪽 정렬을 적용했다.
한·영320·390·1440px에서 두 표의 행·합계·스크롤·페이지 넘침·시간 그래프를
확인했고 모바일 표를 직접 검토했다. 원시 수치와 그래프는 변경하지 않았다.
이 기록은 로컬 검증이며 실제 배포 확인은 별도로 남긴다.

공개 배포 후에도 같은6개 언어/너비 조합에서 글꼴 크기·정렬·합계·그래프를
확인했고, 공개 CSS가 수정 소스와 일치한다. 배포 릴리스는7b8a7f98이다.
