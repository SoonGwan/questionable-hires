# Native pager regression: useful coverage, no overall efficiency win

[Frozen protocol](../../PAGER-LOADING-01-PROTOCOL.md), launch `fa3c10d`,
Mother-in-law entrypoint `c6d8ea0` (resources from `9c91241`). One authored task,
one fresh session per arm, Astra medium, serial skill then baseline. Both complete;
no author reruns/exclusions or resource changes during timing.

| Arm | Input + output tokens | Seconds | Shell commands | Native result |
| --- | ---: | ---: | ---: | --- |
| Baseline | 89,681 | 61.057 | 5 | Four methods, two passing, two failing subtests |
| Skill | 78,649 | 65.964 | 5 | Four methods, two passing, two failing subtests |

**−12.30% tokens, +8.04% time.** Cached input is included once; reasoning output
is not added again. This is not an overall win. Baseline also records a WebSocket
reconnection event, retained in its logs and costs. Do not attribute that event
or the difference to the skill. n=1, shared host/cache, task authorship and the
different test organization further limit causal/general inference.

한국어: 양쪽 모두 요구된 회귀 테스트를 정확히 작성했지만, 스킬은 토큰 12.30%
감소·시간 8.04% 증가로 전체 효율 목표를 충족하지 못했다. baseline의 연결
재시도도 원본 기록과 비용에 포함했다. 한 번의 합성 작업으로 일반 성능이나
인과 효과를 주장하지 않으며, 대표 그래프도 변경하지 않는다.

## Actual coverage and extra work

Both preserve the original single-success test and all production/support files.
Both reuse the existing project-owned request/cleanup fixture; no transport is
copied and no disposable probe runs. Added cases check older success and OSError
while a newer request remains pending, plus latest error/retry. Actual keys and
rows/loading/error are asserted at required transitions. Native tuple assertions
show `(['cached'], False, None)` instead of `(['cached'], True, None)` after stale
completion. Subtests allow newer completion to be checked after that failure;
they do not continue past a failed entry that never produced a response handle.

Each suite runs once, with no test-authoring repair. Baseline shares state and
overlap helpers, adds initial-state checks and performs `git diff --check`.
Skill duplicates the two overlap methods (93 added lines versus baseline's 67),
uses direct assertions, and adds a 20-second subprocess deadline. Both use the
same native interpreter with bytecode writes disabled and one-second fixture/task
waits. These are not identical implementations or all identical extra checks.

Skill's second shell command reads the native transport guide **and the unused
transport asset**, despite supplied equivalent project support. Both arms first
inventory the four known project files and later read AGENTS in a separate call.
The skill correctly avoids the disposable-probe/browser references, but existing
support is checked too late to prevent the unnecessary transport reads. This is
a concrete routing defect to address, not a numerical causal decomposition.

## Original evidence versus author replay

Exports include original events, commands, final tests, diffs, metadata and
reviewed same-session [tool records](pager-loading-regression--skill--1/tool-records.json)
for both arms. All five shell outputs/exits per arm match their persisted tool
responses exactly. No missing, duplicate or unmatched selected tool records.
The CLI's verbose-header heuristic flags two headers versus four methods because
unittest subtest failures concatenate method headings; actual outputs retain all
four names, both failure traces and the four-test/two-failure summary. This flag
is not established capture loss. Full rollout context remains local, not exported.

[Separate author review](author-review.json), reproducible with
`python3 -B benchmarks/review_pager_loading.py --run benchmarks/local-runs/pager-loading-01 --output <new-json>`,
confirms unchanged original test AST, source bytes, four-file final inventory,
installed resources and usage reconciliation. Unmodified model suites each
reproduce the two real failures in disposable project-local copies; changing only
the production finalizer to generation-guarded loading yields four passes each.
No model artifact is repaired and no author replay replaces original evidence.
All author scratch is removed. These checks establish the scoped regression,
not browser behavior, all interactions or broad efficiency.
