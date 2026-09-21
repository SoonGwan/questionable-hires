# Native first-look prototype v2 — 2026-09-21

Status: separate experimental display, **not a shipped skill or measured model
improvement**. The [first prototype's passing overhead](NATIVE-NODE-REPORTER-01.md)
rules out unconditional verbose result JSON. Its source and observations remain
unchanged.

[v2](prototypes/native_node_reporter_v2.mjs) instead displays exceptional outcomes
as positional JSON records with one schema header. Ordinary native pass identities
are explicitly counted as omitted; they remain in the same-run full TAP. Skips and
todos retain their flags. Failure previews remain bounded, with an explicit marker
for truncated strings. Skip/todo pass events and failures each have their own
200-record allowance, so many skips cannot consume the failure allowance. All
omissions are counted. More than200 failures still requires reading raw evidence.

This is **progressive inspection**, not equivalent evidence in fewer bytes. A model
must inspect native exit and relevant raw identities, diagnostics, actual/expected
and stacks before a verification claim. Reading both streams may cost more than
reading TAP directly, especially on tiny suites. File-level success and zero
assertions remain insufficient. No wrapper, input attestation, safe destination
allocator, execution deadline or cleanup is provided by this reporter.

Ten native tests on Node24.16.0 cover:

- Passing display smaller than TAP on a24-test authored fixture, with explicit
  omission of all24 pass identities—not a universal compression guarantee.
- Repeated assertion failures: all24 names retained, native failure preserved,
  exactly24 test-body executions, and display smaller than raw for that fixture.
- A failure following205 ordinary passes remains visible.
- A failure following205 skips remains visible despite the skip display cap.
- Skip/todo/diagnostic handling, exceptional cap and long-name truncation,
  syntax failure, cancellation with explicit native timeout, missing summary,
  and file-level success without authored assertions.

Run (Python3.9 or3.11; Node24 required, otherwise explicit skips):

```sh
python3 -B -m unittest discover -s tests -p test_native_node_reporter_v2.py -v
```

No model sessions or new percentage claims here. Next gate is a complete bounded
capture-and-inspection workflow, including the cost of reading required raw
evidence; only a fresh comparison of that workflow could justify skill adoption.
Do not add this prototype to default entry instructions or change featured charts.

한국어: 정상 통과 목록은 원본에 보존하고 실패·건너뜀·미완료 항목부터 보여주는
별도 시제품이다. 정상 항목이나 건너뜀 항목이 많아도 뒤의 실패가 표시되는지
검사했다. 요약만 보고 검증 완료를 선언할 수 없으며, 원본 확인까지 포함한 실제
비용 절감은 아직 입증되지 않았다. 배포 스킬과 대표 그래프는 변경하지 않는다.
