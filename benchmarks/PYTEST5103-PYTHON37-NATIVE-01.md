# pytest5103 prepared Python37 native gate01 — 2026-09-28

Accept the separately prepared Python3.7 native gate for this selected case.
Protocols: preparation `65a4c0e8`, corrected input mode `f51f73c9`, issue pair
`8f5e5b67`. The official Python3.9 pair remains rejected. This is author validation,
not a skill/model improvement, unchanged official harness or token-saving result.

| Original issue outcome | Base | Gold |
| --- | --- | --- |
| Required FAIL_TO_PASS | 1 failed | 1 passed |
| Required PASS_TO_PASS | 64 passed | 64 passed |
| All primary call outcomes | 64 passed,3 failed | 67 passed |
| Setup skips | 5 | 5 |
| Actual native pytest exit | 1 | 0 |
| Shell/container exit | 0/0 | 0/0 |

[Original aggregate results](results/pytest5103-python37-pair01/grade-summary.json)
and [observer accounting](results/pytest5103-python37-pair01/observer-consistency.json)
cover all72 collected items and211 phase reports per cell:67 three-phase call
items plus5 setup-skip/teardown items. No ambiguous/unmapped required labels,
setup/teardown errors, infrastructure failures, OOM or timeouts. Both required
parser statuses and underlying primary candidates satisfy the frozen contract.
The two additional base failures are retained; gold has no additional failure.
Skips are not passes. The original parser reports67 call-bearing items, not72.

The [pair protocol](PYTEST5103-PYTHON37-PAIR-01-PROTOCOL.md) removes exactly four
conda activation lines from the original evaluation body. The test patch, command,
warnings policy,65 required labels, reset commands and parser are unchanged.
Adapted body SHA256 `35d95f07b5e8fc3faf1aab5f0cd6b821214a5897c7cb0177051a021af03c928a`;
original SHA256 `4fb5a5c9fb54a596c6dd720e30afbca905336730c2d656a3b6062e5bb4a82307`.
This environment also changes image/OS/dependencies, so do not attribute the
entire pair difference solely to Python version. Earlier compiler/native warning
diagnostics provide narrower evidence of that mechanism. Private patch bodies,
original labels and raw issue logs remain outside this repository and solver inputs.

Preparation exports418 byte-verified source files and existing Git metadata from
the official base image, with synthetic HEAD `5df4d131d551b79b9fcf258482eaa4f59bf238b8`.
It does not invent a version/tag or copy installed packages. Source tar17,745,920
bytes, SHA256 `bf7e8f530997f3b4540c3fbca4bf71cbe5ae286044e778481d4183d8c0449d6f`.
All418 source file modes differ from the selected base archive; byte equality is
not file-mode equality. Gold's generated version adds `.d20260928`; base is
4.5.1.dev41+g5df4d131. Both native imports resolve `/testbed/src/pytest.py`.

The first [preparation](PYTEST5103-PYTHON37-NATIVE-01-PROTOCOL.md) fails before
installation with PermissionError reading a wheel: requested0755 under private
umask077 left the parent directory0700. Preserve
[error](results/pytest5103-python37-native01/qh-py37-controls01-native.stderr),
[actual input mode](results/pytest5103-python37-native01/initial-input-mode.json)
and cleanup. The original driver skipped terminal/OOM inspection on early failure;
that state is unknown, not a zero-OOM observation. Native02's prospective ownership
explanation was not instrumented; actual copied UID/GID were not recorded. The
observed boundary is the directory mode/access failure and corrected-mode success.

The [corrected preparation](PYTEST5103-PYTHON37-NATIVE-02-PROTOCOL.md) explicitly
sets the wheel directory0755, keeps files0644 and the enclosing private root0700.
All15 wheel hashes, source tar, preflight and primary observer remain unchanged.
Offline dependencies and ordinary build-isolated editable install succeed,
fresh public import works, pip check reports no broken requirements, and all418
source hashes stay unchanged before/after installation. Metadata is generated
naturally; no forced version or conda shim. Authored pass/fail/nested controls
exit0/1/0 with exactly one primary item/three reports each. The nested inner
assertion fails with41 versus42, while only the passing outer item is reported.
[Native observations](results/pytest5103-python37-native02/qh-py37-controls02-native.stdout),
[full installed packages](results/pytest5103-python37-native02/authored-controls/pip-freeze.stdout)
and [authored assertion output](results/pytest5103-python37-native02/authored-controls/fail.stdout)
preserve the actual checks.

The unchanged8GiB guest-space gate initially requires removing one redundant
guest pytest5221 transport. Host and guest SHA256 are checked against the existing
transport record first; the host archive remains. No image/unrelated resource is
deleted. [Recovery record](results/pytest5103-python37-native01/space-recovery.json).
Successful native02 and both pair containers exit without OOM under network none,
no mounts, dropped capabilities, no-new-privileges and1GiB/1CPU/64PIDs. Frozen input
hashes still match. All attempts end with zero containers, services inactive/disabled,
VM stopped and no owned Lima/SSH process:
[native01 cleanup](results/pytest5103-python37-native01/cleanup.json),
[native02 cleanup](results/pytest5103-python37-native02/cleanup.json),
[pair cleanup](results/pytest5103-python37-pair01/cleanup.json).

Do not rerun this accepted pair unchanged. This establishes one scoped prepared
native case; other selected-case failures and solver authorization remain unresolved.
No model calls, ordinary skill/install/public release changes or measured efficiency
claim. Public release remains `281c3cf0`; whole-task integration07 remains tokens
+1.67%/CLI time−9.63%, only2/8 pairs lower both. No all-eight completion claim.

한국어: 별도 Python3.7 환경에서 원본 필수 실패1개·통과64개와 정답 필수65개
통과를 확인했다. 전체 실제 검사는 원본64통과·3실패, 정답67통과이며 양쪽 모두
5개 건너뛰기로72개·211단계 보고와 일치한다. 실제 pytest 종료값은1/0이다.
최초 폴더 권한 오류와 기존 공식3.9 불합격을 그대로 보존한다. conda 활성화4줄만
제거한 별도 평가이며 이미지·의존성 차이도 있어 단일 원인의 효과로 단정하지
않는다. 원본 채점·경고 조건은 유지했고 모든 환경 종료를 확인했다. 모델·토큰
절감 근거는 없으며 전체8개 목표와 다른 검증 과제는 남아 있다.
