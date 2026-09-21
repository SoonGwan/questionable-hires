# Receipt versions01: original response-cost review

2026-09-22. Analysis of all six completed sessions, not a new model run.
Resources and outcomes remain those in the [review](RECEIPT-VERSIONS-01-REVIEW.md).
The existing `analyze_response_costs.summarize/compare` validates the stored
per-response counters in [measurements.json](results/receipt-versions-01/measurements.json).
No token estimates from prose length and no additional profiling implementation.

| Request | Condition | Responses | First input | Total input | Output |
| --- | --- | ---: | ---: | ---: | ---: |
| Single | Baseline |5|14,873|80,674|1,580|
| Single | Predecessor |6|14,977|110,301|1,138|
| Single | Current |4|14,961|66,181|1,819|
| Multiple | Baseline |5|14,884|82,427|1,791|
| Multiple | Predecessor |5|14,989|103,133|2,313|
| Multiple | Current |5|14,973|97,886|1,110|

For input `I = n*f + g`, symmetric response-count/first-input terms plus the
later-input/output differences reconcile exactly. All rows below compare the
named skill condition with its matching baseline. These are arithmetic
identities, **not causal attribution or safely removable costs**.

| Request / condition | Count term | First-input term | Later-input term | Output term | Total delta |
| --- | ---: | ---: | ---: | ---: | ---: |
| Single / predecessor |14,925|572|14,130|−442|29,185|
| Single / current |−14,917|396|28|239|−14,254|
| Multiple / predecessor |0|525|20,181|522|21,228|
| Multiple / current |0|445|15,014|−681|14,778|

Current's two deltas sum to524 extra tokens. Cached input is already included
in input; reasoning is not added again to output. First input includes all
initial context, not just a skill. Response counts differ from shell-call counts
and do not measure wall time.

## What the original commands establish

- Current/single has one fewer recorded response than baseline, but reads only
  the unchanged Receipt entrypoint and builds a custom comparison. The new
  multi-version parameter is not used. A lower count is not evidence of the
  parameter causing savings, and this cell still takes longer than baseline.
- Predecessor/single reads the Python guide, then searches implementation for
  assertion/output/invocation behavior before using the pairwise helper. Its
  extra response is an actual inspection, not an automatic recovery or a
  repeated failed test. No unambiguous correctness defect justifies removing it.
- Both multiple skill sessions read the entire Python guide and implementation
  in one command. Both have the same five recorded responses as baseline.
  Later input contains those reads, prior conversation and native output; the
 15,014-token current term cannot be labeled entirely as helper-source overhead.
- Current/multiple executes the supported batch helper. Predecessor/multiple
  builds a custom native runner and imports the inventory utility. Both execute
  current once, as baseline also does. There is no redundant native execution
  for a new optimization to remove in these recorded sessions.
- Four custom runners add tracing/profiling to retain passing assertion values;
  two helper runs retain native failure values and passing test identities.
  The task explicitly requests actual assertion values and comparison of passing
  controls. Additional observations are not automatically waste. Do not remove
  native checks, rewrite assertions or silently narrow the requested evidence.

## Decision for further work

Do not add another generic “read less”, batching, helper-mandatory or stop-early
instruction. The guide already says its recipes do not require implementation
reading and that a concrete trust/adaptation question can justify inspection.
Previous [reference consolidation](RECEIPT-REFERENCE-COMPACT-01.md) and
[entry consolidation](RECEIPT-ENTRY-COST-01.md) are existing attempts, not fresh
ideas to repeat under another name.

Do not add assertion tracing to the helper based solely on these two authored
variants: their custom instrumentation is a reasonable response to the supplied
task, not yet a repeated independent user need or a demonstrated helper defect.
Tracing changes runtime behavior and needs its own compatibility contract; more
options and instructions could worsen the observed input cost.

The optional multi-version feature remains functional. This review supplies no
evidence-backed additional Receipt edit or favorable rerun. Broader improvement
work must look for a different concrete bottleneck or correctness failure across
the bundle, rather than continuing this exposed case or inflating its headline.
No resource, frozen measurement, featured pointer or localized graph changes.

한국어:6회 원본 응답별 토큰을 모두 대조했다. 다중 버전에서는 세 조건 모두
응답5회·현재 버전 검증1회였고, 추가 입력에는 안내와 구현 읽기가 포함됐다.
하지만 이를 전부 제거 가능한 낭비라고 볼 수 없다. 지침 압축·도구 강제·검증
삭제를 반복하지 않으며, 이 과제에만 맞춘 추적 기능도 추가하지 않는다.
