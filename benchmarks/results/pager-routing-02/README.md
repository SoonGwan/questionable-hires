# Support-first routing adopted; transfer remains unproven

[Preregistered diagnostic](../../PAGER-ROUTING-02-PROTOCOL.md), candidate/launch
`1cb854d`. One fresh Astra medium skill-only session on the unchanged, already
exposed pager task. One scheduled cell completes without transport errors,
test-authoring repairs, retries, exclusions or resource changes during timing.
This checks adoption after an observed routing defect; it is **not** a new
baseline comparison, independent holdout or featured benchmark.

| Observation | Earlier skill (`c6d8ea0`, screen 01) | Support-first skill (`1cb854d`) |
| --- | ---: | ---: |
| Input + output tokens | 78,649 | 56,368 |
| Full CLI seconds | 65.964 | 48.708 |
| Preparation shell commands | 3 | 1 |
| Total shell commands | 5 | 2 |
| Native suite executions | 1 | 1 |
| Native method outcomes | 2 pass, 2 fail | 2 pass, 2 fail |

The **28.33% lower tokens / 26.16% lower time** describe these two particular
skill sessions, not a causal estimate or general saving against no skill. Earlier
baseline is not reused as a contemporary control. Cached input is included once;
reasoning output is not added again. Task exposure, n=1, shared host/cache and
changed model test organization remain limitations. No favorable redraw follows.

한국어: 수정 후 새 세션은 기존 프로젝트 지원을 바로 사용했고, 불필요한
transport 자료를 읽지 않았다. 준비 명령은 3회에서 1회로 줄고 네 테스트의
요구 검증은 유지됐다. 수정 전 스킬 세션보다 토큰 28.33%·시간 26.16%가
줄었지만, 수정에 사용한 동일 과제의 단일 재검사다. 일반 성능 향상이나
스킬 미적용 조건 대비 효과로 확정하지 않으며, 다른 과제로 전이 검증이 필요하다.

## What actually changed

The first command reads supplied production/tests/support, AGENTS and the skill
entrypoint together. No filename inventory, native transport guide, transport
asset, disposable-probe or browser reference is read. The model explicitly
recognizes adequate existing response control and owned cleanup. The second shell
command runs native unittest after the captured test patch. There is no final
Git status/diff command, unlike screen 01; that omission contributes to the lower
command count and is not attributed to the support gate. Original-file integrity
is independently confirmed below, not presented as a model-run Git check.

The new model implementation uses shared ordinary assertion/overlap methods
instead of the earlier skill's duplicated overlap tests. No claim that the
wording caused that choice. Both implementations meet the same required state
checkpoints, actual request keys, pending-newer checks, success/error overlap and
latest-error/retry coverage. Both preserve the original success test. Both retain
real tuple assertions: cached rows with `loading=False` versus required `True`
while the latest request is still pending. Subtests allow the later success
checkpoint to be exercised without weakening the failed assertion. New native
execution has a 15-second subprocess bound versus the earlier skill's 20 seconds;
one-second fixture/task bounds and original support stay unchanged.

## Evidence and verification

The [model test](pager-loading-regression--skill--1/project/test_pager.py),
commands, native failures, answer, metadata and original events are retained.
Reviewed [tool records](pager-loading-regression--skill--1/tool-records.json)
contain both exact shell outputs/exits, matching CLI command records; all selected
calls have one matching response. Full private rollout remains local. The
verbose-header heuristic is again triggered by concatenated unittest subtest
headings, not demonstrated missing output: all four identities, two failure
traces and the native summary remain present.

[Separate author review](author-review.json) confirms unchanged production,
support/instructions, original success-test AST and installed resources, four
final project files, usage reconciliation and exact stored-output equality.
The retained suite reproduces two real failures on original code and four passes
with only the author-copy finalizer generation-guarded. Author copies are removed;
none of this rewrites the measured model result. Reproduce with
`python3 -B benchmarks/review_pager_loading.py --run benchmarks/local-runs/pager-routing-02 --output <new-json>`.

Keep this candidate for its observed routing adoption. Next evaluate new project
work and the absent/inadequate-support branch before claiming transfer or broad
efficiency. All earlier adverse outcomes and featured/localized charts remain
unchanged.

Post-run repository verification at source `1cb854d`: full local
`python3 -B -m unittest discover -s tests` passes **595 tests / 90.582s**, with
no reported skips. Skill metadata, eight-hire/local-link validation, featured
English/Korean synchronization and whitespace checks pass. The exported evidence
scan finds no local home/temp paths or checked credential markers. This is not
hosted CI, an exhaustive privacy audit or evidence of all-eight model efficiency.
