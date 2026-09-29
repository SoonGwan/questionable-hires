# Landing hosting check — 2026-09-26 (KST)

Deployed website source **`3bbcf7e193b52c4f1af3d01ab0935e74a61c60f5`**.
This is a website hosting record, not new model evidence or the skill project's
hosted test matrix. The featured comparison still belongs to its original frozen
checkpoint and resource, selected by `benchmarks/featured.json`.

- [한국어](https://hires.no-money-do-you-have-money.com/ko/)
- [English](https://hires.no-money-do-you-have-money.com/en/)
- [Served release identity](https://hires.no-money-do-you-have-money.com/_health)

The dedicated Mac origin on loopback port 4180 and the Cloudflare Tunnel are
running as `com.questionable-hires.web` / `com.questionable-hires.tunnel`.
Existing `com.moneybook.web` / `com.moneybook.tunnel` were also running after deployment.

Public HTTPS checks verified:

- Correct app identity and exact source revision, compared with the local origin.
- Static Korean/English metadata, canonical URLs and indexable production pages.
- Both 1200×630 OG PNGs, 32×32 favicon and 180×180 Apple icon match source SHA-256 hashes.
- Sitemap/robots contain the actual public origin.
- Normal headless browser navigation to both locale URLs, chart switching,
  mobile raw-table containment and language/metric preservation, with no script errors.

Local verification separately covered 13 landing/static-origin tests and
14 language/viewport layouts. The featured synchronization check and repository
catalog validator passed. The first public CLI check encountered stale local
negative DNS responses; Cloudflare DNS returned the new record and HTTPS succeeded
with DNS-over-HTTPS. The deployment verifier now uses that resolver for public
checks. A normal browser also loaded both URLs without a resolver override.

No third-party social-platform preview was posted or inspected. HTML/image inputs
are publicly verified; platform-specific caches/rendering remain a separate check.

한국어: 실제 공개 주소의 두 언어 페이지·OG 이미지·사이트맵·앱 식별자를 검증했고,
일반 브라우저에서 모바일 그래프와 언어 전환도 확인했습니다. 로컬 UI 검사,
웹사이트 호스팅 확인, 모델 성능 측정과 원격 CI 매트릭스는 서로 다른 근거입니다.

[Deployment, logs, updates and rollback](LANDING-HOSTING.md)
