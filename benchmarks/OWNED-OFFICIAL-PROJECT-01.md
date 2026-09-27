# Owned official project01 — actual source import, child exec failure

Dated checkpoint **2026-09-27**, protocol/resource `b2e6f8b1`, parent `306def1d`.
[Protocol](OWNED-OFFICIAL-PROJECT-01-PROTOCOL.md),
[actual outcome](results/owned-official-project-01/result.json),
[observed marker whitelist](results/owned-official-project-01/observed-markers.txt).
Zero model turns and selected-case tests. Installed8skills and featured data unchanged.

The existing private [reconstructed root](OWNED-OFFICIAL-ROOT-01.md) was mounted
readonly; no layers were reapplied. Guest-only proc/tmpfs and readonly probe/Rosetta
shares permit observation without changing image files. Python `-B` uses the real
`/testbed` working directory and ordinary current-directory import behavior, rather
than the prior `-I` installed-package scope. Actual Requests now comes from
**`/testbed/requests/__init__.py`**, version2.7.0. Its opaque file hash equals the
previous installed copy's hash; equality of this one file is not full source-tree
or selected-base preparation parity. Official interpreter and prefix remain
`/opt/miniconda3/envs/testbed/bin/python3.9` and its exact environment path.
No source, package or dependency repair was applied.

**Automatic x86 child execution failed:** the actual project-side interpreter
invoked `subprocess.run([sys.executable,'-I','-B','-c','print(6*7)'],...)` without a
shell or alternate route. Native observation returned **OSError errno8**
(`Exec format error`), not the expected childexit0/stdout42. This is a retained
readiness failure, not a passing child-execution test. Explicit Rosetta runs the
parent, but automatic subprocess/shebang execution remains unavailable without a
working guest routing mechanism. No selected case was rerun to hide this result.

The [probe](results/owned-official-project-01/fixture/probe.py) records source and
child outcomes separately. [Controller](results/owned-official-project-01/control.py)
requires actual source path, interpreter observation/Pythonexit0 and guest stop;
controllerexit0 means **observation and source-import checks passed**, never that
child execution passed. First VM observation completed in5.014 seconds, no timeout,
with the same180-second guest/200-second independent parent watchdog. Only the owned
process group may be terminated. Original2,325-byte private console SHA256 remains
in the outcome; public console is a marker/JSON whitelist rather than full transcript.
The owned root sparse image is detached and preserved privately after collection.

Next prerequisite is exact-kernel guest binfmt availability/registration and a
fresh controlled child observation. Do not bypass model-tool approval restrictions,
register anything on the host, substitute a shell result for this native failure,
or claim full amd64-kernel/OCI ownership/test/quality/token parity. No model cost
comparison occurred; original adverse resource-specific measurements remain unchanged.

한국어: 이번에는 공식 작업 디렉터리 `/testbed`에서 실제 프로젝트 import를
확인했다. 그러나 x86 Python이 자식 Python을 자동 실행하는 동작은 errno8로
실패했다. 관측 프로세스의 종료0은 자식 실행 성공이 아니며 원본 실패를 보존한다.
게스트 실행 경로를 검증하기 전에는 자식 프로세스가 필요한 공식 테스트의 준비
완료를 주장하지 않는다. 모델·선택 과제·토큰 절감 측정은 모두0회다.
