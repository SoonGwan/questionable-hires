# Cachetools LRU audit01 — frozen before model execution

One new authored developer request over selected unchanged upstream cachetools
5.5.2 files, tag commit `c403f9f4185e58090b904c1915345b9ba46d5a08`.
The original MIT license is retained. `src/cachetools` is relocated to `cachetools`
for import from the fixture root; every selected file's Git blob and byte count
matches upstream. This is a source excerpt, not all upstream files/tests, a current
upstream bug report, or an independently held-out task.

Model task: audit four independent LRU regressions against two existing tests,
reporting all eight fault/test results and distinguishing actual behavioral errors
from setup failures. Requested behaviors and selection names are supplied; author
patches, witnesses and expected outcomes stay outside model inputs. Tools, grouping
and execution order are unrestricted within the audit scope. No requirement to
use the helper, an alternating schedule or a particular mutation spelling.

## Native preparation

Six source variants: unmodified, behavior-equivalent spelling, and four isolated
faults. Original/equivalent pass all15 upstream LRU tests and four extra behavioral
witnesses; each fault fails its distinct witness by assertion. Both selected
tests execute against each variant. An unhandled KeyError during an unchanged
test's cache access can be behavioral detection, not import failure merely because
unittest labels it ERROR. Review the actual phase and traceback.

Two author preparation mistakes are retained in this narrative: the first manual
test invocation used the repository root instead of fixture root and failed import;
the initial preflight incorrectly rejected every unittest ERROR, including genuine
behavioral KeyError. Fixes changed the author working directory/classification,
not upstream tests or expected behavior. Final two fixture checks pass Python3.9
and3.11. These author controls do not prove exhaustive fault/oracle completeness.

## Three original sessions

Freeze this generator/runner/protocol commit and prepared manifest before launching:

1. no-skill baseline;
2. prior Con Artist resource `51a4f5a`;
3. current Con Artist resource `b1875a0`.

GPT-6 Astra, medium,360 seconds/cell,n=1,serial. Current differs in batch normal
baseline caching, conditional documentation and unchanged applicable resources;
measure actual exposure/use rather than assuming adoption. Fixed order, shared host
and one task limit conclusions. The previous native37.5% process-count and36.1%
timing numbers are not expected model gains or acceptance criteria.

Use `run_cachetools_audit_01.py` to prepare once, inspect the source identities and
native preflight, then `--execute` once. Exclusive execution marker rejects a
second launch. Drift in task/resource/runner inputs rejects execution. Retain every
attempt, repair, timeout, incomplete outcome and usage; stop on account limits.
No favorable retries, replacement cells or excluded failures. No concurrent heavy
author tests during timed model execution. Frozen outputs/criteria are not edited
to fit model behavior.

Review all five frozen criteria and all eight actual outcomes, including surviving
faults. Verify mutation locality, unchanged tests, real copied imports/assertions,
reused observation origins, original file bytes/modes and owned-copy cleanup.
Do not count whole-suite completion or test count as sufficient. A meaningful
behavioral exception is not automatically setup failure; a later author's replay
cannot repair absent original evidence. Wrong/no meaningful fault is not coverage.

Account for full input+output tokens (cache once), elapsed process wall time and
all helper reads/extra checks. Report whole-task quality and scope alongside cost.
If the model groups by test selection or chooses native commands, the new cache
may offer no benefit; preserve that result. One favorable pair cannot establish
broad all-eight improvement or replace the featured graph. No release approval.

한국어: 실제 cachetools 소스·테스트에 새 감사 요청을 작성한 비교다. 도우미 사용이나
교차 실행을 강요하지 않고 무스킬·기존·수정 스킬의 전체 비용과 결과를 비교한다.
새 모델 세션 전 입력과 기준을 고정하며, 불리한 결과나 미사용도 그대로 남긴다.
