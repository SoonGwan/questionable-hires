# Batch/probe composition correction — 2026-09-21

Parent `af9f5d5`. This is an input-contract/documentation correction, not a new
model-performance measurement. [Effort-factorial01](EFFORT-FACTORIAL-01.md)
retains the original failed attempt, its repair and all cost; no attempt is rerun
or relabeled as evidence for this correction.

## Observed mechanism

SQLite low-current read the native batch and probe references, then put
`probe_replacements`, `probe_tests` and `probe_when` at the shared batch root.
The helper rejected this with the generic message:

> Batch requires shared files/imports/runner/tests and 1–8 mutations

The session subsequently read the separate batch contract and recovered. The
native recipe linked probe details without specifying their placement; the probe
page described fragments in single-audit context and requested the common guide.
The detailed batch reference already specified correct nesting, but was not the
initial route. This is a plausible documentation contributor, not proof that the
model will avoid the error after an edit.

## Narrow correction

The native batch route and probe reference now state that probe fields belong in
the relevant `mutations[]` entry; single-audit recipes keep those fields at the
root. The probe reference accepts the already-selected native batch contract
instead of making the single-audit guide another prerequisite. No entrypoint,
invocation policy, assertion requirements or execution authority changed.

Misplaced known fault/probe fields still fail before execution, but the diagnostic
names the fields and their destination. The helper does not silently move them,
apply them to every mutation, ignore them, or broaden the accepted schema.
Unknown root keys still fail the existing validation.

## Actual packaged-example check

The new control extracts the JSON from the shipped native batch recipe and the
first native probe example from a built package. Putting the probe fragment at
the batch root reproduces CLI exit2 with no report and unchanged source inventory.
Before the correction the new diagnostic assertion failed (3tests,1failure,
1.227s); it did not show that the old helper accepted invalid input.

At the documented mutation boundary, both existing weak-test runs survive,
the stronger native probe passes normal code and rejects each actual fault with
`AssertionError: Lists differ`. The second correct probe references the first
executed observation; it is not counted as another process. Original bytes/modes
and owned-scratch cleanup are verified. No model session or benchmark task is
executed by this test.

- Python3.9.6 packaged-guide tests:3pass in1.614s.
- Python3.11.16 audit-related tests:107pass in16.410s, no skips.
- Skill validation, repository links, featured synchronization and whitespace
  checks pass.

Full-task quality review of the eight original sessions remains pending. This
fix does not establish lower model tokens/time, independent generalization or
broad20–30% improvement. Featured charts and default reasoning effort remain
unchanged. Do not retest the same exposed SQLite task until favorable.

한국어: 실제 배치 입력 오류의 원인이 될 수 있는 안내 연결을 수정했다. 강화
검증 필드의 위치를 명시하고, 잘못 놓인 필드는 실행 전 정확한 위치를 안내하며
거부한다. 패키징된 예제를 조합해 실제 정상 통과·결함 검출·원본 보존을 확인했다.
모델의 오류율이나 토큰 절감이 입증된 것은 아니며 과거 결과는 그대로 보존한다.
