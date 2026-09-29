# Production landing browser checks — 2026-09-27

Tested deployed source `ba2713d5355ebed3d7a193e7d16ac0cf684c143f`, at
https://hires.no-money-do-you-have-money.com/ko/ and `/en/`.
[Retained evidence and control sources](../benchmarks/results/landing-browser-ba2713d5/summary.json).
The public HTTPS health response identifies this release. These checks did not
redeploy it. Local-origin application JS/CSS match tracked source; generated
content matches apart from the expected production SITE configuration.

The existing responsive control passes14 layouts: Korean and English at320,
390,760,768,1024,1440 and1920px. No horizontal page overflow or tested heading
clipping, missing translation keys or page errors were observed. It checks all
eight selections across language switches, preferences, explicit language URLs,
clipboard success and failure, blocked storage, keyboard focus and reduced
motion, including a live preference change.

The existing interaction control also passes against both the production local
origin and the ordinary public HTTPS browser route. Checks include production
OG URL/indexability, metric switching, mobile raw-table expansion and preserving
the selected metric and details state when switching languages. Mobile origin
screenshot was visually reviewed. Captures remain local; their digests, original
logs and the executed control sources are retained in the linked evidence.
An additional public metadata check verifies both canonical URLs, locale tags,
Twitter image parity and successful OG image downloads with actual PNG dimensions
of1200×630.

The Browser runtime reported no available browsers after documented recovery;
these controls used standalone Playwright with installed Google Chrome.
Earlier public-browser navigation timeouts remain historical; this is a new
successful observation on the explicitly identified release. It is not exhaustive
accessibility, device/browser coverage, model-quality or efficiency evidence.
The featured benchmark and integration05 adverse cost result are unchanged.

한국어: 배포 버전`ba2713d5`의 한·영14개 화면 크기와 실제 공개 브라우저
접속을 확인했다. 언어 전환·복사 실패 복구·그래프 선택·모바일 원본 표가
통과했고 스크립트 오류는 없었다. 이전 접속 실패를 소급해서 바꾸지 않으며,
이 검증은 웹 동작 확인이지 스킬의 토큰·시간 절감 근거가 아니다.
