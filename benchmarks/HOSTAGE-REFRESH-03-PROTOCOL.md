# Refresh-owner 03 — small adoption screen, 2026-09-15

Resources `6b6962c`; [candidate rationale](HOSTAGE-READ-BUDGET-03.md).
Run only two fresh skill sessions, one per existing refresh variant. This is a
cost-limited adoption screen, not a contemporaneous baseline comparison or a
replacement for the all-eight real-use objective. Exposed development tasks;
no held-out, causal or broad performance claim even if costs decrease.

Freeze `hostage-refresh-cases.json` unchanged, SHA-256
`7b0bc8120865802a29dd97b6fedb9863bdbe19742ce68bb93307588b55a04c21`.
Model Astra medium, n=1, serial, seed 20260911, 240s/cell. Same installed-resource
isolation and task-visible files as runs 01/02. No prior conclusions, labels or
author oracle passed to the model. No author workloads/edits during timing,
no selected retries; retain both scheduled cells and stop on account limits.

Inspect actual commands for complete usage-only reads, useful discovery and
combined non-test review without suppressing needed inspection. Report deviations
with context: these are decision guidelines, not a rigid command-count score.
Native test results and their own exits must substantiate final pass claims.
Review the unchanged task's full behavior/scope requirements, not just cost.

After timing reconcile raw usage, installed resources and frozen input; preserve
all gaps and adverse observations. Inspect retained tests, then run separate
project-local, process-bounded controls for final production, faulty cleanup,
valid alternate generation step and the frozen author oracle. Do not use replays
to replace original evidence. Export both cells and label comparisons to earlier
runs as historical, unequal-work observations. Keep featured/historical charts.

If useful behavior and adoption are supported, move to different workflows and
fresh baseline comparisons; do not keep tuning this same pair until a favorable
number appears. Otherwise correct only a demonstrated failure before expanding.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-refresh-cases.json --output benchmarks/local-runs/hostage-refresh-03 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```

## 한국어

새 스킬 세션 2개로 사용법 읽기·탐색·최종 점검 지시가 실제 채택되는지 확인한다.
기본 모델을 새로 실행하지 않으므로 성능 우위 검증으로 쓰지 않는다. 원본 근거와
행동 요구는 그대로 확인하고 실패도 보존한다. 유용한 동작과 지시 채택이 확인되면
같은 과제를 계속 맞추지 않고 다른 작업과 새 기본 모델 비교로 넓힌다.
