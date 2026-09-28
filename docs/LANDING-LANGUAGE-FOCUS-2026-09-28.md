# Locale keyboard continuity — 2026-09-28

Parent `e2b1a28d`. When a translation response arrived after the visitor had
moved into the experiment, replacing the translated markup removed the focused
control. Browser focus fell to body. A keyboard user could lose their position
on a metric button, disclosure, scrollable table or evidence link.

The builder now gives the experiment's interactive elements stable keys shared
by both locales. Immediately before applying the current translation response,
the app captures focus within that experiment and restores its matching control
after selection, disclosure and scroll state are restored. It uses preventScroll.
Focus moved outside the experiment is untouched. No focus is remembered from the
earlier request click, and existing request ownership still rejects stale responses.
No new dependency, network request, style palette or numeric claim is introduced.

[Real Chrome regression](../tests/browser/landing_language_focus.cjs) holds the
translation response at390px, opens both disclosures and uses Tab navigation to
reach the relevant control while the old locale is still visible. Each locale
covers the elapsed button, both summaries, both scroll regions, the evidence ZIP
link and a profile button outside the replaced region. After translation, focus
must remain on that semantic control. Space/Shift+Tab also verify continued native
disclosure/metric operation. Browser contexts close after every case.

The [initial before run](../benchmarks/results/landing-language-focus01/before.txt)
finds12 actual body-focus losses; its two outside-profile controls additionally
fail an unrelated test setup assumption because elapsed was not selected there.
Correcting that selection before mutation yields the definitive
[before control](../benchmarks/results/landing-language-focus01/before-corrected.txt):
**12 focus failures,2 outside-control passes**. The same corrected test after the
fix gives [14 passes](../benchmarks/results/landing-language-focus01/after.txt).
Original failed-focus cases do not reach later keyboard activation assertions.

Existing [language pending/cancel/resume/fallback cases](../benchmarks/results/landing-language-focus01/pending.txt)
pass10; [landing/server checks](../benchmarks/results/landing-language-focus01/landing.txt)
pass27. The151-file build check passes. Values, chart geometry, installed skills
and downloadable archive stay unchanged. These are controlled interaction checks,
not model token/time or real-network latency measurements.

The Browser runtime initialized but reported no browser; its documented discovery
also returned an empty list. The existing standalone Playwright/Chrome setup was
used. No user browser profile or session data was accessed. Mother-in-law's
interaction workflow guided the checks; the owner's existing improvement/deployment
instruction authorizes this scoped fix.

한국어: 번역 응답이 느릴 때 그래프·표로 이동하면 완료 시 포커스가 본문으로
떨어지는 문제를 고쳤다. 현재 위치를 번역 직전에 확인해 같은 컨트롤로 이어 주며
실험 영역 밖으로 이동했다면 그대로 둔다. 최초 검사 설정 오류2개도 보존했고,
수정된 검사 기준으로 이전12실패·2통과에서 이후14개가 모두 통과했다.
기존 언어 전환10개·랜딩27개도 통과하며 토큰 성능이나 전체 목표 달성은 아니다.

## Hosted verification

Release **`9632bdc98ab64db12e72eefaded4a51dc4b18298`** is live on
[한국어](https://hires.no-money-do-you-have-money.com/ko/) and
[English](https://hires.no-money-do-you-have-money.com/en/).
The [same14 public browser cases](../benchmarks/results/landing-language-focus01/public-browser.txt)
pass, exit0. Translation delay is controlled using the generated fragment; public
pages/scripts load through HTTPS. Separately, [10 HTTPS identities](../benchmarks/results/landing-language-focus01/public.json)
verify both actual public fragments, locale pages, health, runtime assets and
archive/checksum against that release. All52 packaged resource bytes/modes match
source; frozen integration07602,679/current resource1be35120 and canonical/indexable
metadata remain intact. This is not a real-network delay or model benchmark.

The owned preview server was stopped and its process terminated; every browser
context closed. Deployment retained the prior release for rollback. No GitHub push.

한국어: 공개 배포9632bdc9에서도 같은14개 검사가 통과했다. 실제 공개 번역
조각을 포함한 HTTPS10개 경로와 다운로드52개 자원 일치를 별도로 확인했다.
실험 수치는 유지하며 미리보기 서버와 검사 브라우저를 정리했다. GitHub 푸시는 없다.
