# Native cache inventory01 — 2026-09-27

Parent `68570943`; ordinary skills and original grading outcomes unchanged.
This corrects a prospective author preservation guard, not model performance.
The earlier [file probe](EXTERNAL-BUNDLE-02-FILE-PROBE-01.md) counted a real legacy
`.cache` write as a full-inventory mismatch. Its false flag remains historical.

The separate future private driver now records `source` and `runtime_cache` maps,
each with bytes/modes, and retains full-inventory equality separately. Prospectively
declared root cache paths are `.cache`, `.pytest_cache`, `.hypothesis`, plus
`__pycache__` components. Root `.git` remains outside application inventory.
Nested `package/.cache/important.py` remains source. Symlinks record the link target
and lstat mode instead of reading their target. This is not an atomic snapshot,
directory-metadata guard, global filesystem monitor or solver preservation policy;
the declared author cache map does not prove who made a change or that arbitrary
cache contents are harmless.

[Exact extracted inventory](results/native-cache-inventory-01/inventory.py) and
[executed control](results/native-cache-inventory-01/control.py) use fresh owned
directories. Controlled source-byte, mode, deletion and symlink-target changes are
detected, while a root cache mutation remains visible in its separate map. Both
actual installed pytest2.8.7 and4.0.2 run the prior seven-test native status fixture:
the original project source stays identical and actual native cache writes appear
as `.cache/v/cache/lastfailed` versus `.pytest_cache/...`. The native suite deliberately
exits1; successful controls assert that expected outcome and exit0. No cache or
source is silently omitted from the combined inventory.

[Checkout evidence](results/native-cache-inventory-01/checkout.json) and
[Git-free copied evidence](results/native-cache-inventory-01/git-free.json) both
pass. Each native subprocess has a30-second parent timeout. The copied control has
a60-second parent timeout. No selected issue source, gold, required labels or native
issue tests are read or executed; model calls0. The old runners' installed plugins
remain loaded as already disclosed in [status capture01](NATIVE-STATUS-CAPTURE-01.md).

[Driver identities](results/native-cache-inventory-01/driver-check.json) retain the
unchanged status02 driver hash and separate cache03 driver hash. The future driver
syntax compiles but has not executed the cohort; these controls test the exact
inventory function and native cache behavior, not complete external grader parity.
The new driver records source equality, cache equality and full equality separately.
Its surrounding grading inputs remain private. Frozen original rows, labels,
parser, outcomes and adverse flags are unchanged.

This removes a demonstrated author guard error from the prospective comparison
path. Full-cohort native grading, runtime/label compatibility, solver isolation,
all8 developer quality and joint whole-task token/time reductions still require
their own evidence. No skill, README, featured chart or landing performance claim
changes on the basis of these controls.

한국어: 다음 작성자 검사에서는 소스와 선언된 런타임 cache를 별도로 기록하고
전체 변화도 유지한다. 실제 pytest 두 버전과 Git 없는 복사본에서 cache 쓰기를
확인했고, 소스 내용·권한·삭제·링크 변경 검출도 검증했다. 기존 오탐 결과는
그대로 보존한다. 전체 외부 과제와 모델 비교는 미실행이며, 토큰·속도·8개 역할
품질 개선 증거는 아니다.
