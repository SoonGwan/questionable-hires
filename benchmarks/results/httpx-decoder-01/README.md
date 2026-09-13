# HTTPX decoder transfer: correct conclusions, higher skill costs

On a full HTTPX 0.28.1 checkout, both arms identify the same UTF-8 finalization
coverage gap and the existing split-CRLF protection. **Con Artist used 53.8% more
tokens and 14.4% more process time** by the equal-case ratio calculation. This is
an adverse resource result, not a success headline or a current-upstream bug report.

한국어 요약: 실제 HTTPX 고정 버전에서 두 조건 모두 올바른 핵심 결론을 냈지만,
스킬은 토큰 53.8%, 실행 시간 14.4%를 더 썼다. 여러 번의 모델 왕복과 수작업
복사·실행 작업이 관찰됐다. 이후 실행 선택 기준을 수정했지만 그 수정본의 모델
성능은 아직 측정하지 않았다. 불리한 결과를 숨기거나 대표 그래프와 섞지 않는다.

## Frozen experiment

[Protocol](../../HTTPX-DECODER-01-PROTOCOL.md), [manifest](run.json).
Actual upstream commit `26d48e0634e6ee9cdc0533996db289ce4b430177`; two new
author-selected audit requests, not maintainer-submitted tickets. GPT-6 Astra
medium, one session per task/arm, four sessions, sequential schedule with skill
cells first, 360-second deadline. All completed; none excluded or retried.
Requests were frozen at `051b81b`; Con Artist was frozen from that same revision.
Both arms used the full checkout, existing tests/configuration, and the same
preinstalled interpreter. Exact dependencies and resource hashes are in the manifest.

## Every measured cell

Tokens = total input, including cached input once, + output. Time = whole model
process. Interpreter/cache/scheduling effects are not eliminated.

| Task | Arm | Tokens | Cached input | Seconds | Core execution |
| --- | --- | ---: | ---: | ---: | --- |
| Split CRLF | [baseline](line-crlf-split--baseline--1/answer.md) | 112,686 | 92,160 | 73.774 | Correct 40 pass; faulty 39 pass / 1 fail |
| Split CRLF | [skill](line-crlf-split--skill--1/answer.md) | 152,847 | 130,304 | 87.591 | Correct 40 pass; faulty 39 pass / 1 fail |
| UTF-8 finalization | [baseline](text-finalization--baseline--1/answer.md) | 168,352 | 142,848 | 95.138 | Existing 40/40 both; focused 6 pass → 3 fail / 3 pass |
| UTF-8 finalization | [skill](text-finalization--skill--1/answer.md) | 289,351 | 260,736 | 104.648 | Existing 40/40 both; focused 6 pass → 3 fail / 3 pass |

Average the two skill/baseline ratios equally, then subtract one: token increase
53.7562%; time increase 14.3624%. This is not a causal estimate with n=1, differing
orchestration/provenance checks and an order that puts both skill cells first.

## What was verified

- Both UTF-8 arms change only `TextDecoder.flush()`'s final flag from true to false.
  Existing decoder tests survive. Both focused tests cover incomplete UTF-8 at EOF
  and a valid euro sign split across chunks, synchronously and under asyncio/trio.
  All three incomplete-input variants fail on the mutant, while valid controls
  pass. Baseline asserts chunk lists; skill asserts concatenated text, so they are
  not completely identical assertions. See [baseline witness](witnesses/baseline_utf8.py)
  and [skill witness](witnesses/skill_utf8.py).
- Both CRLF mutations produce an extra empty line at the same existing assertion,
  `tests/test_decoders.py:339`, with normal unsplit CRLF preserved. Baseline replaces
  carried CR with LF; skill disables trailing-CR deferral. These are distinct
  narrow faults with the same observed selected consequence. Neither demands an
  unnecessary stronger test after existing protection is demonstrated.
- Each final project snapshot preserves all **125 upstream tracked files** byte
  for byte. Installed skill resources are unchanged. No dependency installation
  or upstream mutation was observed. Final snapshots alone cannot prove every
  transient action; actual commands and hash checks were also reviewed.
- Skill verifies imports and actual caller bindings in pytest's test process.
  Baseline primarily verifies copied imports in separate diagnostic processes;
  that provides weaker test-process provenance. Do not call the work identical.
- Retained baseline CRLF copies and both UTF-8 focused suites were replayed after
  all model sessions ended, with 30-second subprocess caps. Counts match the table.
  The skill CRLF copy was removed by that session; its exact selected fault was
  separately exercised through the current helper. These are author checks,
  excluded from model metrics, not additional independent model observations.

The pre-model author oracle is also separate evidence. [Final oracle](author-oracle.json)
shows the missing-finalization fault survives 40 tests but fails the EOF witness;
the CR→LF fault is killed by the existing CRLF assertion. Both normal controls
pass. [Preliminary oracle](author-oracle-preliminary.json) initially used a lone-CR
boundary rather than the requested split CRLF. It was corrected before model
execution; both records are retained. This is preflight correction, not a model
retry or selection of a more favorable measured cell.

## Execution costs and capture limitations

All four sessions wrote copy-based orchestration instead of using the optional
helper. The skill split work into more commands and explicit provenance checks;
baseline more often grouped phases into one script. Skill's UTF-8 run also tried
unavailable `coverage` once, then successfully used installed pytest. Baseline's
UTF-8 script initially failed an exact interpreter-path spelling assertion and
repaired it. All this work remains included in usage/time.

Skill CRLF `item_8` and skill UTF-8 `item_12` have empty output from file edits.
Decisive pytest outputs are retained; some captured output is a tail rather than
every verbose line. No complete-capture guarantee or superiority score is claimed.
Shared host/cache, one repetition, unequal orchestration, public-model familiarity
and author-selected tasks limit generalization. No additional heavy regression
work was run alongside the model timing window.

## Subsequent improvement: routing, not a claimed measured win

Revision `22389f3` makes the existing helper the preferred path **after** a Python
audit has selected disposable-copy isolation and its limits fit. Adequate native
audits and simpler valid in-memory substitutions still take precedence. This aims
to avoid rewriting copy, subprocess and cleanup code and issuing separate model
round trips for standard phases. Unsupported projects must not be forced into it.

An author-only CLI replay confirms the helper can perform the CRLF audit's two
phases in one invocation and the UTF-8 audit's four phases in one invocation,
including the actual skill-generated six-case witness. Exit/count outcomes match
the table; no phase timed out or truncated its output. This proves compatibility,
**not model token or time improvement**. A new frozen model comparison is needed.

That replay also highlighted a diagnostic pitfall: importing pytest test modules
before pytest collects them bypasses assertion rewriting. The reference now tells
users to list implementation modules, not selected pytest test modules, in the
helper's import checks. Let pytest collect its own tests. The source is unchanged;
this is interface guidance, not an unmeasured claim that all runner semantics are
automatically verified.

Post-change local regression: **274 repository tests passed in 41.058 seconds**.
Skill schema, repository catalog/links and featured-language/chart sync checks
passed. These checks ran after the model timing window and do not measure model
performance of the routing change.

## Compact evidence and reproduction

This export is intentionally **not a runnable full HTTPX checkout**. Each cell
retains metadata, command/output events, answer, source-log digests, the original
decoder/test file and HTTPX's BSD-3-Clause `LICENSE.md`. Full duplicate project
copies and bulk generated diffs remain in ignored local storage, recoverable;
they were not deleted. Answer links to non-exported workspace directories point
to the corresponding command log. No observation or measured value was removed.

To replay, obtain the exact upstream commit, preserve its license, use the recorded
dependency environment and reconstruct the isolated mutation from `commands.json`.
The focused witnesses can be copied into that disposable checkout's `tests/` and
run with pytest. The project snapshot excerpts alone lack required package files.
Do not run mutations against a working production checkout.

For a fresh model experiment, use `benchmarks/run_httpx.py --profile decoder-audit`
with explicit source, Python, new output directory, arms/repeats and the intended
committed `--skill-revision`. Later resources do not reproduce this frozen run.
No changes were submitted to HTTPX, and existing featured charts remain unchanged.
