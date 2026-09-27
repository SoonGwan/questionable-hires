# Traceback display prototype01 — 2026-09-27

Parent `d3e7d5b6`. [Prototype](prototypes/fold_tracebacks.py) reads an already
retained output file and never executes, grades or changes the native command.
Only exact repeated ordinary Python traceback prefixes become backward references
to original line numbers. Test identities, distinct frames, exception messages,
actual/expected values and summaries remain literal. Structured records expand
back to exact original UTF-8. The displayed header names/hashes the full raw file.
Keep that file and native exit; renderer exit0 means rendering succeeded only.

Unlike the [Node reporter prototype](NATIVE-NODE-REPORTER-01.md), passing/unknown
output is byte-identical and header overhead cannot enlarge output: the renderer
falls back to raw whenever its complete view would not be smaller. No arbitrary
test diagnostics are discarded. A1 MiB input limit errors explicitly; invalid
UTF-8 passes through unchanged. It supplies no subprocess deadline, cancellation,
retention/cleanup policy or attestation. Only POSIX/macOS native execution tested.

Four [native controls](../tests/test_fold_tracebacks.py) pass in checkout and a
two-file Git-free source copy: [archive output](results/traceback-display-01/archive-tests.txt).
Actual unittest runs a passing and three-distinct-failure fixture once each, with
an invocation marker unchanged by display/CLI processing. Tests assert native
exit, identities/count, all distinct failure values, unchanged raw bytes and
roundtrip reconstruction. Additional controls cover unknown text, binary/Unicode,
CRLF/no final newline, distinct frames, invalid references and oversized CLI input.
These author controls are not model task evidence or exhaustive format support.

[Historical arithmetic](results/traceback-display-01/profile.json) processes all
159,796 UTF-8 bytes of integration06 command outputs, without rerunning a task or
altering its records. Every structured view reconstructs its input; only current
Hostage item7 changes:9,596→6,198 bytes (35.41% smaller). The whole recorded output
set shrinks by3,398 bytes (2.13%). The [illustrative display](results/traceback-display-01/historical-display.txt)
uses `output.txt` as a display label; the actual source remains the identified
historical commands.json record, not a newly retained native execution file.

Byte counts do not establish tokenizer, whole-task or time savings. Added guide,
capture and inspection work may exceed the reduction. No production skill,
featured graph or hosted claim changes. The next gate is a frozen original-task
model comparison, preserving source/outcomes and charging all capture overhead.
No default adoption without actual use and both cost measures improving.

한국어: 기존 실패 로그의 반복된 동일 프레임만 원본 줄 번호로 참조한다. 정상
출력은 커지지 않고 모든 문자열을 정확히 복원할 수 있으며 실패 값도 그대로다.
네이티브 검사와 Git 없는 복사본 검사는 통과했다. 기존 전체 출력 바이트는2.13%
감소하지만 모델 토큰·시간 절감은 아직 검증하지 않았으며 기본 스킬에는 미반영이다.
