# Friday active consumers 01 — 2026-09-15 KST

Resources `8153fec`. Newly authored maintenance-window SQLite release pair, not
production traffic or a broad performance test. Both variants have identical
SQL/readers/requirements; only the point at which down.sql runs during rollback
differs. All five phases, active consumers, value/column contracts and unknown
production facilities are model-visible. Equivalent native implementations are
valid; use of the optional matrix or phase-selection field is not required.

Frozen `friday-active-cases.json` SHA-256:
`c3fdfb8392a7608dd634365291d6326c2560fd934c81a3d95f87790fac0d0ede`.
[Generator](friday_active_cases.py), [preflight](friday-active-preflight.json).
Author-side native unittest passes the compatible order and rejects the other
with an actual active-reader missing-column assertion at rollback starts. Both
reach correct final row values, so final-state-only testing misses the defect.
No setup failure, source change or leftover scratch. Two fixture regression
tests pass in 0.094s. The author oracle is excluded from model files.

## Fixed run and review

Four new sessions, baseline/explicit Friday × two variants × one repeat, serial
Astra medium, 240 seconds/cell, seed 20260911. Preserve every scheduled cell,
gaps, limits and adverse results; no favorable retries. Stop scheduling on account
limits. Freeze resources/inputs and avoid author test workloads during timing.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/friday-active-cases.json --output benchmarks/local-runs/friday-active-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```

Review actual command captures, not final prose alone: exact migrations, state
continuity, active reader selection, column names, post-write record values and
rollback prefix/final observations. Check file preservation and owned scratch
cleanup. Local compatibility in A and rollback-start incompatibility in B must
not become an unsupported production-ready claim. Confirm originals/resources
against launch manifests and reconcile usage before comparing costs.

Inspect whether the skill chooses native SQL or the helper, reads irrelevant
implementation, repeats unchanged evidence, or accidentally removes an active
consumer. A lower query count alone is not an efficiency win. Both arms may
correctly reuse unchanged observations; strict five independent executions are
not required when the unchanged state and inputs justify reuse. Changed data
or schema requires new affected observations.

Retain authored replays separately if needed: they cannot fill a missing original
capture. Publish all four costs and work differences. This correlated n=1 pair
cannot establish a general 20–30% gain or justify changing historical/featured
charts. Evaluate ordinary tool adoption before adding more instructions.

The [official OpenAI evaluation guide](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
informs the task-specific criteria and review of actual tool choices; this uses
the existing repository CLI runner, not the hosted Evals API.

## 한국어

롤백 순서만 다른 새 과제 2종을 고정했다. 정상 순서는 실제 조회·값 검증에
통과하고, 잘못된 순서는 롤백 시작 단계에서 실제 컬럼 오류를 낸다. 둘 다 마지막
값은 정상이라 중간 단계 검사가 중요하다. 정답 테스트는 모델에 제공하지 않는다.

스킬 없는 기준과 Friday를 각각 실행해 4세션을 보존할 예정이다. 도우미 사용을
강요하지 않고 동일 상태의 근거 재사용도 허용한다. 결과와 비용뿐 아니라 검사
범위·누락·불필요한 읽기를 검토한다. 작성 예제 2종, 반복 1회이므로 전체 실사용
성능이나 20–30% 향상을 입증하는 시험으로 표현하지 않는다.
