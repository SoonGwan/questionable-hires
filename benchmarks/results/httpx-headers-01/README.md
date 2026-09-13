# Header transfer: batch reuse works, token objective still unmet

Con Artist uses the context collector, reads back indexed test bodies, and runs
both faults through one batch audit. Required core outcomes are correct, but
**total tokens increase 35.1% and process time decreases 14.9%** against the fresh
baseline. This new two-boundary task does not establish broad efficiency.

한국어 요약: 다른 HTTPX 기능에서도 색인 후 본문 확인과 배치 재사용은 실제로
작동했다. 그러나 토큰은 35.1% 늘고 시간은 14.9% 줄었다. baseline도 정상
테스트를 한 번만 실행했으므로, 재사용 기능 자체를 상대적인 절감 성과로 세지
않는다. 별도 import 검사와 baseline의 경로 오류 수정 등 차이를 함께 기록한다.

## Frozen experiment

[Protocol and author preflight](../../HTTPX-HEADERS-01-PROTOCOL.md),
[manifest](run.json). Full HTTPX
`26d48e0634e6ee9cdc0533996db289ce4b430177`, Con Artist `a2b6258`, GPT-6 Astra
medium. One new author-selected request containing two separate contracts, one
repetition per arm, serial skill-first schedule, 360-second limit. Not a
maintainer-submitted ticket or independent multi-project holdout. Preflight 27
tests pass. Both model sessions complete; no cell retries or exclusions. Author
oracle code/results stay outside the evaluated projects.

| Arm | Total tokens | Cached input | Seconds | Shell commands |
| --- | ---: | ---: | ---: | ---: |
| [baseline](headers-two-boundaries--baseline--1/answer.md) | 150,896 | 122,752 | 83.847 | 6 |
| [skill](headers-two-boundaries--skill--1/answer.md) | 203,849 | 175,744 | 71.318 | 7 |

Total = input (cached included once) + output. Skill/baseline minus one:
+35.0924% tokens, −14.9427% process time. Two faults are not two independent
model tasks. Shared cache, order, n=1 and unequal preparation/provenance limit
interpretation. Previous unfavorable cases remain intact.

## Required execution

Both model arms choose the same faults, independently in separate copies:

- Remove lookup-key `.lower()` in `Headers.__getitem__`: 1 fail / 26 pass.
  `test_headers.py:31` expects `h['A'] == '123'`; actual `KeyError('A')` comes
  from broken case-insensitive lookup, not support-code failure.
- Reverse values only in `get_list`'s default unsplit branch: 2 fail / 25 pass.
  Lines 16 and 163 expect `['123', '456']` and `['a, b', 'c']`, respectively;
  actual lists are reversed. The embedded comma remains unsplit. This differs
  from the author's preflight truncation fault; neither original record is changed.

Correct existing suite: 27 pass. Both arms verify lowercase single-value indexing
and default list retrieval on correct code and each fault. Control payload text
differs (`plain` versus `ordinary`), not the tested contract. No additional
mutation or new production test is demanded for these detected faults.

## Actual reuse and context decisions

Skill selects the constructor and two method definitions directly. The large
test file returns `definition_index`, followed by an actual read of its first
280 lines, covering the detecting assertions and tests. The session also reads
module setup, autouse fixture/concurrency support, exports and helper source.
Thus automatic-index use and relevant body readback are observed; the index is
not itself credited as assertion inspection or execution evidence.

The batch helper executes six phases: one correct suite, one correct control,
two mutant suites and two mutant controls. Second-fault correct observations
refer explicitly to the first observations; they are not independent executions.
Copied imports are checked in the actual phase processes, with public/internal
class identity and method-file provenance in the control probes. No repair is
observed in the skill session.

Baseline also executes its correct suite/control only once. Its custom runner
adds three separate import-provenance processes (nine total child checks versus
six), and uses pytest for each normal control. Those control tests check the
copied package path in their own process but not the skill's explicit class and
method identities. Baseline initially fails a literal interpreter-path assertion,
repairs it to compare resolved paths, then runs successfully. All repair costs
remain included. Neither reuse alone nor lower raw time proves equivalent-work
savings; provenance work and runner setup differ.

Both stay within the permitted project, with no dependency installation or
upstream modification observed. The author compares all 125 upstream tracked
files in both final snapshots byte-for-byte: unchanged. Actual commands/model
integrity checks were also reviewed; snapshots alone cannot prove every transient
action. Skill removes its disposable copies; baseline retains its diagnostics.

Both capture diagnostics have no invalid JSON, empty command output, error-event
or rejected-patch flags. Decisive outputs are present and executed helper phases
report no timeout/truncation; reused entries are references, not missing passes.
Clear diagnostics do not guarantee every original tool output is complete.
No heavy author regressions run concurrently with model timing.
After model execution, all 297 repository tests pass in 39.670 seconds. Catalog,
local links, featured-language sync and export pattern checks pass. These do not
measure model utility or substitute for current hosted CI/release verification.

## Evidence and next decision

Compact exports retain command/output events, metadata, answers, source-log hashes,
original model/header-test excerpts and HTTPX's BSD-3-Clause license. Baseline's
runner and results JSON are retained; its directory answer link points to the
command log. Full exports/diffs remain recoverable in ignored storage, not deleted.
Interpreter prefixes are redacted to `<ENV>`. This is not a runnable full checkout.

Replay from the full pinned source with recorded dependencies and commands; adapt
interpreter paths. Fresh model runs use `run_httpx.py --profile headers-audit`
with explicit source/interpreter, committed skill revision and unused output path.

This confirms mechanisms in another function area, not overall token savings.
More repeated instruction tuning on these exposed HTTPX tasks is not sufficient;
broader developer workflows and the outstanding all-eight gate remain necessary.
No featured graph or universal improvement claim is updated.
