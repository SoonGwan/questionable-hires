# Qualified context selection: near token parity, broad goal unmet

Con Artist selects the requested definition instead of the full implementation
file. Against the new baseline: **3.2% more total tokens / 7.0% less process
time**. Required core outcomes are present, but a single exposed task, differing
provenance and baseline scope exception prevent broad or equivalent-work claims.

한국어 요약: 구현 파일 전체 대신 필요한 정의를 직접 선택했다. 새 baseline
대비 토큰은 3.2% 늘고 시간은 7.0% 줄었다. 토큰 절감이나 20~30% 개선을 달성한
결과는 아니다. 자동 색인 기능은 이번 모델 세션에서 사용되지 않았으므로 그
기능 자체의 효과로 수치를 돌리지 않는다.

## Frozen comparison

[Protocol](../../HTTPX-CONTEXT-02-PROTOCOL.md), [manifest](run.json).
Con Artist `3ff951f`, full HTTPX commit
`26d48e0634e6ee9cdc0533996db289ce4b430177`, unchanged task/dependencies/criteria.
GPT-6 Astra medium, two fresh sessions, one repetition per arm, serial skill-first
order, 360-second limit. Preflight 14 pass; both sessions complete with no retries
or exclusions. No heavy author work runs concurrently. Prior adverse runs remain
intact; their different baselines and faults are not paired causal comparisons.

| Arm | Total tokens | Cached input | Seconds | Shell commands |
| --- | ---: | ---: | ---: | ---: |
| [baseline](queryparams-repeated-values--baseline--1/answer.md) | 119,799 | 104,832 | 52.702 | 5 |
| [skill](queryparams-repeated-values--skill--1/answer.md) | 123,593 | 96,256 | 49.018 | 5 |

Total = input (cached included once) + output. Ratios minus one: +3.16697% tokens,
−6.99025% time. Shared cache, order and n=1 remain limitations.

## Actual source selection and execution

Skill performs initial scoped discovery, reads interfaces, then calls the context
collector with `tests/models/test_queryparams.py` and
`httpx/_urls.py:QueryParams.get_list`. The result contains the test in full and
the actual method body, **not** a large-file index. Original collector output is
17,018 characters. It subsequently reads autouse fixture/concurrency support,
module imports, the constructor region, public exports and helper lines 1–240.
No post-collector instruction-file search occurs. Needed body inspection is
visible, but helper trust inspection remains a cost. Whole-task savings cannot
be inferred from context length alone.

Both arms choose the same narrow mutation: reverse the actual returned list
with `[::-1]`. Correct tests: 14 pass. Mutant tests: 5 fail / 9 pass at
`tests/models/test_queryparams.py:24`, actual `['456', '123']`, expected
`['123', '456']`. Both execute `get_list('b') == ['789']` on correct and faulty
copies and pass. No unnecessary stronger test or additional mutation is demanded.

Skill uses one helper call with fresh-copy phases, copied-import verification in
actual test/probe processes, and class-identity/method-path checks in its normal
probes. Baseline creates two copies and its own subprocess orchestration, checking
package imports in separate normal-control processes. Provenance differs. No
internal repair is observed. This shows protection against the selected ordering
fault, not every possible defect or a current-upstream bug.

Baseline's third command searches `..` outside the permitted project. No match
appears, but the attempted search is a scope exception. Skill stays scoped. All
125 upstream tracked files compare byte-identically in both final snapshots;
actual commands and model integrity checks were reviewed too. Final snapshots
alone cannot prove every transient action. No dependency installation is observed.

Both capture diagnostics have no invalid JSON, empty command output, error-event
or rejected-patch entries. Decisive assertion/control output is retained; helper
phases report no timeout/truncation. This is not a universal capture guarantee.

## Implemented capability versus measured behavior

`3ff951f` adds automatic indexes for Python files over 200 lines when the index is
smaller than full source, nested class/method locations, explicit omitted-body
labels and `--full` readback. Instructions/configuration remain complete. Fifteen
collector tests pass; all 296 repository tests pass in 45.423 seconds before model
timing. These are behavior/regression checks, not model-efficiency measurements.

Author CLI comparison on the same full-file selectors: compact serialized JSON
20,011 characters in automatic mode versus 39,919 with `--full`; the index retains
the method at lines 526–535. This omits bodies and requires follow-up reading,
so it is not equivalent-work token saving. The model instead used the existing
qualified-selector path with new guidance. Automatic-index adoption remains
unmeasured. Subsequent `a2b6258` clarifies that conditions inside omitted class
bodies are not exposed by the index; fifteen collector tests still pass. This
wording correction is outside the frozen model revision.

## Evidence and next step

Compact exports retain commands/events, metadata, answers, source-log hashes,
original source/test excerpts and HTTPX's BSD-3-Clause license. Full exports and
diffs remain recoverable in ignored storage. Interpreter prefixes become `<ENV>`.
Excerpts alone are not runnable: replay from the full pinned checkout with the
recorded dependencies and reconstructed commands. Fresh runs use
`run_httpx.py --profile queryparams-audit` with explicit source/interpreter,
committed revision and unused output path.

The same development case has now been exposed repeatedly. Do not rerun it merely
for favorable scores. Separate confirmation and broader task coverage are needed;
current all-eight efficiency remains unmet. No featured chart is changed.
