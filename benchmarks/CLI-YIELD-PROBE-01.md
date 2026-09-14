# Yielded-command output control — 2026-09-15 KST

Both prior [high](CLI-OUTPUT-PROBE-01.md) and [low](CLI-OUTPUT-PROBE-02.md)
requested output-budget controls retain complete bulk/line-flushed output.
Next isolate command yielding: one command prints an unpredictable BEGIN nonce,
flushes, waits two seconds, then prints an independent END nonce. It writes an
exclusive local witness before printing. No model source/witness reads permitted.
The model requests a 1,000ms command yield and polls the same live session if needed.
This is an intentional tiny diagnostic wait, not an application performance test.

One baseline Astra medium session, existing ephemeral JSONL runner, serial,
seed 20260915, 240-second deadline. No repeats/restarts or resource/settings changes.
Review actual emitted events and model-reported marker visibility; command tool
arguments are not independently included in completed events. A model claim about
polling alone is not a low-level trace. Marker agreement requires checking that no
alternate file/command access occurred. All historical results remain unchanged.

```sh
python3 -B benchmarks/capture_yield_cases.py --output benchmarks/cli-yield-probe-01-cases.json
python3 -B benchmarks/run.py --cases-file benchmarks/cli-yield-probe-01-cases.json \
  --arms baseline --repeats 1 --jobs 1 --seed 20260915 --timeout 240 \
  --model gpt-6-astra --effort medium --output benchmarks/local-runs/cli-yield-probe-01
```

한국어: 앞선 두 대조에서는 누락이 없어, 이번에는 최초 출력 뒤 대기하고 같은
세션을 폴링하는 경로를 분리한다. 시작·종료 표식과 원본 이벤트를 비교하며
모델의 폴링 설명만으로 내부 구현을 단정하지 않는다. 성능 수치 시험은 아니다.
