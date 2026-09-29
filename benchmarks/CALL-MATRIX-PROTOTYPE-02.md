# Call matrix prototype02 — partial evidence retained, 2026-09-27

Parent `a4ce4ee0`; [historical prototype01](CALL-MATRIX-PROTOTYPE-01.md) unchanged.
[Source](results/call-matrix-prototype-02/matrix.py),
[native controls](results/call-matrix-prototype-02/control.py),
[actual observations](results/call-matrix-prototype-02/result.json),
[Git-free copy](results/call-matrix-prototype-02/archive-check.json),
[source identities](results/call-matrix-prototype-02/identities.json).
Zero models; no ordinary skill installation or performance claim.

Version2 changes the report interface explicitly: attempted calls, evaluated cases,
unrun cases and ungraded observed calls are separate. An unsupported actual return
now stops with `complete:false`, an encoding error and all earlier comparisons and
examples retained. It does not count an unreportable return as a pass/mismatch or
execute later cases. Invalid inputs/expectations still fail before the first call.
Consumers must check complete, counts and error, not assume process0 means complete
or that collected expected failures are passing alternatives. Version1 is frozen;
this does not retroactively repair original model probes or rescore results.

Native controls preserve the same real supported render caller, independent source
substitutions and all27 cases per variant: mismatches0/15/0/9. Required unittest4
passes separately. Nine boundaries pass: wrong return, wrong exception type, input
mutation, invalid example limit, invalid expectation, retained partial mismatch,
unrun not called, count conservation and validation before first call. In the
partial control, call0 returns41 instead of42; call1 returns an unsupported object;
call2 remains unrun. Report has attempted2,evaluated1,mismatch1,ungraded1,unrun1,
completefalse and the first actual/expected example. Full source/input preservation
and callback restoration remain observed. A Git-free native copy passes all controls.

Limitations remain: callback execution is unsandboxed and internally unbounded,
exact exception types only, no message checks, limited primitive value encoding,
Python equality semantics and caller-owned source binding/contract derivation.
BaseException interruptions and unexpected failures outside encoding still propagate;
partial report retention is not comprehensive process-loss/cancellation recovery.
The archive run has30s parent/15s required-test bounds. Initial checkout control
completed without an imposed parent deadline; retain this execution limitation.
Authored repeated controls are not independent validation. Report size changes are
not measured whole-task tokens/time, and this prototype is not a default helper.

한국어: v2는 평가 완료·호출 시도·미실행·판독 불가 항목을 구분한다. 중간에
지원하지 않는 반환값이 나오면 앞선 실제/기대값 예시를 보존하고 completefalse로
중단하며 뒤 항목은 실행하지 않는다.9개 경계 검사와 필수 테스트4개를 실제 실행,
Git 없는 복사본에서도 확인했다. 인터페이스 변경은 명시적이고 모델 실행·설치·
토큰/시간 절감 주장은 없다. 프로세스 손실·중단 전반의 복구는 아직 보장하지 않는다.
