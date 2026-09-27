# Receipt native split01 — compatibility gate, 2026-09-28

Parent`1b85702c`; isolated code-layout candidate only. Ordinary installed/deployed
Receipt remains unchanged. The [guard output01 model records](RECEIPT-GUARD-OUTPUT-01-REVIEW.md)
show large helper reads and combined source-output truncation in three of four
sessions. Existing instruction/read-budget experiments did not establish a general
fix. This candidate tests a runtime partition before any model schedule.

[Transformation](receipt_native_split_candidate.py) moves unchanged Python/Node
startup strings, native check interpretation and process capture into native.py.
compare.py retains recipe validation, snapshotting, revision selection, copying,
original/tree guards and CLI. Existing call names stay available; actual capture,
read and assertion-startup instrumentation is passed at the observed boundaries.
The local source loader uses runpy rather than changing sys.path or writing a native
module bytecode cache. Bytecode behavior still requires actual verification before
adoption. Loading trusted package code is not a sandbox.

Source size: compare.py43,772→27,952 bytes, with17,162 bytes in the new companion.
The total grows to45,114 bytes. These are bytes, not model tokens or saved work.
An agent that needs both sources may read more or require another response.

## Fixed native gate

[Controller](results/receipt-native-split-01/control.py) runs the same ten current
native test modules in ordinary and candidate Git-free copies, serially. Existing
fixtures provide real positive and defective assertions, bootstrap/module/Pytest/
Node entrypoints, assertion observation, timeout/cleanup, guards and multiple
versions. Node24 and the existing Python environment are used; no installation,
model call, approval change or user-project mutation. Preserve every result.

Do not alter the two existing tests that relocate only compare.py. They exercise
a known one-file CLI caller, and the new required companion is a compatibility
concern. Passing full-package calls cannot silently replace that requirement.
Require identical child program strings and unchanged functional assertions.
Any failed existing caller blocks adoption and paid model timing at this checkpoint;
record the exact failure, not just a smaller source file or otherwise-green suite.
No featured/chart/README capability/installed resource change follows preparation.

한국어: 긴 하위 실행 코드를 분리하는 격리 후보다. 진입 파일은 작아지지만 전체
리소스는 커지고 추가 파일을 읽을 수 있으므로 토큰 절감으로 계산하지 않는다.
기존 파일 하나만 복사하는 CLI 검사도 그대로 유지한다. 이 호출 방식이 깨지면
정상 설치 경로가 통과해도 채택하거나 모델 성능 실험을 진행하지 않는다.
