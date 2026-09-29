# Lossless landing artwork delivery — 2026-09-28

Source parent `bce4faad`; native artwork/browser work, not a model experiment.
The approved PNG, dimensions, palette and character crops are unchanged. A
lossless WebP derived from it reduces the first artwork body from **1,330,161
to756,050 bytes**, a574,111-byte / **43.16%** reduction. Source/output/pixel hashes
and encoder versions are in the [asset manifest](../assets/team-characters-webp.json).
This addresses the first-transfer payload left unchanged by the earlier
[artwork cache release](LANDING-ARTWORK-CACHE-2026-09-28.md).

The encoder uses Pillow11.3.0/libwebp1.5.0 with lossless/exact enabled, quality100
and method6. It verifies decoded RGBA bytes, dimensions and color profile before
writing the derivative. These options follow the [Pillow WebP documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#webp).
This PNG has no embedded color profile. Encoding is an author-only operation;
ordinary builds use the committed derivative and reject mismatched source/output
hashes. [Regeneration instructions](../assets/README.md) keep Pillow outside the
normal static build/runtime dependency set.

Both illustrations use `<picture>` with a typed WebP source and the original PNG
fallback. Each format retains a full SHA-256 URL and immutable successful-response
caching. Missing images/errors stay uncached. Image/source URLs become absolute
before in-page locale navigation so root-to-language navigation cannot change
their resolution. Original PNG/legacy URLs and social cards remain available.

## Local evidence

- [Lossless regeneration check](../benchmarks/results/landing-webp-20260928/pixel-check.txt): identical pixels and encoded output.
- [Browser checks](../benchmarks/results/landing-webp-20260928/local-browser.json):16 conditions, KO/EN ×320/390/768/1440px ×JavaScript on/off. Native image size1536×1024, no horizontal overflow/page errors. JavaScript cases exercise all8 portraits. Supported browsers request WebP without also requesting PNG.
- The same browser check verifies root→EN navigation and unsupported-source-type PNG selection. That is a format fallback, not automatic recovery from a failed WebP network request.
- Separate same-browser canvas decoding of both formats compares6,291,456 RGBA channel values with **zero differences**. A390px and1440px screenshot was visually inspected for layout/crops.
- First local transfer is756,350 bytes including browser-reported transfer overhead; subsequent KO→EN→KO page visits report0 transfer bytes for the artwork while retaining756,050 encoded bytes.
- Nineteen landing methods and [seven origin methods](../benchmarks/results/landing-webp-20260928/server-checks.txt) pass. New checks cover stale derivative rejection, source/fallback markup, WebP media type, immutable200/304 and uncached404. An initial author test used a case-sensitive `Content-Type` dictionary lookup; it raised KeyError before the assertion. Corrected the test to compare HTTP header names case-insensitively; this was not an origin response failure.

The connected in-app browser list was empty, so QA used the existing standalone
Playwright installation with installed Chrome. The [executed check](../benchmarks/results/landing-webp-20260928/ui-check.cjs)
is retained. The [pre-deployment public observation](../benchmarks/results/landing-webp-20260928/before-public-browser.json)
records the old PNG's1,330,461 first transfer and zero on the two subsequent page
visits. These first transfers are separate browser contexts; no controlled full-page
latency improvement is claimed from their network durations.

No whole-task model tokens, native skill efficiency, all-eight outcomes or featured
benchmark numbers change. The owner's complete efficiency objective remains unmet.

## Hosted release

Source **`d4916dfd`** was deployed with the existing Mac/Cloudflare release switch.
Both loopback and public health checks identify this source. The
[public HTTP check](../benchmarks/results/landing-webp-20260928/public-origin.json)
retrieved exactly756,050 WebP bytes with the expected SHA-256, `image/webp` media
type and one-year immutable cache header. That request was a Cloudflare MISS;
do not describe it as an observed edge HIT.

The complete [public browser check](../benchmarks/results/landing-webp-20260928/public-browser.json)
then passed all16 responsive/language/JS conditions, all8 JavaScript profile
selections, root locale navigation, PNG format fallback and zero-difference canvas
comparison. First artwork transfer was756,350 bytes; the next two page visits
reported0. The old/new encoded-body difference is43.16%; it is not a controlled
measurement of full-page elapsed time, and this release does not establish the
cause of an earlier unrelated hosted navigation timeout.

한국어: 승인된 그림의 픽셀·크기·팔레트를 유지하면서 WebP 전송 파일을 만들었다.
첫 그림 본문이1,330,161→756,050바이트로43.16% 줄었다. PNG 대체 표시와 장기
캐시를 유지하고, 브라우저의6,291,456개 RGBA 값 비교에서도 차이가0이다.
양언어·4개 폭·JS 켜짐/꺼짐16개 조건과8개 캐릭터, 루트 주소의 언어 전환을
확인했다. 최초 헤더 검사 코드 오류를 고친 뒤 정적19개·서버7개 검사가 통과했다.
전체 페이지 지연이나 스킬 토큰 절감으로 바꾸어 주장하지 않는다.
`d4916dfd`를 실제 공개 주소에 배포했고 같은16개 브라우저 조건·PNG 대체 표시·
픽셀 일치·재방문 전송0바이트를 확인했다. 공개 응답의 형식·캐시·실제 파일
해시도 일치한다. 확인한 HTTP 요청은Cloudflare MISS였다.
