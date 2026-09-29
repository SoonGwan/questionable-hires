# Language transition feedback — 2026-09-28

Parent `63187078`. A delayed experiment translation kept the old page visible
without any indication that a language click was pending. The navigation now shows
a small localized status, and marks main content busy until the current request
commits. Choosing the current language clears pending feedback immediately. Existing
request ownership prevents late success/failure from superseded requests changing
the page. No spinner, dependency or extra network request is introduced.

[Actual Chrome controls](../tests/browser/landing_language_pending.cjs) hold the
translation response while clicking the real navigation at320px in both languages.
Each locale covers success, cancellation followed by old success or failure,
returning to the pending target, and HTTP503 fallback to its complete locale page.
They assert visible localized/live feedback, viewport containment, busy state,
final locale/URL, and selection/metric/expanded-record preservation for inline
changes. Full-page failure fallback retains its existing state-reset behavior.

[Before](../benchmarks/results/landing-language-pending01/before.txt):all10 cases
fail at the first missing busy-state assertion, so later checks were not reached.
[After](../benchmarks/results/landing-language-pending01/after.txt):same10 pass.
[Existing clipboard cases](../benchmarks/results/landing-language-pending01/copy.txt):12 pass.
[Landing/server checks](../benchmarks/results/landing-language-pending01/native.txt):27 pass.
The build remains151 files and skill download bytes are unchanged. Individual
browser actions/navigation and request observation have time bounds. Translation
responses are controlled; no performance or real-network-latency claim follows.
No in-app browser was available; these use the installed standalone Chrome.

Visual inspection of a320px English pending state exposed a pre-existing title/
tagline collision, separate from feedback. Its responsive repair is tracked next;
these pending-state checks do not establish collision-free text across the page.
Frozen featured and integration07 measurements remain unchanged. No model calls,
new model-token/time result or all-eight goal completion is claimed.

한국어: 느린 언어 전환 중 작은 진행 문구와 접근성 상태를 표시한다. 취소 후
이전 응답·재선택·실패 시 전체 페이지 이동을 한영10개 실제 브라우저 사례로
검증했고 기존 복사12개·랜딩/서버27개 검사도 통과했다. 토큰 절감 근거는 아니다.

## Hosted verification

Release **`874944965c82e6a8fb53dedaaebd32c7af1d1bd7`** is live on
[한국어](https://hires.no-money-do-you-have-money.com/ko/) and
[English](https://hires.no-money-do-you-have-money.com/en/).
[Same10 hosted browser cases](../benchmarks/results/landing-language-pending01/public-browser.txt)
pass in their own command, exit0. Translation responses remain controlled; full
locale pages, assets and fallback navigation come from public HTTPS.
[Eight HTTP identity checks](../benchmarks/results/landing-language-pending01/public.json)
match release revision, locale pages, JavaScript, stylesheet, copy data and unchanged
archive/checksum; all52 skill resource bytes/modes still match source.
The owned preview server stopped; browser contexts were closed. No GitHub push.

한국어: 공개 배포87494496에서도 언어 전환10개 검사가 통과했다. 공개8개 경로·
다운로드52개 자원 일치를 확인했다. 실제 번역 응답 지연은 통제한 검사이며
모델 비용 측정은 추가하지 않았다.
