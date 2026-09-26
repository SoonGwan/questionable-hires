# Receipt guard I/O prototype01 — rejected, 2026-09-27

Author prototype against repository **`d4bacdf6`**, unchanged measured Receipt
resource **`6701069f`**. No model calls or whole-task efficiency comparison.
[Rejected patch](results/receipt-guard-io-01/rejected-prototype.patch),
[source hashes](results/receipt-guard-io-01/source-sha256.json).

The guarded comparison checks selected originals and then inventories the whole
project. The prototype integrated exact selected-byte/mode comparisons into the
final inventory stream, keeping hashes, size bounds and non-followed symlinks.
A real native before/after control reduced selected source opens4→3. The original
new I/O control fails4≠3, rather than an import/setup error.

Two intermediate warmed author profiles alternate20 pairs on one9MiB synthetic
tree: selected8MiB, other file1MiB, empty directory and dangling link. Both verify
the same returned inventory and exact selected bytes/modes. First median final-pass
5.522→4.667ms(−15.49%); after observed-open mode checking,5.584→4.668ms(−16.42%).
Absolute differences are under1ms. These are isolated preservation-pass timings,
not native test times, model tokens, independent samples, whole-task speed or
all-eight gains. [First profile](results/receipt-guard-io-01/prototype-profile.json),
[second profile](results/receipt-guard-io-01/profile.json).
The final rejected source additionally checks selected permissions after reading;
those intermediate timings are not relabelled as its measurement.

## Decisive counterexample

After both actual native checks complete, mutate a watched file immediately after
its selected-read bytes are returned. This is a deterministic author stream hook,
not a claim about production concurrency. Both implementations execute one real
assertion failure before and one real pass after, with completion counts1 each.

| Implementation | Watched file finally contains | Verdict |
| --- | --- | --- |
| Original d4bacdf6 helper | `changed!` | Rejects: whole-tree scan detects notes.txt change |
| Final prototype | `changed!` | Incorrectly accepts and reports tree guard unchanged |

[Original native counterexample observations](results/receipt-guard-io-01/counterexample.json).
The original selected read sees captured bytes; its subsequent whole-tree read
sees the changed file. The single-pass prototype compares and hashes the earlier
bytes, missing this observed change. Mode checks do not repair it. Existing guards
are not atomic and never certified every transient action, but that limitation
does not authorize discarding a change they actually detect.

**Reject the optimization and restore helper bytes exactly.** Saving one read or
under1ms does not justify weakening this behavior. No helper API, byte/mode check,
output contract or skill instruction change is adopted. Default and guarded
comparison workflows remain unchanged; no release/token improvement is claimed.

Keep one new regression in `test_receipt_tree_guard.py`: a real native comparison
rejects the late watched-file mutation and does not restore the changed file.
[Current checkout controls](results/receipt-guard-io-01/current-regression.txt):15/15.
[Git-free current controls](results/receipt-guard-io-01/current-archive.txt):15/15.
Apply the exact rejected helper patch only in the archive and run that same test:
[it fails because RuntimeError is not raised](results/receipt-guard-io-01/prototype-regression.txt).
The new test therefore detects this bad optimization rather than merely repeating
an implementation check. Author-owned temporary projects are cleaned up.

## Validation boundaries

Intermediate prototypes pass201/201 and202/202 Receipt tests; the final prototype
passes19 focused controls despite the counterexample. Those counts are historical
prototype tests, not current full-suite or model evidence. Earlier focused16 pass;
an initial Git-free17-test run has one missing `receipt_startup_case` import, then
corrected fixture copying yields17/17. Retain the import failure as author packaging
error, not a native behavioral failure. Intermediate owned all8 installation
byte/mode checks and Receipt native checks pass; not final release validation.
Observed permission change during a selected read initially escaped the prototype;
its failing control and later correction are retained. They do not erase the
final byte-mutation counterexample. [All author artifacts](results/receipt-guard-io-01/source-sha256.json).

Historical diagnostic script snapshots have redacted local path placeholders;
they are evidence, not new supported analysis CLIs. No full private context or
model session is involved. No featured benchmark, deployed site, dependency,
configuration or CI change. The all-eight quality/token/time goal remains unmet.

한국어: Receipt guard I/O01(2026-09-27,저장소`d4bacdf6`,스킬 자원`6701069f`)에서
마지막 보존 검사의 중복 읽기를 줄이는 시제품을 만들었다. 로컬9MiB 검사에서
중앙값 차이는1ms 미만이고 모델 토큰 절감 근거는 없다. 읽은 직후 파일이 바뀌는
통제된 반례에서 기존 검사는 거부하지만 시제품은 잘못 통과했다. 시제품을 폐기하고
도구를 정확히 복원했으며, 이 변경을 막는 회귀 검사만 남겼다. 현재 체크아웃과
Git 없는 복사본의 관련15개 검사가 통과하고, 같은 검사는 폐기된 도구에서 실제로
실패한다. 전체8개 역할의 품질·토큰·시간 개선 목표는 계속 미달이다.
