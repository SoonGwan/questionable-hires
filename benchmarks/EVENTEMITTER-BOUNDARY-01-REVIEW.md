# EventEmitter boundary 01 — no candidate efficiency improvement

2026-09-21. Launch `ed74b11`; prior resource `716ef88`; candidate `89c5172`.
[Frozen protocol](EVENTEMITTER-BOUNDARY-01-PROTOCOL.md),
[all six original attempts](results/eventemitter-boundary-01/run.json),
[reviewed criteria and capture correspondence](results/eventemitter-boundary-01/comparison.json).

## Reviewed results

| Task | Arm | Criteria met | Total tokens | Wall seconds | Final native tests |
| --- | --- | ---: | ---: | ---: | ---: |
| Reentrant once | Prior | 5/5 | 139777 | 95.019 | 25 passed |
| Reentrant once | Baseline | 5/5 | 112623 | 93.827 | 42 passed |
| Reentrant once | Candidate | 5/5 | 141489 | 121.331 | 25 passed |
| Empty-event removal | Candidate | 5/5 | 127564 | 57.385 | 8 passed |
| Empty-event removal | Baseline | 5/5 | 89939 | 55.497 | 6 passed |
| Empty-event removal | Prior | 5/5 | 104756 | 51.028 | 7 passed |

All six scheduled attempts completed without timeout or account limit. Token totals
include cached input, output, every resource read, failed check and rerun. Test
counts are not a quality ranking: the suites contain different parameterizations.
Each reviewed task meets its five frozen criteria; this is not exhaustive proof.

Candidate uses more tokens and wall time than both prior and baseline on **both**
tasks. It establishes neither a correctness advantage nor an efficiency gain here.
Reject promotion of this candidate on this evidence. Production skills and featured
charts remain unchanged. No favorable reruns or replacements were performed.

## What the original attempts checked

Reentrant deliveries track consumption on the actual registration and remove by
identity. They cover nested single/multiple-listener paths, caught/propagated exact
errors, distinct duplicate registrations, fresh registrations, ordinary snapshots,
context/payload identity, symbols and instance isolation using the actual local
module. All keep the supplied smoke test unchanged. Candidate and baseline also
directly test an unconsumed duplicate surviving another duplicate's exception.

The prior first recorded 21 failures out of 25 against the unchanged implementation,
then 25 passes after the fix. Candidate recorded 20 failures out of 24, then 24
passes, added another test and recorded 25 passes. Baseline implemented before its
single recorded 42-test passing run. These are unequal verification paths; prior
and candidate's extra before-fix evidence is not free and is not subtracted.

All empty-event deliveries make the same one-line change to distinguish undefined
from a specific event, with native assertions for empty/absent selection, retained
string/symbol siblings, fluent results, counts/names and reuse. Before/after native
results were prior 3 failures of 7 → 7 passes, baseline 2 of 6 → 6 passes, candidate
3 of 8 → 8 passes. No initial test, license or instruction file was changed.

## Capture and scope limits

All usage totals reconcile with original same-session records. Of 32 shell outputs,
28 have unique exact correspondence. The prior/candidate reentrant before-fix
outputs were truncated in the original capture; their native identities and failure
summaries are visible, but full diagnostic text was not delivered there. Two empty
successful candidate cleanup outputs are ambiguous to the text matcher. They remain
ambiguous, not relabeled as exact matches. Final native passing summaries are present
in the original records. Neither missing text nor a later replay repairs a transcript.

Scope inspection verifies unchanged initial test/license/AGENTS bytes, original file
modes, HEAD, installed resources and pre-collection index entries matching the initial
tree. A pre-session binary index was not captured. All delivered changes are local
implementation/tests. Public exports retain answers, source, edits, original tools,
usage and exposure records; private initial instructions/rollouts are excluded.
Privacy-pattern scanning passes, but is not a general security certification.

## Author reference limitation discovered during review

The frozen author correction marks once registrations consumed but still removes
all same-function once registrations together. If one duplicate throws, an unconsumed
sibling is lost. The original oracle's simple duplicate-count check missed this.
The model deliveries instead remove by registration identity and preserve the sibling.

A [separate native probe](probe_eventemitter_duplicate_gap.py), run only after all
timed sessions ended, [records](results/eventemitter-boundary-01-author-gap.json)
one remaining registration and two eventual calls for all three model deliveries,
versus zero remaining and one call for the frozen author reference. The probe checks
local module binding, exact error propagation and actual counts. It is supplementary
author evidence, not another model run. A Python regression rejects the frozen
reference and accepts identity removal on the same native check (3.9/3.11 pass).
Original tasks, references, controls and model outputs are retained unchanged.

## Interpretation

Two author-selected tasks on a pinned real-project source excerpt, n=1, fixed order,
shared host/cache and unblinded review cannot establish causality or all-eight skill
performance. Tests are authored, not the upstream suite; synchronous dispatch does
not prove async cleanup coverage. This run supports not adopting the narrow guidance
change for efficiency, not a general assertion that all skill use is harmful.

한국어: 원본 6세션은 모두 정해 둔 요구사항을 만족했지만, 수정 후보는 두 과제에서
기존 스킬·무스킬보다 토큰과 시간이 모두 늘었다. 따라서 이 후보를 채택하지 않는다.
작성자 사전 대조 코드에도 중복 등록과 예외를 함께 다루지 못한 누락이 있었으며,
세 모델 제출물은 해당 추가 검사에 통과했다. 불리한 비용·출력 잘림·대조 코드의
한계를 모두 공개하고 기존 그래프나 원본 결과를 덮어쓰지 않는다.
