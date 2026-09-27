# Con Artist cleanup lookup evidence01 — 2026-09-28

Parent **`e9ee3bce`**; [source identity](results/audit-cleanup-lookup01/identity.json).
A controlled lookup failure exposed incorrect successful-removal evidence. This
repairs the runtime counterpart to the existing unknown-guard contract; it is not
a new model-efficiency result or a remeasurement of prior comparisons.

Path.exists()/is_symlink() can suppress EBADF, ENOTDIR and ELOOP as absence on the
validated Python3.11.6 runtime. The helper's negated presence expression then
reported `owned_scratch_removed: true`. A completed audit could remain observed
and CLI0, or a pre-existing error could retain a false cleanup success. An explicit
lstat now confirms absence only for FileNotFoundError; an existing entry, including
a dangling symlink, is present. Other lookup errors retain unknown/null evidence.

With otherwise completed checks, the existing integrity-error path raises the lookup
OSError and keeps returned checks; CLI2 emits incomplete JSON. A pending execution
or final guard error keeps its original exception identity and unknown removal.
Later mutations stop. This does not add cleanup retries, infer an unreturned check,
restore originals or guarantee an atomic filesystem snapshot.

[Receipt's earlier repair](RECEIPT-EXECUTION-EVIDENCE-01.md) addressed lexists on its
own error paths. This change addresses Con Artist's separate presence expression,
including its otherwise-successful path; no Receipt runtime or frozen result changes.

## Reproduction and scope

[Six controls](../tests/test_audit_cleanup_lookup.py) execute real native checks and
inject OS lookup errors at the parent process's Path.stat boundary. This is not an
observed production incident. The helper's normal native runner, actual assertion
failure, selected-source checks and cleanup remain in use.

The [initial fixture](results/audit-cleanup-lookup01/invalid-fixture.txt) failed to
reach injection because the Mac temp path used /var while the helper resolved
/private/var. Its eight failures are invalid bug evidence and remain recorded.
The corrected fixture normalizes that root and asserts that the lookup injection
actually ran. Only this corrected version is used unchanged before/after the fix. Original
unittest transcripts retain their progress-line trailing spaces.

[Valid before](results/audit-cleanup-lookup01/before.txt):seven failing subcases across
six methods. Three errno cases return observed/true instead of incomplete/null;
the CLI returns0 instead of2, the batch runs8 processes instead of stopping after4,
and pending runner/guard failures incorrectly retain true removal. The permission
error and dangling-symlink controls already behave correctly. Failing assertions
stop later assertions in those subcases; do not claim the full new suite passed.

[After](results/audit-cleanup-lookup01/after.txt):all six methods pass, zero skips.
The same real four checks retain exits0/0/0/1 and the intended `AssertionError: 2`;
a runner failure retains only its one returned result. Error identity, unknown
fields, direct CLI main output and two unrun batch mutations are checked. The CLI
control invokes main in-process with injected lookup failure, not a separate shell
or model execution. Dangling owned symlinks remain false/present. Successful normal
removal and existing guard/cache/native-runner contracts remain covered by the
[Git-free source-copy suite](results/audit-cleanup-lookup01/gitfree.txt):162 methods
across12 modules pass, zero skips. Some retention/process controls are structural
mocks, not additional native performance measurements.

Both README capability rows and the common guide describe unavailable lookup
results honestly. Entry, model settings, native assertion requirements, featured
measurements and integration07 stay unchanged. The batch's8→4 count reflects stopping
invalid work after a required guard failure, not a general speed/token saving.

한국어: 복사본 조회 오류를 삭제 완료로 잘못 기록하던 경로를 수정했다. 실제 없음만
성공으로 확인하며 조회 불가는null·불완전 결과로 남기고 기존 오류·반환된 검사·
후속 실행 중단을 유지한다. 첫 경로 오류가 있는 재현은 무효로 별도 보존했고,
교정한 동일 검사에서 수정 전7개 실패→수정 후6개 메서드 통과를 확인했다.
Git 없는 사본162개 검사도 통과했지만 모델 토큰·시간 개선 수치로 계산하지 않는다.

## Installed and packaged source

Source **`a7828248`** is installed after prior Con Artist resources matched parent
`e9ee3bce` bytes and Git modes; the previous directory is backed up outside discovery.
[All eight installed skills match](results/audit-cleanup-lookup01/installation.json),
and [six controls using the installed helper](results/audit-cleanup-lookup01/installed.txt)
pass. [Standalone package checks](results/audit-cleanup-lookup01/package.txt):4 pass.
The151-file build changes only archive/checksum; [all52 packaged resource bytes/modes](results/audit-cleanup-lookup01/download.json)
match source. No layout, OG, frozen model metric or browser interaction change is claimed.

한국어: 소스a7828248를 개인 설치와 다운로드에 반영했다. 기존 자원을 확인·백업한 뒤
설치본6개·패키지4개 검사 및 전체8개 자원 일치를 확인했다. 실행 오류를 바로잡은
수정이며 기존 모델 비용 결과를 새 버전의 성과로 바꾸지 않는다.

## Public delivery

Hosted release **`ea9c9dd253ba2dc325ff9848849c7dcf931a8f0b`** is live on the existing
[한국어](https://hires.no-money-do-you-have-money.com/ko/) and
[English](https://hires.no-money-do-you-have-money.com/en/) addresses.
[Six HTTPS observations](results/audit-cleanup-lookup01/public.json) verify revision,
exact locale pages/JavaScript, canonical/indexable metadata and archive/checksum.
All52 public archive resource bytes/modes match current source. Download:107,508
bytes, SHA-256 `45090c01c009041bd8d7b5ffa8ac14b951e83903a2c6f3c02375c2868e35d26a`.
Existing integration07 values still measure `1be35120`. No browser interaction,
new model-efficiency result or GitHub push is inferred from these HTTP checks.

한국어: 배포ea9c9dd2의 실제 HTTPS 다운로드에서52개 자원·권한 일치를 확인했고
한영 페이지와 체크섬을 포함한6개 경로가 통과했다. 기존 실험 수치는 유지한다.
