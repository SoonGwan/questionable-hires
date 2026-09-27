# Copy feedback request ordering — 2026-09-28

Parent **`7a1bce63`**. On two rapid installation-copy clicks, the older promise
could replace the newer attempt's success with a failure, or its failure with a
success. This affects visible feedback in both languages. The UI contract adopted
here is that feedback belongs to the most recent click, in the current locale;
copy requests retain the same installation command.

`landing/app.js` now assigns each click a request number, keeps its outcome local
until settled, and updates shared copy state/status only when still current. It
neither cancels a clipboard operation nor claims what an unobserved promise did.
Normal copying, retry, enabled-button behavior and locale changes remain available.
There is no new dependency, translated string, layout or benchmark change.

The [browser regression](../tests/browser/landing_copy_order.cjs) uses real clicks
and rendered status at390px in KO/EN. Its controlled clipboard promises exercise
normal success, failed-then-successful retry, older failure after newer success,
older success after newer failure, reversed two-success completion and a locale
switch while pending. It checks the exact command passed to every write, enabled
button, visible live status and page errors. It does not change the OS clipboard
or validate physical clipboard writes/permissions. No sleep-based ordering is used.

- [Before](../benchmarks/results/landing-copy-order01/before.txt):12 cases,4 actual
  stale-feedback assertion failures,8 passing controls; native process exit1.
- [After, unchanged checks](../benchmarks/results/landing-copy-order01/after.txt):
  all12 pass, native exit0. Browser/contexts close after every case/run.
- [Source and checker identity](../benchmarks/results/landing-copy-order01/identity.json)
  retains original/fixed app hashes and the unchanged regression hash.
-151-file static build and19 existing landing tests pass. Skill archive, published
  measurements and featured images remain unchanged. No model call or cost gain.

Executed with a90-second subprocess bound:

```sh
node tests/browser/landing_copy_order.cjs http://127.0.0.1:4198/landing/ /path/to/playwright
```

The optional third argument selects the existing Playwright module; otherwise
normal Node module resolution is used. Chrome defaults to the installed Mac app;
`QH_CHROME_PATH` can specify another Chrome executable. Each page/action has a
bounded timeout. The in-app browser discovery returned no available browser, so
these are standalone Chrome observations, not in-app browser coverage.

한국어: 복사 버튼 연속 클릭 시 이전 요청이 마지막 요청의 성공·실패 안내를
덮어쓰는 문제를 양쪽 언어에서 재현했다. 마지막 클릭의 결과만 반영하도록
수정했고, 동일한 실제 브라우저 검사12개가 모두 통과했다(수정 전4실패).
정상 복사·재시도·처리 중 언어 전환을 유지한다. 클립보드 응답은 통제했으며
실제 OS 클립보드는 바꾸지 않았다. 모델 토큰 절감이나 전체 목표 완료는 아니다.
