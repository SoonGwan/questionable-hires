# Native-probe selection interface model01 — 2026-09-28

Previous resources **`4dac0d2b`**, candidate **`e7e1f8b2`**, frozen execution
**`9df733a1`**. [Protocol](AUDIT-PROBE-SELECTION-MODEL01-PROTOCOL.md),
[original costs](results/audit-probe-selection-model01/comparison.json),
[response counters](results/audit-probe-selection-model01/response-cost.json),
[arithmetic](results/audit-probe-selection-model01/metrics.json).

**Joint model-cost gate fails.** The shared-probe candidate really removes two
native processes, but its whole-task tokens increase. The distinct-probe control
uses fewer tokens but takes longer. Keep the [native optimization](AUDIT-PROBE-SELECTION-01.md)
for its demonstrated scope; do not claim model efficiency or retry unchanged cells.

| Task | Previous tokens | Candidate tokens | Change | Previous CLI s | Candidate CLI s | Change | Responses |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Shared native probe |129,718|131,745|+1.56%|40.688|39.596|−2.68%|6→6|
| Distinct native probes |137,194|134,644|−1.86%|47.002|54.010|+14.91%|6→6|
| Sum |266,912|266,389|−0.20%|87.690|93.606|+6.75%|12→12|

Input counts cached input once, plus output. All four complete within360 seconds,
without limit, timeout, scheduler retry or replacement. Actual contexts confirm
Astra/medium. No author native tests/replays ran during model timing. This is an
explicit helper-interface study, not a no-skill or natural-adoption comparison.

## What actually executed

[Original native review](results/audit-probe-selection-model01/native-review.json)
checks exactly one actual installed audit.py invocation in each cell, unchanged
recipe, required interpreter and outer exit0/status observed. Both arms use native
`python -B -m unittest` in copied projects. Each executed check runs one non-skipped
method, with expected native/check exit agreement, no timeout or truncated check
output. This conclusion comes from original returned results, not the final answer
or the author's earlier preflight.

All original positive/integer tests pass on correct code and on their prescribed
return2/3/4 mutants. Correct stronger probes pass; all three mutant probes fail
through their intended assertions at copied test_stronger.py line9:

| Task | Actual stronger mutant assertion values | Previous native processes | Candidate native processes |
| --- | --- | ---: | ---: |
| Shared |2 !=1;3 !=1;4 !=1|11|9|
| Distinct |2 !=1;6 !=2;'4' !='1'|11|11|

Copied service hashes match actual correct/mutant source bytes. Every executed
check reports copied service/test module imports and same-process binding precheck
completion. Probe bodies confirm their imported value function is service.value
before the behavioral assertion. These are reached assertion failures, not import,
syntax, setup or early-exit failures.

Both arms reuse the third original positive baseline from audit0, while the integer
baseline executes separately. Only candidate/shared reuses audit0's correct stronger
probe for audits1/2; previous/shared executes all three. Both distinct arms execute
all three different correct probes. References point directly to actual earlier
successful observations. All mutant originals and all mutant probes still execute;
no requested mutation/check is left unrun. Final answers accurately report9/11
processes and distinguish repeated comparisons from executions.

## Unequal reading and review work

All sessions take six model responses. Shared previous reads native/common/probe
guides and performs Git status/HEAD checks before and after. Shared candidate reads
native/common/batch guides, then audit.py's first160 and last85 lines as well as
source/discovery and README. Its native report is1,492 characters shorter, but the
five CLI outputs together grow44,321→54,122 characters. These raw redacted output
sizes are not tokenizer counts. Additional implementation/reference reads remain
charged; they are observed choices, not proof that documentation caused them.

Distinct previous reads native/common/probe guides and emits a full initial inventory,
then summarizes its identical final inventory. Candidate additionally reads the batch
guide, independently checks Git status and emits only inventory count/equality summaries
to the model while retaining full raw CLI inventories. Both original before/after
inventory strings match exactly, including installed resources/Git. These are different
read/report workflows; raw CLI character totals do not describe identical model-visible
input. Initial response input is14,634 tokens in three cells and14,739 in candidate/
distinct. The response-cost decomposition is arithmetic, not causal attribution.

## Capture, preservation and limitations

[Artifact review](results/audit-probe-selection-model01/artifact-review.json) verifies
unchanged original project inventories, installed resources, HEAD and captured
pre-collector index bytes/modes in all four. [Frozen identity checks](results/audit-probe-selection-model01/frozen-identity-review.json)
confirm exact task files and condition resource snapshots. Helper integrity reports
confirm selected originals, authorized whole-project boundaries and owned-copy removal.
These before/after observations do not prove absence of all transient actions.

[Capture review](results/audit-probe-selection-model01/capture-review.json) accounts
for24 CLI commands. Twenty-one complete outputs exactly match their paired original
records; three inventories are deliberately transformed into counts/equality in the
original tool response, with full CLI inventories retained separately. Their summaries
are not reconstructed full outputs. Two initial automatic associations were unresolved
because a command used a const variable; [the initial review](results/audit-probe-selection-model01/capture-review.initial.json)
is retained. Manual literal/order review resolves both without replay. No original
call/output is missing or duplicated; no truncation marker occurs in the full output
pairs. No missing-prefix recovery or author execution substitutes for model evidence.

Exact entry bodies are observed in tool output for all four; initial exposure is
unobserved, not proven absent. Private initial instruction text is not published.
[Preflight](results/audit-probe-selection-model01/preflight.json) contains42 actual
native checks and four fresh public imports across both resource versions/tasks.
Four synthetic scheduling/resource controls pass in checkout and a Git-free file
copy; these are separate author controls, not model evidence.

The two tasks deliberately exercise an exposed mechanism, share source and are
correlated; n=1, shared host/cache, different optional reads and initial contexts
limit interpretation. No independent-validation, uniform saving or all-eight claim
follows from the small favorable token sum. Both READMEs retain native capability
claims without claiming measured model savings. Featured data and integration07
remain frozen; installed/hosted source from the native checkpoint is unchanged.

한국어: 실제 모델 실행에서도 재사용 배치의 검사 수11→9는 확인했지만 토큰은
1.56% 증가하고 시간만2.68% 감소했다. 다른 강화 검사가 필요한 대조 배치는
토큰1.86% 감소·시간14.91% 증가다. 합계 토큰0.20% 감소만 강조하지 않으며
시간은6.75% 증가했다. 네 실행의 필수 결과·원본 보존은 유지됐지만 추가 코드/
문서 읽기와6→6응답을 포함한 전체 비용 개선 기준은 미달이다. 네이티브 최적화는
유지하고 동일 실험 재시도나 대표 수치 승격 없이 모든 원본과 한계를 보존한다.
