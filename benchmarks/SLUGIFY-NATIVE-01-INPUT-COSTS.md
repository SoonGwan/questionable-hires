# Slugify remaining-cost diagnosis — 2026-09-21

Measured resource `a7dcbd8`; this analysis follows `3fa1758` and reuses the three
[original sessions](SLUGIFY-NATIVE-01.md). No new model calls or performance gain.
The existing `analyze_response_costs.compare` function reconciles original
response counters; [arithmetic with profile hashes](results/slugify-native-01/input-cost-analysis.json)
is retained. No second profiler or text-based token estimator was added.

| Current minus reference | Response-count term | First-input term | Later-input term | Output term | Total-token difference |
| --- | ---: | ---: | ---: | ---: | ---: |
| No-skill baseline |15,647.5|4,603.5|11,450|−638|31,063|
| Prior recipe |−16,154|55|−16,861|−141|−33,101|

These are the exact symmetric decomposition already defined in
[the all-eight input analysis](ALL-EIGHT-03-INPUT-COSTS.md): input=`n*f+g`, where
`n` is recorded response count, `f` first-response input and `g` subsequent input
relative to `f`. The product difference is `delta_n*mean(f)+delta_f*mean(n)`.
**Terms are accounting identities, not causal costs or recoverable savings.**
Initial input includes all recorded initial context, not just the skill; subsequent
input includes source reads, prior conversation, generated work and evidence.

Current has5 responses versus baseline4 and prior6. Current output is already
smaller than both references. Reducing final-answer length alone is not supported
as the main correction. Current has31,701 more input tokens than baseline and
638 fewer output tokens; native process count is not a token-count multiplier.

## Why not add a grouping mode immediately?

Both skill arms used8 native processes for12 methods. Baseline grouped those
methods by variant into4 processes. All meet the frozen task, but their setup
grouping differs. The helper currently pairs each selection with matching correct
code, caching only identical test arguments and other execution identity.
Its existing recipe already accepts suites and test overrides; it does not offer
a single explicitly different normal-suite plan for multiple mutant selections.

Simply grouping each fault's selected and witness methods would produce three
different paired selections, not the baseline's one shared correct suite. Treating
one larger correct suite as interchangeable with smaller selections would change
reuse semantics, especially for stateful tests. It must not be a silent cache
optimization. New explicit orchestration would add interface/inspection cost and
would still need required method evidence, failed-correct stopping, provenance,
integrity and cleanup. Fewer child processes alone does not demonstrate lower
whole-task tokens or wall time.

Decision: **do not add a new grouping API based only on this count difference**.
Keep the narrower recipe correction provisionally, preserve its adverse baseline
comparison, and inspect whole-bundle regressions before further helper expansion.
The existing source/context reads, response boundaries and returned evidence
remain observed contributors to the conversation, not proven dispensable work.
Previous failed read-order/output-reduction experiments remain in the history;
this analysis is not a license to repeat them unchanged.

## Whole-bundle scope

Diffing last all-eight resource `ee5eb28` against `3fa1758` finds changes in six
roles: Con Artist, Receipt, Friday, Hostage Negotiator, Mother-in-law and Necromancer.
Landlord and Exorcist resources are unchanged. The old all-eight20.34% token
increase cannot be silently relabeled as a current measurement. Local full-suite
validation can check regressions across the current checkout, but cannot replace
whole-task cost measurement or independent generalization evidence.

한국어: 무스킬 대비31,063토큰 증가를 기존 분석기로 분해했다. 응답 횟수·초기
입력·누적 입력 차이가 함께 있으며 출력은 오히려 줄었다. 이 계산을 원인이나
절감 가능량으로 단정하지 않는다. 프로세스 수만 보고 새 배치 기능을 추가하면
검증 의미와 사용 비용을 바꿀 수 있어 보류한다. 전체 회귀 검사와 실제 성능
측정은 별도 근거로 유지한다.
