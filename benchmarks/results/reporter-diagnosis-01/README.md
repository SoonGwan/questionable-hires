# Reporter diagnosis 01 — reviewed 2026-09-15 KST

**Supported diagnosis, incomplete skill trace; no accepted efficiency win.**
[Protocol](../../REPORTER-DIAGNOSIS-01-PROTOCOL.md), launch/resources `3c7721a`,
unchanged Exorcist, Astra medium, one fresh baseline/skill pair, serial, 240-second
deadlines. Both completed; no author retry, exclusion or timeout.

| Arm | Total tokens | Process seconds | Commands |
|---|---:|---:|---:|
| Baseline | 199,192 | 146.853 | 10 |
| Skill | 116,700 | 82.136 | 7 |

Input (cache included once) + output: skill −41.41%; elapsed −44.07%. These are
recorded costs, **not a demonstrated general performance improvement**. Baseline
repairs its own diagnostic error and performs extra native/reporter validation;
skill has incomplete captured leading output. Related known installer fixture,
author-written diagnosis task from a real model failure, n=1, shared host/cache.
No featured graph promotion or broad eight-skill claim.

## Native observations

[Baseline commands](reporter-lifecycle--baseline--1/commands.json): item_3 reproduces
FileNotFoundError in reporter addFailure; item_6 supplies a passing one-method
normal control. Item_7 records complete cancellation lifecycle events 22–32:
test assertion sees leftover targets, TemporaryDirectory cleanup removes their
parent, then addFailure sees absence. Provenance checks use the actual installer
module/code/ROOT. Its fourth test gets a **probe-only AttributeError** because
the trace looks up `shutil.rmtree.__code__` while that function is mocked. This
is not an installer regression. Item_9 captures the code object before mocking
and verifies that test passes. Item_8 separately recovers the unchanged native
four-test outcome: three passes, one line-303 assertion failure. Item_11 validates
the suggested reporter-only correction in memory, preserving original test and
implementation behavior, with complete verbose results and counts. All failures
and recovery costs are retained.

[Skill commands](reporter-lifecycle--skill--1/commands.json): item_4 reproduces the
same reporter exception. Item_8 uses actual code-object profiling, native fixture
cleanup and standard failure reporting while preserving installer/tests. The
received output **starts at cancellation addFailure**, with the destination already
absent. Earlier promised runtime/source prints, the first two test headers and
the cancellation deletion sequence are missing. Only the fourth verbose method
header remains, followed by the actual line-303 assertion, `Ran 4 tests`, one
failure, zero errors/skips and successful file preservation. The fourth normal
test's cleanup call/removal/absent-path/addSuccess sequence is retained.

Thus the skill's core explanation is consistent with source and retained native
behavior, and recovered failure/counts are present. But its final answer's full
normal/cancellation observation table is **not fully verifiable from the original
captured stream**. Do not substitute the command's intended prints, author
preflight, baseline trace or a later replay for those missing observations. The
layer responsible for omission is not established; raw CLI text already lacks it.

Both recommend removing the post-cleanup filesystem diagnostic while preserving
standard failure recording. That fixes the reporter, not cancellation rollback,
and cannot reconstruct deleted state. Ordering was examined on supplied Python
3.9.6, not established universally. No files were edited by either model. All 13
final input files match frozen bytes, installed skill manifests are unchanged,
and no scratch remains. Original commands/usage and source-hash manifests reconcile
with the redacted export. Complete received streams are retained, not full upstream
output guarantees. No author replay supplies missing model evidence.

## Collector correction after the frozen run

The old verbose-count review heuristic required `unittest -v` in shell text.
Programmatic TextTestRunner calls bypassed it, so the original metadata has no
warning. A regression using this exact captured item first failed (`None` rather
than a review candidate). The corrected collector also recognizes a mismatch from
native verbose method headers: four reported tests versus one retained header.
Quiet output without headers remains unclassified; complete native output stays
unflagged; multiple count summaries remain unsupported. This is a manual-review
candidate, not automatic test failure, proof of capture loss or a completeness
guarantee. Historical metadata is unchanged. Native full/partial/quiet controls
and the retained trace are tested; no model performance claim follows from this fix.

Decision: retain the incomplete evidence and fix the collector blind spot. Do not
add an Exorcist rule for this one case or rerun unchanged skills for a favorable
number. Further diagnostic experiments must retain concise decisive lifecycle
records separately from large source dumps when evaluating capture reliability.

한국어: 기록상 스킬 비용은 토큰 41.41%·시간 44.07% 낮지만, 기본 모델은 자체
진단 오류 복구·추가 검증을 했고 스킬의 앞쪽 실행 출력은 누락됐다. 원인 설명과
실제 assertion 실패는 확인되나 최종 관측표 전체는 원본 로그로 검증되지 않는다.
따라서 성능 승리로 채택하지 않는다. 이 누락 후보를 놓친 검증기는 실제 기록으로
실패를 재현한 뒤 수정했고, 기존 결과·수치·메타데이터는 바꾸지 않았다.
