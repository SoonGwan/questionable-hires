# Landing maintenance check — 2026-09-27

Source checkpoint: `c6ac548b`; public functional release: `916b00f5`.
Measured resource: https://hires.no-money-do-you-have-money.com/ (KO/EN).
This is author browser/resource verification, not a new model benchmark.

[Browser observations](../benchmarks/results/landing-final-c6ac548b/browser.json)
cover both languages at 320, 390, 760, 768, 1024, 1440 and 1920 pixels.
All 14 cases pass: eight cohort rows, exact footer totals, time graph switching,
no document overflow and no page errors. Actual ZIP downloads at 390 pixels
in each language have identical hashes, 24 members and valid CRCs;
[download records](../benchmarks/results/landing-final-c6ac548b/downloads.json).
The [executed fixture](../benchmarks/results/landing-final-c6ac548b/check.cjs)
retains an older three-width console summary; the executed width array and
observed JSON contain all seven widths. No historical observation was rewritten.

[Five template GitHub links](../benchmarks/results/landing-final-c6ac548b/links.json)
respond HTTP 200. This does not verify every skill example or report URL.
[Public OG images](../benchmarks/results/landing-final-c6ac548b/og.json) match
both local source assets byte-for-byte at 1200 × 630. No social platform crawler
or cached preview was exercised.

Current generated preview verification passes for 37 files, and featured
benchmark synchronization passes. The prior [evidence release audit](LANDING-EVIDENCE-2026-09-27.md)
records all 25 public evidence paths and 18 checks in a Git-free source archive;
those checks were not repeated in this sweep because functional source is unchanged.
This browser control does not establish every heading's visual quality or every
interaction. The separate language-scroll regression retains its before/after
proof in [the scroll report](LANDING-SCROLL-2026-09-27.md).

No model result, featured graph value or skill capability changed. The eight-skill
cohort remains 606,355 → 718,747 total input/output tokens (+18.54%) and
507.824 → 553.853 summed CLI seconds (+9.06%). Cached input is part of input,
not an additional token charge; these totals are not billed cost. Whole-task
quality, token and speed improvements remain unproven in the current status.

한국어: 공개 한·영 페이지를 7개 너비씩 총14개 조합에서 확인했다. 표의8개 행과
합계, 시간 그래프 전환, 문서 가로 넘침·페이지 오류 여부가 통과했다. 두 언어의
실제 ZIP 다운로드는24개 파일과 정상 CRC를 가지며 해시가 같다. 주요 GitHub
링크5개는200, OG 이미지2개는1200×630 원본과 일치한다. 모든 시각 요소나
소셜 플랫폼 미리보기를 검증했다는 뜻은 아니다. 모델 측정은 추가하지 않았고,
전체8개 스킬의 토큰·시간 개선은 여전히 입증되지 않았다.
