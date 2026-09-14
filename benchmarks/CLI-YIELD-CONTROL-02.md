# Completion-before-yield control — 2026-09-15 KST

Same emitter/task as [yield probe](CLI-YIELD-PROBE-01.md), changing only requested
`yield_time_ms` from 1000 to 10000. One fresh baseline Astra medium session,
240-second timeout, seed 20260915, serial, no retries/settings changes. Witness
and command review remain required. This tests whether completing the same
two-second output sequence within the initial wait retains both nonces; it does
not establish a universal capture guarantee or change benchmark defaults.

```sh
python3 -B benchmarks/capture_yield_cases.py --yield-ms 10000 --output benchmarks/cli-yield-control-02-cases.json
python3 -B benchmarks/run.py --cases-file benchmarks/cli-yield-control-02-cases.json \
  --arms baseline --repeats 1 --jobs 1 --seed 20260915 --timeout 240 \
  --model gpt-6-astra --effort medium --output benchmarks/local-runs/cli-yield-control-02
```

한국어: 같은 2초 명령에서 최초 대기 요청만 10초로 바꾼 대조다. 표식·명령·원본
이벤트를 확인하며, 결과가 좋아도 긴 대기를 모든 벤치마크의 해결책으로 강제하지 않는다.
