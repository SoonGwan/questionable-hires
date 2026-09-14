# CLI output localization — 2026-09-15

This is a capture diagnostic, **not a skill-performance comparison**. Four fresh
baseline-only GPT-6 Astra medium sessions used codex-cli 0.153.4, serial execution,
one repeat, seed 20260915 and a 240-second timeout. All completed without timeout.
No skill was loaded. Protocols and fixtures were committed before each launch.

| Frozen protocol / launch | Retained evidence | Expected → recorded command bytes |
| --- | --- | --- |
| [Large budget](CLI-OUTPUT-PROBE-01.md), `d21d6f4` | [output 01](results/cli-output-probe-01/) | tiny 1126→1126; bulk 66646→66646; chunked 66652→66652 |
| [Small budget](CLI-OUTPUT-PROBE-02.md), `9aeae6d` | [output 02](results/cli-output-probe-02/) | tiny 1126→1126; bulk 66646→66646; chunked 66652→66652 |
| [Short yield](CLI-YIELD-PROBE-01.md), `98a2b75` | [yield 01](results/cli-yield-probe-01/) | delayed 92→45 |
| [Long yield](CLI-YIELD-CONTROL-02.md), `4a70281` | [yield control 02](results/cli-yield-control-02/) | delayed 92→45 |

## What the records establish

Each emitter created fresh random BEGIN/END nonces and an exclusive witness file
with the intended payload length and SHA-256. The model was instructed not to read
the emitter or witnesses. Recorded commands are exactly the requested invocations:
three commands for each output probe, one for each delayed probe, all exit 0.
No alternate source/witness access is present in the events. Supplied emitter and
instructions remain byte-identical; only the expected witnesses were added.

All six immediate outputs match their witnesses byte-for-byte and by hash.
Changing the requested output budget alone did not reproduce the missing prefix.
For both delayed probes, the emitter flushes BEGIN, waits two seconds, then flushes
END. The original CLI completion output contains only the 45-byte END line, losing
the 47-byte BEGIN line. Started command records contain no replacement prefix;
there are no incremental output events in these JSONL records.

Nevertheless, every final model answer correctly reports both fresh nonces,
including BEGIN in both delayed probes. This is evidence that the model had access
to information absent from the retained **command-event output**. BEGIN is not
absent from the entire JSONL: the final assistant answer contains it. The witness
is an author-side reconciliation aid, not an extra output read supplied to the model.

The short-yield model reports polling a live session; the long-yield model reports
no polling. Requested `yield_time_ms`/`max_output_tokens` arguments are not available
in the command-completion records, so neither actual tool settings nor the
reported polling distinction is independently established. Manual polling is not
proven necessary. Timing-separated output is a reproducible condition here, not
a source-level root-cause diagnosis or an explanation of every historical gap.

## Reconciliation and limits

Run `python3 -B benchmarks/verify_capture_localization.py` to check the retained
fixtures, exact commands, final nonces, witness payload hashes, byte counts,
command-event extraction, usage equality and terminal metadata. This does not run
the emitter/model or reconstruct missing observations as original evidence.
Original local artifact hashes match each exported `source-sha256.json`; exported
events equal the original JSONL after the existing path-only redaction. Full logs
are retained, including the bulky immediate-output controls.

The first emitter also received a native author preflight before model execution:
all three payload hashes/lengths matched, and duplicate invocation refused the
exclusive witness file with nonzero exit and empty stdout. That preflight is not
a model outcome or a deliberate behavioral-assertion test.

Historical missing-evidence verdicts remain missing evidence for public audit;
they do not establish that the model never saw the omitted content. No historical
scores, graphs, featured claims or skill instructions are rewritten. No performance
win is inferred from these four diagnostic sessions. Next capture work should test
a separately retained incremental-output channel prospectively, before relying on
it for a fresh equal-condition skill comparison.

## 한국어 요약

큰 출력 6개는 원본 해시와 일치했지만, 2초 간격으로 나눈 92바이트 출력은 두
실험 모두 앞의 47바이트가 명령 완료 기록에서 빠졌다. 모델은 그 앞부분의 새
무작위 표식을 정확히 답했다. 따라서 이 경우 기록 누락은 모델의 관측 실패와
같지 않다. 수동 폴링 때문이라고 단정할 수 없고 내부 코드 원인도 아직 모른다.
모든 원본 결과를 보존했으며 이전 판정·그래프를 소급해서 좋게 바꾸지 않는다.
이는 측정 기록의 한계를 확인한 결과이지 스킬 성능 향상 실증이 아니다.
