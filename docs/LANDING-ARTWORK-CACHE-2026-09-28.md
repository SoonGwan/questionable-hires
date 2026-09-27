# Artwork delivery cache — 2026-09-28

The approved1,330,161-byte PNG is unchanged. New HTML references its full SHA-256
in the filename, so revised bytes get a new URL. The existing original image URL
remains available. Only successful fingerprinted artwork responses receive
`public, max-age=31536000, immutable`; HTML, health, legacy URLs and errors retain
`no-cache`. No Cloudflare account settings, image palette or visual layout changed.

This follows Cloudflare's documented [origin cache behavior](https://developers.cloudflare.com/cache/concepts/cache-control/)
and [cacheable file rules](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/).
It removes the requirement for repeated origin validation of this immutable file.
It does not reduce the first image payload, prove a whole-page speedup, or identify
the cause of the earlier public browser's `networkidle` timeout.

Before change, one public image request returned200,1,330,161bytes,
`cf-cache-status: REVALIDATED`, browser `max-age=14400`,1.768182s first byte and
5.306368s total. This single shared-network sample is descriptive, not a baseline
mean. Cloudflare's downstream browser TTL differs from the origin's `no-cache`;
we do not claim the old public browser always downloaded the image again.

## Local controls

[Native original/fixed evidence](../benchmarks/results/landing-artwork-cache-20260928/native.json)
uses an isolated Git-free copy with identical six origin tests. Old server:
one expected cache-header failure. New server: all six pass, including HEAD,
conditional304, legacy freshness, missing-image/error freshness and traversal
refusal. [Before](../benchmarks/results/landing-artwork-cache-20260928/before.txt)
and [after](../benchmarks/results/landing-artwork-cache-20260928/after.txt) retained.

The18 landing tests also pass: exact artwork bytes, both image references in all
three HTML routes, changed input producing a changed filename, previous experiment
and skill downloads, metadata and raster identities. No model experiment was run.

[Local browser](../benchmarks/results/landing-artwork-cache-20260928/local-browser.json):
390px, reduced motion, KO→EN→KO in one browser context. First artwork transfer
1,330,461bytes including reported overhead; next two artwork transfers0bytes.
All eight portraits retain the same decoded1536×1024 source, no horizontal
page overflow or JavaScript page error. This local cache check is separate from
public edge delivery. Hosted evidence is recorded after deployment.

한국어: 원본 그림을 바꾸지 않고 내용 해시가 붙은 주소만 장기 캐시하도록 했습니다.
로컬 브라우저의 반복 이동에서는 해당 그림 전송이0바이트였고8명 프로필을 확인했습니다.
이는 모델 토큰 절감이나 전체 페이지 속도 개선의 증거가 아니며, 앞선 공개 페이지
대기 시간 초과의 원인도 아직 확정하지 않았습니다.
