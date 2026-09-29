# Integration07 costs — 2026-09-28

Measured bundle **`1be35120`**, execution **`47a00692`**. [Protocol](ALL-EIGHT-CURRENT-07-PROTOCOL.md), [original review](ALL-EIGHT-CURRENT-07-REVIEW.md), [machine-readable costs](results/all-eight-current-07/comparison.json).

**Whole-task tokens increase 1.67%; CLI elapsed decreases 9.63%. The all-eight objective remains unmet.** Only Necromancer and Exorcist decrease both. All 16 original cells complete without timeout, limit, retry or replacement.

| Role | Baseline tokens | Current tokens | Change | Baseline seconds | Current seconds | Change | Responses B/C |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mother-in-law | 62,395 | 83,250 | +33.42% | 40.404 | 47.337 | +17.16% | 4/5 |
| necromancer | 82,293 | 68,149 | -17.19% | 51.183 | 43.861 | -14.31% | 5/4 |
| receipt | 66,558 | 72,249 | +8.55% | 70.871 | 31.267 | -55.88% | 4/4 |
| hostage-negotiator | 82,569 | 86,910 | +5.26% | 109.352 | 101.527 | -7.16% | 5/5 |
| exorcist | 76,732 | 63,130 | -17.73% | 48.469 | 43.636 | -9.97% | 5/4 |
| con-artist | 81,561 | 85,758 | +5.15% | 75.373 | 73.369 | -2.66% | 5/5 |
| landlord | 76,806 | 77,420 | +0.80% | 34.669 | 33.372 | -3.74% | 5/5 |
| friday | 63,869 | 65,813 | +3.04% | 64.669 | 72.933 | +12.78% | 4/4 |

Totals: **592,783 → 602,679 tokens**, **494.990 → 447.302 seconds**, **37 → 36 responses**. Tokens decrease in 2/8 pairs; elapsed in 6/8. These are sums, not averages of normalized task ratios.

Input includes cached input once; output includes reasoning rather than adding it again. Original per-response profiles reconcile with each CLI total. Elapsed measures each serial CLI lifecycle, not only native execution. Actual recorded contexts are Astra/medium in all 16 cells. Baseline installs no task skill; current installs only its matching role from the bundle.

Eight current entries have exact full-body observations in tool output; none has an exact structured initial-body match. Missing matches do not prove absence. The [loading audit](SKILL-LOADING-01.md) documents historical variation without assigning a cause. Initial context, shared-host timing/cache, n=1 and repeatedly exposed authored cases prevent causal or independent-validation claims.

Response accounting is descriptive, not causal: Mother adds one response (4→5), while Necromancer and Exorcist each remove one (5→4). Mother’s +20,855 tokens decompose into +14,583 response-count, +837 first-input, +5,237 later-input and +198 output terms under the existing symmetric arithmetic. This does not prove that removing a call would retain quality or achieve that saving. See [all decompositions](results/all-eight-current-07/response-cost.json).

Native work differs: Exorcist baseline repeats more actual tests; Necromancer baseline tests all three variants while current directly probes all variants and runs the current suite; Con Artist uses different process/suite groupings. Receipt uses its helper without optional argument observation. Con Artist does not use its updated helper. The changed helper capabilities therefore cannot explain this aggregate by themselves.

Integration06 remains its historical +16.95% tokens/−10.00% elapsed result at `1d0e92ac`; the difference between cohorts is not a controlled optimization effect. No featured pointer or frozen chart is changed. No new skill improvement or quality superiority is established by this screen.

한국어: 현재 묶음 `1be35120`의 integration07은 미적용 대비 합계 토큰 1.67% 증가, 시간 9.63% 감소다. 토큰·시간 동시 감소는 2/8이며 전체 목표는 미달이다. 반복 노출 과제·조건별 1회·추가 검사 차이가 있어 독립 검증이나 인과적 개선으로 해석하지 않는다. 기존 integration06과 대표 확인 실험은 과거 자원에 연결된 수치를 유지한다.
