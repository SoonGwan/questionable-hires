# Repository collector cache audit — 2026-09-20

Prepared transfer task, not a model result. The implementation and four-test file
are unchanged snapshots of this repository at `716493b`:
`skills/con-artist/scripts/context.py` and `tests/test_context_line_index.py`.
The request and project instructions are authored for evaluation. This is not an
external issue, independent real-project study or held-out evidence: both the
code and tests were developed in this thread.

The task asks whether the real tests protect context isolation across separate
`collect` calls. Models must establish native correct-code outcomes, introduce
one valid cross-invocation reuse fault only in an isolated copy, and report actual
assertion evidence. Production/test edits are forbidden; all originals and owner
notes/cache stay intact. Native unittest discovery executes all four unchanged
tests in their original relative layout. Source binding/provenance, copied input
identity, local scratch and cleanup are explicit criteria, not hidden scoring.

Author preflight independently applies one process-global cache substitution to
the isolated implementation. Correct code passes; the faulty copy returns native
exit 1 with real assertions, including the stale-source test, not syntax/import
errors. The tests are byte-identical across arms. An author-only startup audit
hook observes actual `tempfile.mkdtemp` paths within each copy's `.test-tmp`;
normal test cleanup leaves that directory empty. The hook, mutant text and expected
outcome are not model inputs. Two fixture tests pass.

Next freeze should compare fresh baseline and current Con Artist under identical
limits, retain all attempts/costs and review originals. Do not require helper use
or a particular mutation implementation. A different fault must actually exercise
the requested cross-invocation boundary; a setup failure is not sensitivity.
This is a whole-task audit, not the earlier collector microbenchmark, and cannot
inherit its 76–78% local helper speedup as a model claim.

한국어: 실제 저장소의 코드·테스트를 수정 없이 가져온 감사 과제다. 요청과 실행
조건은 평가용으로 작성했고 이 대화에서 개발한 코드이므로 독립적인 외부·비공개
평가로 부르지 않는다. 정상 코드 4개 통과와 호출 간 캐시 재사용 결함의 실제
assertion 실패, 작업공간 내부 임시 파일 정리를 사전 검증했다. 모델에는 정답·
결함 패치를 주지 않으며 아직 모델 성능 측정이나 개선 주장은 없다.
