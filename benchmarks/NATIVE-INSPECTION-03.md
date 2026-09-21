# Native full-inspection accounting — 2026-09-21

Decision: **do not ship the custom first-look reporter as a default workflow**.
The [v2 prototype](NATIVE-NODE-FIRST-LOOK-02.md) is smaller on selected large
fixtures only if required raw inspection is left out. Reading the complete raw
stream afterward adds cost on every case. Selective inspection may differ, but
has not been measured or established as sufficient for any developer task here.

## Four authored cases, all retained

Node24.16.0, one native execution per case with TAP, native `spec` and v2 reporters
attached to the same run. Invocation markers confirm1/24/24/206 test executions.
This is byte accounting, not model-token, latency, billing or correctness evidence.

| Case | Native exit | TAP bytes | Native spec bytes | First-look bytes | First-look + full TAP | First-look + full spec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| One pass | 0 | 201 | 138 | 814 | 1,015 | 952 |
| 24 passes | 0 | 2,148 | 698 | 822 | 2,970 | 1,520 |
| 24 failures | 1 | 23,632 | 20,616 | 6,314 | 29,946 | 26,930 |
| Failure after205 passes | 1 | 18,966 | 6,158 | 1,060 | 20,026 | 7,218 |

Every completed run also emitted **267 stderr bytes** with a native
`MaxListenersExceededWarning` when three reporters were attached. The table counts
report streams only; complete reading of stderr adds267 bytes to each relevant
column, and native exit/command/input identity and inspection interactions add
further overhead not measured here. No warning was suppressed or classified as a
test failure. This three-reporter harness is not proposed as a production command.

The first harness attempt stopped after one passing test because the author's
assertion incorrectly required empty stderr. Its native exit0, warning, logs and
invocation marker are retained separately. The script was revised to preserve
stderr presence and identity rather than reject it; all four cases were then
run in a new directory. Total authored attempts: five, including that first case.
These are not model retries or an independent holdout.

[Original observations, redacted output strings and both-byte identities](results/native-inspection-03.json)
retain every run, source, argv, full TAP/spec/first-look, stderr, exit and markers.
Original counts/hashes refer to pre-redaction strings. Published JSON embeds exact
text strings after workspace/executable-path redaction, preserving whitespace.
The artifact test reconciles source/output identities, invocation counts, exits,
both full-inspection sums and the initially rejected attempt.

## Consequence for skill development

Native `spec` was smaller than TAP in these four cases while retaining readable
test identities and failure diagnostics. It is an existing Node feature, **not a
skill innovation or proof of equivalent machine-readable evidence**. Existing
TAP-dependent parsers must not be switched. No model has been shown to solve a
task faster or with fewer tokens because of it; normal project reporter selection
should take precedence over injecting another layer.

Do not spend new model sessions testing the unconditional custom-reporter route.
Before revisiting progressive inspection, identify a real task where specific
raw evidence can be selected without rereading the whole stream, and compare the
whole interaction with the project's native output—including tiny passing cases.
Until then, keep this in experiments, not skill instructions, default wrappers or
featured charts. Production capabilities and prior benchmark conclusions unchanged.

Reproduce in a fresh directory:

```sh
python3 -B benchmarks/profile_native_inspection.py --output benchmarks/local-runs/native-inspection-fresh
python3 -B -m unittest discover -s tests -p test_native_inspection_accounting.py -v
```

한국어: 네 예제 모두 요약과 원본 전체를 함께 읽으면 표시량이 늘었다. 기존 Node
출력 형식인 spec도 이 예제들에서는 TAP보다 짧아서, 별도 요약기를 기본 기능으로
추가할 근거가 없다. 세 리포터 동시 사용으로 발생한 경고와 최초 측정기 중단도
보존했다. 실제 작업의 토큰·시간 절감은 입증되지 않았으며 배포본·그래프는 유지한다.
