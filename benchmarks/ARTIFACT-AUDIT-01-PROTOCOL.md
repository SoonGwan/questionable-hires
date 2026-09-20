# Artifact audit 01: frozen three-condition development comparison

2026-09-20. One new authored artifact-manifest workflow, not an independent
real-project benchmark. Baseline has no skill, original Con Artist is `9c0c458`,
candidate is `7c96592`. Entry/metadata are identical; only audit.py and its two
interface references change. No assumption that agents choose the helper.

Three fresh Astra medium sessions, one per condition, serial fixed order:
original, baseline, candidate. Timeout 360 seconds each. Shared host/cache and
fixed order confound timing; n=1 is exploratory. No retries or omitted attempts.
All eight roles remain the overall objective; this diagnostic task cannot prove
their performance or a general 20–30% improvement.

## Native controls before model calls

`tests/test_artifact_audit_case.py` executes the existing native pytest suite and
a strengthened native suite, each against correct and digest-loss implementations.
Original correct/faulty and stronger correct: three passes. Stronger faulty:
two digest-value assertion failures plus one passing empty control, exits 0/0/0/1.
Unicode names, duplicate names and exact digests are retained. Configuration runs
before application import, and fixture-owned temporary files remain project-local.
The current helper independently produces the same four results, copied-import
evidence and cleanup. Original project bytes/modes remain unchanged.

The fixture deliberately exercises the recently corrected native lifecycle; it
is a diagnostic transfer task, not an unbiased sample of everyday work. Its
stronger author oracle is not exposed to model sessions. Agents choose their own
isolation and native assertions. The task explicitly permits only test-file edits,
with no production/fixture/resource edits, external discovery, installs or network.

## Frozen evaluation criteria

All four model-visible criteria in `artifact_audit_case.py` are necessary:
original full native correct/faulty comparison; same improved native suite passes
correct and rejects faulty behavior; counts/exits and same-process provenance for
each check; requested test-only delivery with original preservation and cleanup.
Setup errors and incomplete controls are not detected faults. Author replay of
delivered tests, if needed, is separate from the model's measured evidence.

Retain total input plus output tokens (cached input once), process wall time,
native outcomes, final diff, commands and all scheduled cells. Inspect persisted
initial context rather than trusting disable arguments. Missing CLI output is
checked against the original stored tool response, never repaired by a rerun.
Only equal-work outcomes support an efficiency comparison; adverse results remain.
No representative-chart promotion from this experiment.

Prepare using a Python with the declared development dependencies:
`python -B benchmarks/run_artifact_audit_01.py`. Review and commit the immutable
inputs, then invoke once with `--execute`. Preparation executes native controls,
snapshots committed resources and records hashes; it makes no model call.

한국어: 새로 작성한 산출물 목록 검증 과제를 무스킬·수정 전·수정 후 각 1회
비교한다. 최근 고친 pytest 실행 순서를 의도적으로 포함한 진단용 과제이지
실제 프로젝트 전체의 무작위 표본이 아니다. 정상/결함 코드와 기존/강화 테스트의
네 조합을 먼저 실행하고, 같은 요구사항을 완료한 모델 작업의 비용을 비교한다.
실패도 보존하고 대표 그래프나 8개 역할 전체의 성과로 확대하지 않는다.
