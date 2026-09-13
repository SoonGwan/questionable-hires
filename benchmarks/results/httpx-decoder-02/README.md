# HTTPX routing recheck: helper adopted, token objective unmet

Con Artist used the copy-audit helper in both new skill sessions. Against the
contemporary baseline it used **32.0% more total tokens and 15.1% less process
time** (equal-case mean ratios). Both arms reached the correct core conclusions.
This is not an all-metric efficiency win or broad confirmation.

한국어 요약: 실제 HTTPX 고정 버전의 두 개발용 과제를 다시 비교했다. 스킬은
두 세션 모두 helper를 사용했고 시간은 15.1% 줄었지만 토큰은 32.0% 늘었다.
발견한 테스트 파일 생성 오류를 줄이는 기능을 추가했으며, 그 기능의 모델 비용
개선 여부는 아직 측정하지 않았다. 이전 불리한 결과도 그대로 보존한다.

## Frozen comparison

[Protocol](../../HTTPX-DECODER-02-PROTOCOL.md), [manifest](run.json).
HTTPX commit `26d48e0634e6ee9cdc0533996db289ce4b430177`, full checkout,
same installed dependencies; Con Artist revision `22389f3`. GPT-6 Astra medium,
two already exposed author-selected tasks, one repetition, four fresh sessions,
serial execution, 360-second limit. All completed; no cell retries or exclusions.
Preflight: 40 decoder tests pass. Skill-first scheduling and shared caches remain
confounders. No heavy author regressions ran during the model timing window.

| Task | Arm | Total tokens | Cached input | Seconds |
| --- | --- | ---: | ---: | ---: |
| Split CRLF | [baseline](line-crlf-split--baseline--1/answer.md) | 141,664 | 109,056 | 81.919 |
| Split CRLF | [skill](line-crlf-split--skill--1/answer.md) | 178,033 | 149,504 | 58.799 |
| UTF-8 finalization | [baseline](text-finalization--baseline--1/answer.md) | 169,371 | 131,456 | 96.305 |
| UTF-8 finalization | [skill](text-finalization--skill--1/answer.md) | 234,303 | 205,312 | 94.381 |

Total tokens = input (cached included once) + output. Average the two
skill/baseline ratios equally, then subtract one: +32.0049% tokens, −15.1104%
time. The [earlier comparison](../httpx-decoder-01/README.md) remains adverse;
its baseline differs, so historical changes are not paired causal estimates.

## Actual evidence and unequal work

- Both CRLF arms replace carried CR with LF in an isolated copy. Existing tests
  go from 40 pass to 39 pass / 1 fail at `tests/test_decoders.py:339`. Unsplit
  normal-control assertions pass before the failing split assertion. Baseline
  also performs separate diagnostics. Skill's conditional stronger probe is
  **skipped** because the existing tests kill the fault; its caller-binding
  assertions therefore do not count as executed evidence. The helper's actual
  test-process implementation import checks do execute.
- Both UTF-8 arms turn off the final decode flag in `TextDecoder.flush()`.
  Existing tests remain 40 pass on both implementations. Baseline focused tests
  go from 6 pass to 3 fail / 3 pass. Skill focused tests go from 8 pass to 4 fail /
  4 pass, including redundant synchronous parametrization across both async
  backends. Incomplete-input EOF assertions fail; valid split-input controls pass.
  Skill checks actual caller binding in the focused test process. Coverage and
  orchestration are not identical; larger test counts are not credited as wins.
- Skill UTF-8 first fails probe collection with a SyntaxError caused by byte
  escapes inside nested source strings, then repairs the recipe and reruns the
  helper. Baseline UTF-8 first fails a literal interpreter-path assertion, then
  repairs it. All internal repairs remain in measured costs and command logs.
- All four final snapshots preserve all 125 upstream tracked files byte for byte.
  No upstream patch or dependency installation was made. Skill references/helper
  source are inspected repeatedly, so helper adoption alone does not eliminate
  model overhead. Final snapshots cannot prove every transient action.

Baseline UTF-8 `item_5` has empty output from directory creation; decisive pytest
outputs are retained. Clear capture diagnostics do not guarantee every verbose
line was captured. One repetition, exposed tasks, differing assertions and
provenance work limit generalization. These are not maintainer-submitted tickets
or newly discovered current-upstream bugs.

## Implemented follow-up, not yet a model-performance result

Revision `89d91af` adds `probe_files` and `probe_tests` to the audit helper.
Tests requiring native pytest/unittest collection can supply new test files
directly, avoiding Python source nested inside another Python source string.
JSON escaping still applies. New files exist only in fresh probe copies, never
in existing-test phases or the original project. Validation rejects overwrites,
traversal, colliding paths and ambiguous modes; batch reuse includes file content
and test arguments in its identity. Existing inline probes remain supported.

[Author replay](native-files-author-replay.json) converts the actual successful
skill-generated HTTPX witness to this interface. Existing tests: 40 pass on both;
focused tests: 8 pass on correct, 4 fail / 4 pass on mutant. Caller-binding checks
execute and originals remain unchanged. This is compatibility/behavior evidence,
**not another model session or a token/time saving**. Full local regression after
the feature: 280 tests pass in 44.559 seconds, including six new interface tests.
Skill schema, catalog/links and featured-language sync checks also pass.

## Evidence and reproduction

This compact export is not a runnable full checkout. Each cell retains metadata,
commands, events, answer, source-log hashes, original decoder/test excerpts and
HTTPX's BSD-3-Clause license. The baseline focused test is retained under
`text-finalization--baseline--1/project/.decoder-finalization-audit/`.
Full exported project copies and diffs remain in ignored local storage; they were
not deleted. Two CRLF answer links were adjusted to exported project paths only.

Clone the pinned upstream revision into a disposable directory, recreate the
recorded dependencies, and reconstruct recipes from command logs. Historical
interpreter paths must be adapted to that environment. The author replay includes
its new-interface recipe, but requires `89d91af` or later; it cannot reproduce the
older frozen skill interface. Fresh model runs use `benchmarks/run_httpx.py
--profile decoder-audit` with explicit source, interpreter, unused output path and
committed skill revision. No featured graph or broad success claim is updated.
