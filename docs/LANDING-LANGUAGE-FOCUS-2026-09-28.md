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
