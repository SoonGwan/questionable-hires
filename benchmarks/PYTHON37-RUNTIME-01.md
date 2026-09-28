# Python37 runtime preparation01 — 2026-09-28

Protocol `8f91ee4a`; [frozen scope](PYTHON37-RUNTIME-01-PROTOCOL.md),
[authored probe](probe_python37_runtime.py),
[raw observations](results/python37-runtime01/observations.json).
The pinned Python3.7 environment accepts the compiler shape rejected by the
existing Python3.9 environment under SyntaxWarning-as-error. This establishes
one prerequisite for a separate native environment, **not the pytest5103 gate**.

| Authored source and policy | Python3.7.17 | Python3.9.20 |
| --- | --- | --- |
| Numeric identity guard, default warnings | Compiles, no warning | Compiles, SyntaxWarning |
| Numeric identity guard, SyntaxWarning as error | Compiles, no warning | SyntaxError |
| Variable identity guard, either policy | Compiles, no warning | Compiles, no warning |
| Invalid syntax control, either policy | SyntaxError | SyntaxError |

All12 scheduled observations match the frozen prediction; both probe processes
exit0, recording expected compilation errors rather than counting them as test
passes. No compiled body is executed. These are two different prepared images,
not an experiment holding every dependency/OS constant. The actual prior native
loading failure remains documented in the
[warning-policy diagnosis](EXTERNAL-BUNDLE-02-PYTEST5103-REWRITE-01.md).

The original selected source `.travis.yml` declares Python3.7 at lines9/48 and
allows the3.8-dev job to fail at115–116; its hash is in
[review metadata](results/python37-runtime01/review.json). The new image has Git
at `/usr/bin/git`, but `conda` is absent from its configured PATH. Consequently
the original evaluation body cannot be claimed runnable unchanged. No project
source, gold or test patch was copied into the new image. No project installation,
pytest import, original test, original label, solver or model was exercised here.

The official Python image is pinned by
[registry identity](results/python37-runtime01/registry-identity.json) and
[loaded identity](results/python37-runtime01/loaded-identity.json). Eight layers
downloaded346,359,955 bytes; SHA256 and uncompressed diff IDs match. Uncompressed
verification covered925,497,344 bytes without host extraction. The Docker transport
is346,378,240 bytes, SHA256
`3d081372e8d79674c0a1ae45532ed4c91653fc9561381135d3e7f6636ceb8796`.
Both host and guest passed the unchanged8GiB free-space gates; load used overlay2.
[Transport evidence](results/python37-runtime01/transport.json) preserves each
digest/size. Host and guest transport copies and the loaded image remain available
for future explicitly prepared native work; no archive deletion was necessary.

Both containers used network none, no mounts, dropped capabilities,
no-new-privileges,1GiB/1CPU/64PIDs and exited without OOM. All frozen file hashes
still match. [Cleanup](results/python37-runtime01/cleanup.json) confirms zero
containers, all three services inactive/disabled, VM stopped and no owned
Lima/SSH process. Prior native failures remain adverse. Skills, installed resources,
featured data and public release `281c3cf0` are unchanged. Zero model calls and no
token/time efficiency evidence.

Next prerequisite, if pursuing this selected case: prepare compatible offline
dependencies and exact source metadata under a separately frozen native protocol,
then verify fresh imports and actual passing/failing test controls. Do not fake
conda activation, suppress warnings, alter original labels, or replay the rejected
Python3.9 pair unchanged. This runtime alone does not authorize a solver route or
establish full-cohort readiness.

한국어: 고정한 Python3.7 환경에서는 숫자 비교 대조군이 경고 없이 컴파일되고,
기존3.9 환경에서는 경고 오류 정책에 따라 실패했다. 예약한12개 관찰을 모두
보존했으며 원본 사례는 실행하지 않았다. 새 환경에 conda가 없어 공식 평가 본문을
그대로 실행할 수 있다고 주장하지 않는다. 의존성·소스 메타데이터·실제 pytest
실행 검증이 남아 있다. 두 컨테이너와 서비스를 정리하고 VM 종료까지 확인했다.
기존 불합격·전체8개 목표 미달 판단과 공개 수치는 유지하며 토큰 절감 근거는 없다.
