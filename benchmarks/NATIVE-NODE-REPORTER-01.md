# Native Node display prototype — 2026-09-21

Decision: **do not adopt as the default skill workflow**. This is an author-native
feasibility experiment, not a model benchmark or a performance improvement.
Production skills and featured graphs remain unchanged.

The [prototype](prototypes/native_node_reporter.mjs) consumes Node's native test
events while a second native reporter writes full TAP from the **same execution**.
It does not parse TAP, run tests again, modify native exits or certify correctness.
Node documents this mechanism under [multiple and custom reporters](https://nodejs.org/docs/latest-v24.x/api/test.html#multiple-reporters).
Local measurements use Node **24.16.0**, not a claim about every Node version.

## Both original observations

| Authored fixture | Native exit | Actual test executions | Full TAP bytes | Display bytes |
| --- | ---: | ---: | ---: | ---: |
| 24 repeated assertion failures | 1 | 24 | 22,663 | 14,161 |
| 24 passing assertions | 0 | 24 | 2,534 | 8,256 |

The failure display is 37.5% smaller; the passing display is **3.26 times larger**.
These are UTF-8 byte counts, **not tokens, latency, billing or task-level savings**.
Each fixture executes once, confirmed by an append-only invocation marker. The
failure and passing fixtures differ only in the assertion's actual value. They
are author-selected examples, not an independent holdout or realistic task mix.
Absolute path lengths and runtime diagnostics also affect sizes.

[Published original observations and redacted outputs](results/native-node-reporter-01/manifest.json)
include both cases, native source, command, exit, TAP and displayed JSONL. The
manifest separates original-byte hashes/counts from published-byte hashes/counts.
Workspace paths are replaced with `<WORKSPACE>`, the Node executable with `<NODE>`,
and published nonempty files have
a final newline. Empty stderr files are recorded but omitted. Observation JSON's
hashes and table sizes refer to original, unredacted output. The passing run's
original limitation text mistakenly says “repeated-failure fixture”; `failures: 0`,
source and exit identify the passing control. That historical record is preserved;
the profile script now describes both variants correctly.

## Boundaries and local checks

- Native summaries, individual result identities, skip/todo flags and failure
  previews are retained. The compact view omits stacks, actual/expected values and
  diagnostics; full TAP remains necessary for diagnosis.
- First 200 result events and first 500 characters per preview are displayed;
  omissions/truncations are explicit. Distinct omitted failures are not recoverable
  from the compact view alone. A missing global summary is incomplete, not success.
- Seven checks cover repeated failures/exactly-once execution, passing overhead,
  nested skip/todo/diagnostics, syntax failure, native cancellation, display limits,
  and an absent global summary. Checks require Node 24; other versions skip with
  an explicit reason rather than implying compatibility.
- An initial unresolved-test fixture without a native deadline reached the author's
  10-second subprocess limit. No leftover matching processes were found. The
  fixture was corrected to request a 50ms native timeout, then verified as a
  cancellation/failure. The reporter provides **no deadline or process cleanup**.
- Caller owns fresh destinations, full raw retention, input identity, exit capture,
  timeout/child cleanup and sensitive-output handling. This is not an attestation
  wrapper, security boundary or replacement for existing capture helpers.

Reproduce in **new** output directories (existing paths are rejected):

```sh
python3 -B benchmarks/profile_native_node_reporter.py --output benchmarks/local-runs/native-display-fresh-fail
python3 -B benchmarks/profile_native_node_reporter.py --output benchmarks/local-runs/native-display-fresh-pass --passing
python3 -B -m unittest discover -s tests -p test_native_node_reporter.py -v
```

Next candidate must avoid the normal-case display expansion without discarding
decisive diagnostics, and account for wrapper/read overhead. Only then is a fresh
whole-task model comparison justified. This experiment does not justify adding
more default skill instructions or claiming the old model-token gap is solved.

한국어: 실패 로그는 작아졌지만 정상 통과 로그는 약 3.3배로 늘었다. 기본 스킬에
채택하지 않으며 두 결과를 모두 보존한다. 바이트 크기 비교일 뿐 토큰·시간 절감이나
전체 성능 개선의 증거가 아니다. 실제 개선이 확인되지 않아 대표 그래프도 유지한다.
