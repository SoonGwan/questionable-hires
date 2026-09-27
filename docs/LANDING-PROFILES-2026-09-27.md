# Profiles and static delivery — 2026-09-27

Source checkpoint `9d1e498f`; hosted functional release `916b00f5`.
Measured resource: https://hires.no-money-do-you-have-money.com/ (KO/EN).
Author browser verification only; no new model or skill performance result.

[Actual browser observations](../benchmarks/results/landing-profiles-9d1e498f/browser.json)
cover all eight profile buttons in each language at 390 × 844 pixels. Each selection
has exactly one pressed button, populated description and the matching example URL.
The final profile selection persists across language switching. Reduced-motion
contexts have no active portrait animation; both contexts report no page errors.
This does not assert animated-mode behavior or profile preservation for every
possible input sequence.

Fresh JavaScript-disabled contexts provide localized canonical/OG URLs, ten
featured rows, eight cohort rows and both token/time graphs. Profile selection
requires JavaScript; this check concerns static evidence and metadata delivery.
All eight observed [GitHub example URLs](../benchmarks/results/landing-profiles-9d1e498f/links.json)
respond HTTP 200. This does not audit the semantic contents of those examples.

The [same executed control](../benchmarks/results/landing-profiles-9d1e498f/check.cjs)
was first deliberately given an expected roster count of nine. Its
[failure](../benchmarks/results/landing-profiles-9d1e498f/control-failure.txt)
reports actual eight versus expected nine; the normal eight-count run
[passes](../benchmarks/results/landing-profiles-9d1e498f/pass.txt).
No generated asset, benchmark value or release changed.

한국어: 공개 한·영 페이지에서 직원8명 모두의 선택 상태·설명·예시 링크를
확인했다. 마지막 선택은 언어 전환 후 유지되고, 동작 줄이기 설정에서는
초상화 애니메이션이 실행되지 않는다. JavaScript를 끈 두 페이지에서도
언어별 canonical·OG, 대표10개/현재8개 기록과 두 그래프를 제공한다.
직원별 예시 링크8개는 모두200이다. 모델 측정·성능 개선의 증거가 아니다.
