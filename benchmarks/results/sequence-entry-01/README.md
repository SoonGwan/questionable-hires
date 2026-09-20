# Sequence entry pilot 01: verification succeeds, efficiency does not

2026-09-21. Launch `031b961`; Receipt resources `9f0cd19`.
[Frozen protocol](../../SEQUENCE-ENTRY-01-PROTOCOL.md),
[task and unchanged extracted sources](../../sequence-entry-case-01.json),
[execution manifest](run.json), [reviewed comparison](comparison.json).

Two fresh GPT-6 Astra medium sessions, baseline then skill, n=1. Both completed
without timeout or account limit; no replacement, retry or excluded cell. This is
one known issue extracted from this repository, with authored history/instructions,
not an untouched external project or held-out generalization test.

| Arm | Total tokens | Process seconds | Recorded responses | Full task/scope |
| --- | ---: | ---: | ---: | --- |
| No skill | 92,431 | 76.357 | 4 | pass |
| Receipt | 129,866 | 87.738 | 5 | pass |

Receipt uses **40.50% more tokens and 14.90% more time**. This is not an accepted
efficiency win. Input includes cached input once; output includes reasoning where
reported. Recorded response counters and original CLI totals reconcile in both
arms. Shared serial host/cache, one pair and differing setup work preclude causal
attribution, significance or general percentages. No featured chart is changed.

## Actual execution and review

Both retain the same two current test files, load exactly the eight selected test
identities through unittest, and execute the real copied component. Before revision
`7a5c5b0ba9ff661624ec8dd7242563905a8d7b38` has four 0.5-second async entry-wait
errors at `entered.get()` and four passing controls. After revision
`a8d15369e7d70d98b16f9008e89c2b70eab24d2d` passes all eight, with no skips. These
are fixture commit identities, not the original repository's source commits.
Neither mistakes missing imports/setup for defect reproduction.

- Baseline makes four shell commands in three tool interactions, then the final
  response. It writes no harness file: an in-memory runner asserts the test modules
  and dynamic `probe.__file__` belong to each copy, checks the exact suite identities,
  runs both revisions, reports each native exit and verifies its whole-tree snapshot
  including Git plus final status. Both copies are cleaned.
- Receipt makes five shell commands in four tool interactions, then the final
  response. It reads the existing-fix guide, searches helper implementation for
  import/copy behavior, and explicitly decides that module-only import checks do
  not establish the required dynamic `probe.__file__` attribute. It then writes an
  in-memory native comparison instead of invoking the helper. Actual process PIDs,
  component paths/hashes, selected identities/counts, native exits and no process
  timeout are reported. Its 78-entry inventory includes installed skill files and
  Git; diff/status checks and owned-copy removal pass.

The exact fixed-file hashes match the frozen task in both runs. All project bytes
and 0644 modes, HEAD and installed resources remain unchanged; exported final
snapshots have no extra files. Native command evidence includes full Git-state
inventories before/after execution; collector-side index changes are separately
identified by the runner's pre-collection metadata. All five frozen criteria are
marked passed by unblinded author review of commands and outputs, not just answers.

The additional helper-compatibility inspection is an observed cost contributor,
not proof it caused the entire token/time difference. A useful next boundary is
making dynamic-module provenance capability/limits clearer or supplying suitable
optional support. Any such change needs its own correctness tests and a different
task; do not keep retuning this exposed issue or promise a measured gain in advance.

## Capture and exposure

One CLI output in each arm omits a prefix. Matching original stored tool records
recover baseline `item_5`, line33 (four interpreter/test-hash lines), and Receipt
`item_6`, line39 (five interpreter/revision/test-hash/command lines). After that
prefix, outputs and exits match exactly; every other command matches in order.
No execution was repeated to recover output. Both original CLI captures and
selected stored tool records are retained, with omissions disclosed rather than
silently rewriting the original streams.

Receipt's exact entry body is observed in the initial message and a later tool
read. Baseline has no observed exact Receipt body; this is not universal proof
that all possible contextual influence is absent. Per-cell exposure records state
that limitation. Full private rollouts and initial instructions remain local;
exported selected records are path-redacted and the privacy-pattern scan is clear.

한국어: 두 실행 모두 동일한 실제 테스트 8개로 수정 전 오류 4개와 수정 후 통과를
확인했고 원본·Git 상태·정리를 지켰다. 하지만 Receipt는 토큰 40.50%, 시간
14.90%가 더 들었다. 도구의 동적 모듈 경로 검증 가능 여부를 추가 확인한 뒤 별도
네이티브 코드를 작성한 과정이 관찰됐다. 기능 경계 개선의 단서이지 전체 비용의
원인 확정은 아니다. 불리한 결과를 그대로 남기며 대표 그래프는 유지한다.
