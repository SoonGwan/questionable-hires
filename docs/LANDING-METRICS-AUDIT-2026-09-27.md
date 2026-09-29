# Landing metrics audit — 2026-09-27

Source checkpoint `efe8bc23`; current source checks and public delivery observations,
zero new model experiments. Small documentation correction distinguishes historical
September26 nine-test verification from current 12 landing + 4 server tests, and
labels integration05 elapsed change as a ratio of cohort sums. Measurements and
graphs are unchanged.

The fixed integration05 record (`75183f2f`, eight tasks per condition) recomputes:

| Whole-cohort usage | Without skill | With skill |
| --- | ---: | ---: |
| Input tokens |592,509|705,328|
| Output tokens |13,846|13,419|
| Input + output tokens |606,355|718,747|
| Cached input, already included above |530,432|613,632|
| Model responses |38|39|
| Sum of CLI elapsed seconds |507.824|553.853|

Tokens increase18.54%, summed elapsed increases9.06%. These adverse values are
preserved; no billing conversion or new optimization claim. Featured graph values
are equal-weight per-task ratios from the separate frozen featured resource,
not these aggregate changes. Both datasets retain their dates and limitations.

Local checks: all16 existing tests pass, featured synchronization check passes,
all15 generated preview files match. [Current public audit](../benchmarks/results/landing-current-audit-efe8bc23/audit.json)
checks live health against deployment revision `da01b392`, and seven ordinary URLs
against bytes in that release's served `site` directory. No cache-busting URL or
new deployment. The exact release ID and file hashes are in the audit record.

[Reused browser control](../benchmarks/results/landing-current-audit-efe8bc23/public-control.cjs)
changes screenshot destinations only. Actual browser checks pass for both locales
at1440px, chart switching, canonical/OG URL/index metadata, then390px raw-table
containment/ten featured rows and KO switch preserving the time metric. No page
errors. [Korean mobile capture](../benchmarks/results/landing-current-audit-efe8bc23/public-mobile-ko.png)
was visually inspected; both desktop captures are retained. This is not a new
fourteen-layout sweep, social-platform crawl, new OG raster download or model
performance measurement. The original [hosted delivery record](LANDING-UNITS-2026-09-27.md)
remains separate.

Two author setup failures are explicitly recorded: the first NODE_PATH lacked
Playwright before browser launch; the existing installed module path was used
without installation. The first byte check assumed files under release root and
failed FileNotFoundError; deployment source identifies release/site as the actual
served root. New ordinary reads verify that root. Error summaries, not complete
first stderr or incomplete retrieved bytes, are retained. No page data or browser
assertion was relaxed to obtain a pass.

한국어: 문서의 과거 검사 수와 현재16개 검사를 구분하고, 전체 시간 합계 증가율을
과제별 비율 평균과 혼동하지 않게 수정했다. 원시 수치·대표 그래프는 그대로다.
현재 공개 health·7개 파일의 배포 일치와 한·영 그래프·390px 표·언어 전환을
확인했다. 검사 환경/로컬 경로 오류도 보존하며 새 성능 측정으로 취급하지 않는다.
