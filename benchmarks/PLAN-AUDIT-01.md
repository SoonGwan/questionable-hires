# Dependency-plan audit01 — scope transfer observed, efficiency still mixed

2026-09-21. Frozen launch`557a021`; prior Con Artist`740948e`, current`a3dee3b`
(entry change`e17e13d`; helper resources identical between these skill arms).
[Protocol](PLAN-AUDIT-01-PROTOCOL.md), [all six original attempts](results/plan-audit-01/),
[structured review](results/plan-audit-01/comparison.json).

Two requests over a fresh authored dependency planner, GPT-6 Astra medium,n=1,
serial fixed order, shared host/cache. Every scheduled session completed without
timeout or account-limit stop. No model-session retries, replacements or excluded
cells. One prior session repaired its own instrumentation; its entire cost remains.

## Complete task cost and review

| Request | Condition | Total tokens | Wall seconds | Native unittest processes | Other Python probes | Criteria |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Proposals | Baseline | 84,616 | 74.468 | 8 | 4 binding checks | 5/5 |
| Proposals | Prior | 76,424 | 84.041 | 12 | 0 | 5/5 |
| Proposals | Current | 74,975 | 72.247 | 8 | 4 behavioral observations | 5/5 |
| Verified | Current | 96,744 | 94.577 | 14 | 0 | 6/6 |
| Verified | Prior | 100,613 | 130.563 | 15 including repair | 0 | 6/6 |
| Verified | Baseline | 85,740 | 86.752 | 14 | 4 binding checks | 6/6 |

Tokens are full input+output, with cached input counted once. Process counts are
child test/probe invocations, not outer harness processes or model responses.
Prior proposal combines three correct stronger tests into one unittest process;
its three faulty stronger checks are separate. Counts are not coverage scores.

Current versus prior: proposal tokens−1.90%/time−14.03%; verified
tokens−3.85%/time−27.56%. Current versus **no skill**: proposal
tokens−11.39%/time−2.98%; verified **tokens+12.83%/time+9.02%**.
These individual pairs do not establish general superiority. Required evidence
was retained, but optional work, provenance instrumentation and a repair differ.

## What actual native evidence shows

All six attempts isolate the specified faults inside`plan`, preserve original
test bodies and demonstrate the same selected outcomes:

| Fault | Chain test | Cycle test |
| --- | --- | --- |
| Reverse successful order | Pass; length/membership ignore order | Pass; reversal not reached |
| Clear caller lists after building internal sets | Pass; input not inspected | Pass; mutation hidden by expected exception |
| Return partial order instead of cycle exception | Pass; acyclic path unaffected | Assertion failure: `ValueError not raised` |

Two successful correct-code observations are reused per completed matrix.
No setup failure is counted as mutation detection. All answers explain the gaps
and avoid claiming full-contract correctness.

For proposal-only, baseline/current give concrete unexecuted ordering and input
preservation assertions, including preservation after a cycle exception. Prior
executes additional stronger assertions. Current still runs four separate probes
showing outputs and mutated inputs; it has fewer unittest processes than prior,
**not fewer total child Python invocations**. Do not call every omitted optional
assertion a speed improvement on identical work.

For verified requests, all three conditions execute unchanged stronger checks
against correct/faulty copies for prerequisite order, acyclic input preservation,
and cyclic input preservation. The clearing fault still raises the expected
cycle exception and fails at the later graph-equality assertion. That is distinct
from the partial-return fault's missing-exception failure. Correct code passes.
Some tests additionally check list identity/alias contents; fault runs fail first
at equality, so those later checks have no independent detection observation.

## Provenance and repair differences

- Proposal baseline uses verbose same-process copied imports plus separate
  binding prechecks. Proposal current uses verbose native copied imports and
  direct known test imports, plus separate behavioral probes. Their separate
  processes are not same-process dispatch instrumentation.
- Both prior attempts and verified current use traces of actual calls into the
  copied function. Prior's first verified attempt omits the copy-root PYTHONPATH,
  so its hook does not load. The native correct chain test passes, then the harness
  rejects missing provenance and cleans copies. It repairs the environment and
  executes the full14-check matrix. Count15, not just the final14. The first pass
  is excluded from proof of the final matrix, **not from recorded resource cost**.
- Verified baseline has separate binding prechecks, not direct same-process import
  instrumentation. Actual native copied-test traceback paths, known unchanged
  direct imports, isolated source variants and their distinguishing outcomes
  support its review. This evidence is weaker than tracing each dispatched call;
  do not describe all arms as having identical provenance.

The prior repair contributes to the time/cost difference. This n=1 run cannot
attribute its absence in current to the entry edit. No session uses`audit.py` or
reads its guide; this is not evidence of the helper-cache optimization's adoption.
All four skill bodies are present initially and read again. Baselines have no
exact matching body observations; that alone is not proof of no other influence.

Original project bytes/modes, installed resources and HEAD remain unchanged.
Owned copies are removed; each delivery contains only its four initial files.
Pre-collection staged entries match the initial tree; the unavailable pre-session
binary index prevents a byte-identical-index claim.

## Capture and interpretation limits

26 shell outputs:21 exact matches and5 nonempty suffix matches, no unmatched
outputs. Original stored records retain the missing CLI prefixes: proposal
variant/command labels; verified baseline's first binding/command labels; and
the **entire first correct native result in the repaired prior verified matrix**.
That native result is present in original storage and used in review, not recreated
by an author replay. Private initial text/raw rollouts are not exported; redacted
tools and usage/exposure metadata are. The export scan is not a security certificate.

This is a fresh synthetic development transfer, not independent holdout or
real-project evidence. Two related requests,n=1, fixed order/shared host/cache,
unblinded review and unequal work limit interpretation. The narrower proposal
instruction remains reasonable provisionally, but the no-skill verified arm is
cheaper and faster. No new production edit, broad20–30% claim, featured-graph
promotion or release approval follows. Do not retune this exposed fixture for a
larger favorable number.

한국어: 새 과제에서도 제안과 실제 입증을 구분했고 필수 검증은 유지됐다. 수정
스킬은 기존보다 두 비용이 줄었지만, 입증 과제에서는 무스킬보다 토큰12.83%·
시간9.02%가 더 들었다. 기존 스킬의 출처 확인 설정 실패·복구 비용과 서로 다른
추가 작업을 모두 보존하므로 시간 차이를 지침 효과로 단정하지 않는다. 전체
성능 우위나 독립 검증 결과로 확대하지 않고 대표 그래프도 유지한다.
