# Owned native pytest01 — actual runtime FAIL/PASS control

Dated checkpoint **2026-09-27**, protocol`7eeed75a`, device intervention`7e7a117c`,
parent`cad6ae94`. [Frozen protocol](OWNED-NATIVE-PYTEST-01-PROTOCOL.md),
[actual native outcome](results/owned-native-pytest-01/result.json).
Zero models and selected-case tests. Eight skills and featured data unchanged.
This is authored runtime calibration, not independent model-quality evidence.

## Actual assertion and subprocess outcomes

Inside the readonly official reconstructed root, Python3.9.20/pytest7.4.4 runs
actual native `python -B -m pytest -rA -p proof test_answer.py` subprocesses.
Fixtures and reports live only in guest `/tmp` RAM. Before/after tests and observer
plugin bytes are identical; the sole fixture implementation change returns41 or42.

| Control | Native exit | Actual pytest call outcomes |
| --- | ---: | --- |
| return41 | 1 | answer assertion failed, native child test passed |
| return42 | 0 | answer assertion passed, native child test passed |

Before output exposes **`assert 41 == 42`**, not a setup/collection error; after
reports **2 passed**. Both two-test runs have all setup/teardown phases passed,
no skip and matching test SHA256
`a94be08c436e27ad0fda03003c0a40838d823ebf9a773bc48a6246d6537482fc`.
The child's actual native interpreter prints42 and exits0 in both runs, exercising
nested automatic x86 execution. The pytest observer records native interpreter,
phase/node/outcome and session exit, rather than inferring success from shell exit.
Final VM/controller0, all8 device/routing statuses0, guest poweroff, no timeout,
**6.044 seconds**. The [controller](results/owned-native-pytest-01/control.py)
requires exact native exit/phase contrasts, identical test hash and assertion values.
[Authored fixture driver](results/owned-native-pytest-01/fixture/probe.py).

## Retained failures and device correction

Three related owned VM attempts, no selected benchmark execution:

1. [First result/source](results/owned-native-pytest-01/first-result.json): driver
   expected an observer report before preserving native stdout/stderr. Missing
   report triggers FileNotFoundError; Pythondriver1/controller1,VM0. It launched
   the before subprocess, but its native result was not exported before guest RAM
   teardown. **Capture gap remains**; do not infer its test/exit outcome.
2. [Second result](results/owned-native-pytest-01/second-result.json): collector
   tolerates missing report and retains both native outputs. Each pytest process
   exits1 **before tests**, because capture initialization cannot open `/dev/null`.
   Observer reports absent; these are startup failures, not intended assertion FAILs.
3. Final: after freezing the device intervention, mount guest-only **devtmpfs** at
   existing chroot `/dev`. Keep tests/commands/capture/package versions unchanged.
   Device mount0, actual expected FAIL/PASS contrast succeeds. No `-s` or capture
   disabling, source/dependency repair or old-attempt relabeling.

[Attempt/resource identity](results/owned-native-pytest-01/retained-attempts.json)
retains first/second private raw-console hashes, originals and the capture limit.
The readonly root image has no file repair; proc/dev/tmp mounts are guest-only
runtime additions, just as device/proc filesystems are runtime rather than OCI
layer contents. VM has1CPU,1GiB RAM,no NIC or block device, readonly root/probe/
Rosetta shares; only guest virtual devices are exposed. No host module, profile,
trust or installation changes. Same frozen kernel/modloop/registration setup from
[guest binfmt01](OWNED-GUEST-BINFMT-01.md).

[VM source](results/owned-native-pytest-01/probe.swift) has180-second guest deadline;
independent parent watchdog200 seconds with owned process-group TERM/KILL cleanup,
pytest subprocess30 seconds, nested native child10 seconds. All observed processes
terminate normally after each VM; owned volume detached after collection.

## Remaining scope

No official test/issue/gold body is used, no selected case is replaced or scored,
and no solver runs. These related authored fixtures prove basic native pytest
assertion/capture/subprocess functionality, not prepared selected-source parity,
TLS/HTTP fixture readiness, official parser/FAIL-PASS grading, OCI UID/GID/capability
or amd64-kernel equivalence. No model work/token/time comparison or all8 release
adoption follows. Preserve original adverse measurements and continue exact-case
runtime preparation under a distinct private author protocol.

한국어: 공식 실행 환경에서 실제 pytest가 동일 테스트의41 반환을 실패,
42 반환을 통과로 구분했고 두 실행 모두 자식 Python 테스트를 통과했다.
첫 출력 수집 누락과 `/dev/null` 없는 초기 실행 실패를 보존했다. 기본 게스트
장치를 연결해 해결했으며 공식 선택 과제·모델·토큰 절감 측정은0회다.
