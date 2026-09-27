# Hosted task-unit clarification — 2026-09-27

The public Korean and English landing pages now serve release
`da01b392be37ecc3a2ac93b112496cc9b7209535`, built at `20260927T084200Z`:
https://hires.no-money-do-you-have-money.com/ko/ and `/en/`.
This deploy delivers the already committed `ab4e1b7c` labels distinguishing mean
token/time changes per task from whole-task cumulative usage. It does not change
the featured benchmark, underlying measurements, or candidate adoption decisions.

[Retained hosted evidence](../benchmarks/results/landing-units-da01b392/release-check.json)
identifies the release and records byte-for-byte agreement between seven ordinary
public URLs and the deployed files, including both localized HTML pages, runtime
content, JS, CSS, sitemap and robots. No cache-busting URL was used. Both localized
mean labels were asserted. The server supplies `Cache-Control: no-cache`.

The existing landing tests passed (16 tests), featured synchronization check passed,
and the static production build generated 15 files. Reused standalone Playwright
controls with installed Google Chrome verified both public languages, canonical
and OG metadata, successful 1200×630 PNG downloads, chart switching, mobile raw
table display and preservation of metric selection across language switching.
The token breakdown control verified the original input, output, total and cached
counts plus 38/39 model response counts at 390px, without page overflow or script
errors. The Korean mobile breakdown screenshot was visually inspected locally.

The original public control failed because its global `tbody tr` selector counted
18 rows after the eight-row usage table was added. Its original failure remains in
`public.log`; `public-control.cjs` scopes the assertion to `.raw-details tbody tr`,
whose ten frozen benchmark rows pass. This changes the control, not the page data.
The metadata and token controls are reused unchanged from the earlier retained
landing evidence; their new outputs and the scoped public output are retained here.

These are hosted delivery checks, not new model performance measurements or a new
14-layout responsive sweep. The eight-role integration05 result remains adverse:
606,355 → 718,747 total input/output tokens (+18.54%), with mean elapsed time also
increased (+9.06%). Cached input is a subset of input and must not be added again.
No optimization success or benefit across all eight roles is claimed.

한국어: 공개 한·영 랜딩에 과제별 평균 토큰·시간 변화라는 단위 표기를
반영했다. 원시 토큰 합계와 캐시 포함 관계, 그래프·언어 전환·모바일 표 및
OG 이미지를 실제 공개 주소에서 확인했다. 기존 검사 실패와 범위 수정도
보존했다. 수치나 featured 포인터는 바꾸지 않았으며, 8개 역할 전체 비교의
토큰 증가 18.54%·시간 증가 9.06%는 그대로다. 배포 검증은 성능 개선 증거가
아니며 모든 역할의 비용과 시간을 줄인다는 목표는 아직 달성하지 못했다.
