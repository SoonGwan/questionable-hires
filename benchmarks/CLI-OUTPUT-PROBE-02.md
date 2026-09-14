# Low-output-budget control — 2026-09-15 KST

Follow [probe 01](CLI-OUTPUT-PROBE-01.md). Its original completed command outputs
retain all 1,126 / 66,646 / 66,652 expected bytes, and the model reports matching
unpredictable first/last nonces with only the three requested commands. Bulk size
and line flushing alone did not reproduce missing prefixes. Full reconciliation
will be published with both controls, retaining every outcome.

Change only the model-visible output-budget request: exactly 1,000 tokens if
configurable, instead of at least 20,000. Same emitter, three commands, generated
witnesses, no file reads/redirects/retries. Command-completion events do not expose
the actual output-budget argument, so prompt compliance for that parameter is not
independently established. Inspect original outputs and markers rather than
assuming the requested budget took effect. This is not a skill or timing benchmark.

One fresh baseline session, Astra medium, serial, 240 seconds, seed 20260915.
Do not modify source/settings during execution. Preserve all results; no retry.

```sh
python3 -B benchmarks/capture_probe_cases.py --output-tokens 1000 --output benchmarks/cli-output-probe-02-cases.json
python3 -B benchmarks/run.py --cases-file benchmarks/cli-output-probe-02-cases.json \
  --arms baseline --repeats 1 --jobs 1 --seed 20260915 --timeout 240 \
  --model gpt-6-astra --effort medium --output benchmarks/local-runs/cli-output-probe-02
```

한국어: 큰 출력 예산을 요청한 첫 대조는 전체 바이트가 보존됐다. 이번에는
출력 예산 요청만 1,000토큰으로 바꾼다. 실제 도구 인자는 완료 이벤트에 없어
요청 준수를 확정할 수 없으므로 원본 표식·출력으로 판정한다. 성능 시험이 아니다.
