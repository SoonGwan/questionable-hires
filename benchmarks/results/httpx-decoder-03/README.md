# Native probe files adopted: lower time, aggregate tokens still higher

Against four fresh HTTPX sessions, Con Artist uses **16.5% more total tokens and
30.4% less process time** by equal-case mean ratios. Both arms reach the correct
core conclusions. The new native probe interface is used successfully without
repair in the one task requiring stronger tests. The aggregate token objective
and broad eight-skill goal remain unmet.

한국어 요약: 두 과제 평균으로 시간은 30.4% 줄었지만 토큰은 16.5% 늘었다.
새 테스트 파일 인터페이스는 실제 모델 세션에서 오류 복구 없이 사용됐다.
다만 조건별 추가 검증이 다르고 각 과제·조건을 한 번씩만 실행했으므로 전체
스킬의 보편적 성능 향상이나 동일 작업의 확정적 절감으로 해석하지 않는다.

## Frozen run and every cell

[Protocol](../../HTTPX-DECODER-03-PROTOCOL.md), [manifest](run.json).
Full HTTPX checkout at `26d48e0634e6ee9cdc0533996db289ce4b430177`, Con Artist
at `89d91af`, GPT-6 Astra medium. Two exposed author-selected development tasks,
one repetition per arm, serial execution, 360-second limit, skill-first order.
Preflight: 40 decoder tests pass. All four sessions complete; none retried or
excluded. Resources and criteria remain frozen throughout execution.

| Task | Arm | Total tokens | Cached input | Seconds |
| --- | --- | ---: | ---: | ---: |
| Split CRLF | [baseline](line-crlf-split--baseline--1/answer.md) | 106,281 | 77,824 | 73.423 |
| Split CRLF | [skill](line-crlf-split--skill--1/answer.md) | 142,367 | 123,392 | 49.727 |
| UTF-8 finalization | [baseline](text-finalization--baseline--1/answer.md) | 196,497 | 171,520 | 95.949 |
| UTF-8 finalization | [skill](text-finalization--skill--1/answer.md) | 194,444 | 149,632 | 68.551 |

Total tokens = input (cached included once) + output. Equal-case mean of
skill/baseline ratios minus one: +16.4543% tokens, −30.4140% time. UTF-8 alone is
−1.0448% tokens / −28.5548% time; this favorable cell does not replace the aggregate.
The [previous run](../httpx-decoder-02/README.md) and its adverse token costs remain
intact. Different fresh baselines and one repetition prevent causal attribution
of historical differences to the interface change.

## Reviewed execution

- CRLF baseline changes carried CR into LF. Skill removes trailing-CR deferral.
  Both are narrow carry-over faults, but not identical mutations. Both take the
  existing suite from 40 pass to 39 pass / 1 fail at `test_decoders.py:339`, with
  the extra empty line visible in actual/expected output. The two preceding
  unsplit assertions pass. Baseline additionally checks the nearby Issue 1033
  case in separate diagnostic processes; skill does not. No stronger probe is
  needed or claimed by skill.
- UTF-8 both disable `TextDecoder.flush()`'s final flag. Existing tests stay
  40 pass on correct and mutant. Baseline's focused suite goes from 4 pass to
  2 fail / 2 pass (sync and asyncio). Skill's goes from 6 pass to 3 fail / 3 pass
  (sync, asyncio and Trio). All incomplete-EOF cases fail for a missing U+FFFD;
  valid split-euro controls pass. Both compare joined text, with different ASCII
  prefixes. Additional Trio coverage is not counted as a second independent task.
- Both skill sessions use one audit-helper invocation. UTF-8 selects
  `probe_files`/`probe_tests` directly, with no nested source wrapper, syntax-error
  repair or repeated helper call. Its check function verifies copied decoder
  paths and both synchronous/asynchronous caller globals inside each focused
  test. Baseline verifies copied package imports in its pytest process but not
  those explicit caller bindings. CRLF skill verifies implementation imports in
  the test process; static caller inspection is not a runtime binding assertion.
- The author compared all 125 upstream tracked files in each final snapshot to
  the pinned source: byte-identical in all four. Model commands and integrity
  checks were reviewed too; final snapshots alone cannot prove every transient
  action. No dependency installation or upstream mutation was observed.

All four capture diagnostics contain no invalid JSON, empty command output,
error-event or rejected-patch entries. That is not a complete-capture guarantee.
The decisive helper phase outputs are not truncated or timed out. Neither arm
needed the interpreter-path or source-string repairs seen in the preceding run.
Skill still inspects helper source (a prefix on CRLF and search matches on UTF-8).
Adoption has removed custom orchestration, not all model context overhead.

## Limits and next decision

This verifies that the new interface is usable in a real model session and
preserves the intended fault/normal checks. It does not establish universal
efficiency, current-upstream defects or maintainer-ticket effectiveness. Work,
fault choice and provenance differ; shared caches, skill-first order, exposed
tasks and n=1 remain limitations. No heavy author regressions ran during timing.
The remaining cost problem is most visible in the CRLF task, where existing
coverage already suffices. Do not keep rerunning these two cases to chase a score;
further changes need a concrete workflow-cost hypothesis and separate confirmation.

## Compact evidence

Each cell retains commands, outputs/events, metadata, answer, source-log hashes,
original decoder/test excerpts and HTTPX's BSD-3-Clause license. The baseline
UTF-8 report is also retained. Full project copies and generated diffs remain
recoverable in ignored local export storage, not deleted. This public excerpt is
**not a runnable HTTPX checkout**.

Reproduce in a disposable full checkout of the pinned revision with recorded
dependencies. Commands include the complete faults and focused test source;
The exported interpreter prefix is redacted to `<ENV>`; adapt it locally. Fresh model experiments use
`benchmarks/run_httpx.py --profile decoder-audit` with explicit source, interpreter,
new output path and committed skill revision. Original model evidence is not
replaced by author replay. Featured graphs and their language variants remain
tied to their previous frozen experiment, not these development cells.
