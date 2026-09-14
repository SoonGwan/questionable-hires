# Hostage refresh-owner transfer 01 — 2026-09-14

Resources `864005b`, new authored cases `hostage-refresh-cases.json`, SHA-256
`7b0bc8120865802a29dd97b6fedb9863bdbe19742ce68bb93307588b55a04c21`.
Two variants share the task/contract: one clears pending on any settlement;
the other correctly leaves ownership with the latest-started refresh. Unlike
the previous form task, every overlapping call must invoke its own callback.
Suppressing, serializing or cancelling older work is explicitly forbidden.

## Preflight, not model evidence

The [generator](hostage_refresh_cases.py) separates its author oracle from the
model-visible files (preview.py, requirements.md, notes.txt only). Native author
preflight runs six methods with actual Preview and owned controlled callbacks.
The valid implementation passes; unconditional cleanup produces three explicit
False-is-not-True assertions for older success/failure/cancellation, not setup
errors. Other controls cover newer-first completion, exact result/error identity,
prior display, latest failure/cancellation/retry, synchronous failure and instances.
[Initial output](hostage-refresh-preflight.json) is retained. Two fixture tests
pass / 0.173s; frozen-input equality and native failure paths are checked.
All scratch is under the benchmark directory and is removed.

## Prospective screen

Run four fresh sessions, baseline/explicit skill per task, Astra medium, serial,
n=1, seed 20260911, 240s/cell. No retries selected for favorable outcomes; no
task/resource/criteria edits or author workloads during timing. Stop scheduling
on account limits and retain failed, timeout, unknown-usage and unattempted cells.
Do not show oracle tests, fixture labels or prior conclusions to the model.

Review actual native tests and evidence-grounded final reports. Fix the faulty
owner without suppressing concurrent callbacks; preserve the valid control and
unrelated notes. Required transitions, identity, safe ownership/cleanup and the
native runner are explicit in the task. Native pass claims need actual results,
not a final shell status. Inspect any missing capture separately from model claims.

After timing reconcile sources/raw usage, preserve every original gap, and replay
retained tests against valid/faulty owner implementations and relevant alternative
correct behavior. Do not use author replay to repair original evidence. Publish
each pair including extra work and cost regressions. These are two correlated
authored variants, not independent production data or evidence of all-eight gains.
Historical/featured charts stay unchanged. No model run has occurred at preflight.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-refresh-cases.json --output benchmarks/local-runs/hostage-refresh-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```

## 한국어

동시 요청을 막으면 안 되는 새 로딩 상태 과제 2종을 준비했다. 정상 구현은
통과하고 잘못된 상태 해제는 성공·실패·취소 3경로에서 실제 단언으로 실패했다.
작성자 정답 테스트는 모델 입력에서 제외한다. 다음 단계는 기본/스킬 총 4세션의
실제 수정·정상 구현 보존·근거 있는 보고·비용 비교다. 아직 모델 실측은 아니다.
