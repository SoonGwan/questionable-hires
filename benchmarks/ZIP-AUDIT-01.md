# ZIP audit01: routing changed, whole-task efficiency not established

2026-09-21. Prior `f7ecb45`, candidate `ac108f5`, launch `0807814`.
[Frozen protocol](ZIP-AUDIT-01-PROTOCOL.md) · [all original evidence](results/zip-audit-01/README.md).

## Decision

All six original attempts meet the four task-visible criteria. The candidate
uses a direct native check for one fault and the batch helper for two faults;
the prior uses a batch for both. This is an observed routing difference, not
proof that the wording caused it or that direct execution is always cheaper.
Keep the phase distinction provisionally as accurate guidance, **not an accepted
performance win**. Do not promote this experiment to the featured chart or rerun
these exposed cases until a favorable result appears.

| Task | Arm | Input + output tokens | Process seconds | Criteria |
|---|---|---:|---:|---:|
| Single fault | Prior | 110,138 | 56.614 | 4/4 |
| Single fault | Baseline | 66,342 | 68.562 | 4/4 |
| Single fault | Candidate | 86,203 | 67.712 | 4/4 |
| Two faults | Candidate | 97,126 | 62.874 | 4/4 |
| Two faults | Baseline | 66,871 | 68.739 | 4/4 |
| Two faults | Prior | 96,300 | 60.472 | 4/4 |

Candidate versus prior: single fault **−21.73% tokens / +19.60% time**;
two faults **+0.86% / +3.97%**. Versus no skill, candidate tokens increase
**29.94% and 45.24%**, while elapsed time decreases1.24% and8.53% respectively.
Cache is included once in input, reasoning is not added again to output.
These are descriptive per-cell ratios, not billing estimates or causal effects.

## Original execution review

All arms inspected the actual test, package entrypoint, endpoint alias and writer.
Every checking process verified local imports and actual `build → create_package`
and `_pack → writer.pack` bindings. All kept the two specified faults independent.
Existing native tests pass on normal code and every requested mutant. Stronger
checks reopen actual returned ZIP bytes and compare complete ordered records,
including empty/binary payloads, permission bits and Unix creator system3.
They also check caller values and tuple identities before the defect assertion.

All normal stronger checks pass. Metadata omission fails an assertion on384
(`0600`) versus493/416 (`0755`/`0640`); payload omission fails on empty versus the
original binary bytes. No import/setup failure substitutes for a killed fault.

- Single/prior: original two-test suite in all four phases; augmented original
  test catches the metadata fault, empty-package test still passes. Helper batch
  contains one mutation, with per-mutation probe replacements.
- Single/baseline: two original tests plus a separate stronger native test in
  each of two fresh processes; outer script explicitly expects the mutant's
  assertion failure, so overall command exit0 is not a false pass.
- Single/candidate: four fresh native runs, each includes a binding test;
  original phases run3 tests, stronger phases run2. No helper/reference read.
- Multiple/prior: two original tests and one added stronger native test per
  variant; batch reuses the correct original/probe checks for the second fault.
- Multiple/baseline: same native runner over three independent copies; stronger
  fixture is extracted from the actual original test's literal assignment.
- Multiple/candidate: original two-test suite augmented in the probe; batch
  reuses correct original/probe checks, with two native tests per actual phase.

Both skill batches use the documented per-mutation probe placement without
schema-error recovery. Candidate/multiple selects four source/test files rather
than copying requirements, but reads requirements and enables whole-project
preservation. All six preserve every original file's bytes/modes and installed
skill resources; exact final project inventories contain only the five supplied
files. Original cleanup evidence confirms owned project-local scratch removal.
Reviewed commands show no external discovery, network or out-of-scope repair.
Final inventories alone are not proof of every transient action.

### Reviewer correction: escaped bytes are not a failed criterion

An intermediate reviewer message mistakenly interpreted the candidate/single
JSON-escaped output as testing literal backslashes. Decoding the stored shell
output and parsing its displayed record establishes payload hex
`00ff6c61756e6368`, length8, in both normal and faulty checks. The prior/multiple
record has the same binary value. This was a reviewer display-interpretation
error, not a model failure; no model replay or evidence rewrite was performed.

## Provenance and limitations

Actual stored turn contexts are GPT-6 Astra medium for all six. Original usage
counters agree with CLI totals. Exact skill bodies appear in original tool
outputs for the four skill cells; no exact candidate body is observed in either
baseline. This narrow observation is not proof of absence from all possible
context. Resource bytes/modes match the frozen prior/candidate manifests.

CLI prefixes missing from final execution output: baseline/single1153 characters,
candidate/single686, candidate/multiple3369, baseline/multiple1135. All match
unique stored full outputs with equal exit status; no unmatched records remain.
Helper-level outputs report no truncation. Filtered original records retain the
complete evidence; private raw initial instructions are not published.

One authored project, two correlated requests, n=1, shared host/cache, unblinded
author review, different extra test counts and orchestration. No independent
generalization, broad20–30% improvement, release approval or hosted-check success.
The frozen initial `measurements.json` pending-review labels remain intact; this
report supplies the subsequent review. Existing historical charts stay unchanged.

한국어:6회 모두 요청 기준4/4를 충족했다. 단일 결함에서 수정본은 이전 스킬보다
토큰21.73% 감소했지만 시간19.60% 증가했고, 복수 결함에서는 둘 다 증가했다.
무스킬 대비 토큰은 두 과제 모두 더 많다. 경로 선택 변화는 관찰했으나 전체 성능
향상으로 채택하지 않는다. 이진 바이트 관련 중간 검토자의 오독은 원본 출력의
실제 값을 확인해 정정했으며, 실패로 세거나 모델을 재실행하지 않았다.
