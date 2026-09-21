# EventEmitter boundary transfer — native preparation only

2026-09-21. Candidate resource `89c5172`, production resource `716ef88`.
No model sessions have run and no adoption decision follows from these controls.

Two author-selected changes to the unmodified EventEmitter3 tag5.0.1 source,
commit `a650549176ded0d0dcc52e27b03ae5669d7dcd7c`. The unchanged implementation
and MIT license are [pinned locally](fixtures/eventemitter3-5.0.1/PROVENANCE.md).
This is a source excerpt with authored native tests, not the upstream test suite,
an independently selected holdout or a claim about the current upstream version.

1. Reentrant once dispatch: an earlier listener recursively emits the same event;
   the later once listener currently runs twice. Correct the registration lifetime
   across nested single/multiple-listener paths, including failure propagation.
2. Ordinary synchronous control: `removeAllListeners('')` currently removes all
   events, including unrelated string/symbol events. Keep empty event selection
   distinct from omitted/undefined selection without changing other APIs.

Exact requests and five criteria per task are in
[eventemitter_boundary_cases.py](eventemitter_boundary_cases.py). Solutions and
oracle assertions are author-only, not part of `cases()` model input files.
Initial native smoke coverage is authored and must be described as such, not as
upstream tests. Preserve initial source/license hashes and report all edits.

## Native observations

[Five original author controls](results/eventemitter-boundary-01-preflight.json)
run Node24.16.0 against temporary copies of the actual pinned module. Both upstream
behaviors fail real assertions. Full corrected reentrant code passes six native
tests including initial smoke; a partial fix handling only the array dispatch path
still fails the nested single-listener control. Corrected empty-event code passes
three native tests including smoke. The Python wrapper verifies expected exits,
assertion failures and source identities; both tests pass Python3.9/3.11.

These observations establish useful controls, not exhaustive correctness or model
benefit. Source has not been modified upstream or in the pinned fixture.

## Next execution gate

Freeze runner identities, Node/Python environments, resource digests, six-cell
schedule and a one-shot launch marker before measuring. Use baseline, prior and
the completion-boundary candidate once per task; reverse order between tasks.
Retain failures, repairs, full token/time cost and original native capture. Never
repeat these exposed tasks to replace unfavorable results. Scope and execution
claims must be checked separately from the implementation's observed behavior.

This transfer is synchronous reentrant dispatch, not a Python completed-fetch
callback window. It tests whether the narrow ownership guidance generalizes;
even a success would not prove async-boundary coverage, all-eight improvement or
20–30% savings. Production skills and featured charts remain unchanged.

한국어: 실제 라이브러리의 고정된 소스에서 재진입 중복 호출과 빈 이벤트 제거
문제를 재현했다. 작성자 정상·결함 대조만 검증했으며 아직 모델 비교는 하지
않았다. 원본 과제를 재탕하지 않는 전이 검사지만 독립 홀드아웃은 아니다.
