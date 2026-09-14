# Conditional-example adoption screen — 2026-09-15 KST

Freeze Con Artist resources at `bec12d6`, HTTPX at
`26d48e0634e6ee9cdc0533996db289ce4b430177`. Use the existing unchanged
`audit` / `asgi-exceptions` task in `run_httpx.py`, not a hinted new prompt.
This revisits an exposed author-selected audit on real upstream source, not an
organic maintainer ticket, independent holdout or all-eight performance study.

Question: does the model use the common interface and avoid unnecessary stronger
probe validation when native existing assertions already detect the selected
fault? Equivalent direct native checks remain valid; helper adoption is not a
scoring requirement. A required normal control must not be skipped merely because
it shares a probe with an optional stronger assertion.

Fresh baseline and skill, one repetition each, GPT-6 Astra medium, existing
seed 20260912 schedule, serial execution, 360 seconds per cell. Same full checkout,
interpreter and task; committed resources frozen before timing. Preserve both
outcomes, no retries or candidate changes while running; stop scheduling on limits.
Do not run author workloads during model timing. A live handle is polled rather
than restarted after an observation timeout.

Author preflight: [native output](httpx-exception-example-preflight.json), produced
by `preflight_httpx_exception_example.py` in project-local disposable copies.
Correct ASGI suite: 24 pass. Removing exception propagation: 4 fail / 20 pass,
with `DID NOT RAISE RuntimeError` at test_asgi.py:172 and :180 under asyncio and
trio. Independent actual-client witness passes correct code and fails faulty code
with the expected swallowed-exception assertion. These tests/results stay outside
model projects; they establish the fixture's intended behavior, not model evidence.

Review original commands, actual implementation/binding, unchanged native test
results, the detecting assertion, scope and preservation. Missing native output
is a gap; author replay cannot repair the original transcript. Inspect optional
guide usage, helper parameters and extra checks without prescribing a call count.
Report complete input tokens (cache included once) plus output and process wall
time, both arms and unequal work. Two fewer subprocesses in a documentation test
are not a model efficiency gain. One pair cannot establish causality or broad
20–30% superiority. Do not change featured charts from a favorable observation.

```sh
python3 -B benchmarks/run_httpx.py \
  --source /tmp/qh-httpx-preflight.3Slnqw/httpx \
  --python /tmp/qh-httpx-preflight.3Slnqw/venv/bin/python \
  --profile audit --case asgi-exceptions --arms baseline skill --repeats 1 \
  --skill-revision bec12d6 --output benchmarks/local-runs/httpx-exception-example-01
```

This follows [OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
on task-specific objectives and reviewing metrics alongside judgments; it does
not use an external grading service or substitute a generic score for native proof.

한국어: 수정 예제를 포함한 스킬과 기본 모델을 동일 HTTPX 과제로 한 번씩 비교한다.
정상 24개 통과·결함 4개 실제 실패를 사전 확인했지만 이 작성자 근거는 모델에게
제공하지 않는다. 기존 테스트가 잡은 결함에 불필요한 추가 검증을 붙이는지 살피며,
필수 검증은 생략할 수 없다. 이미 노출된 과제이며 전체 성능·인과관계의 증거가
아니다. 불리한 결과·출력 누락도 남기고 기존 그래프는 유지한다.
