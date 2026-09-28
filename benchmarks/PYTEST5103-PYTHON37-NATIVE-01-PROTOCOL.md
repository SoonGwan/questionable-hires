# pytest5103 Python37 native preparation01 — 2026-09-28

Parent `eb7326a1`; follows [runtime preparation01](PYTHON37-RUNTIME-01.md).
Author-only installation/control gate, zero models. This deliberately prepared
Python3.7 environment is distinct from the rejected official Python3.9 pair.
No original issue test/patch/label is executed or copied in this preparation.

Use the already loaded Python3.7 image config `db1238b04cccbbd9feb8398d29e8efcd98f02b7912b7e308dea9d1cca63392ce`.
Export only the418 hash-verified selected source files and existing Git metadata
from one fresh stopped-then-run official5103 container, config
`6685f236ddea92e412c046f1276f178d34895e4efbda2830ac3ab81903364787`,
synthetic HEAD `5df4d131d551b79b9fcf258482eaa4f59bf238b8`.
Do not synthesize a tag/version or transfer its installed Python packages/generated
version module. Export <=512MiB, reject symlinks; destination extraction accepts
only regular relative files without parent traversal. Record raw source equality,
actual Git HEAD and generated version; image file-mode differences remain disclosed.

Offline wheel closure: setuptools57.5.0 (same as new image), setuptools-scm3.5.0,
wheel0.41.3, atomicwrites1.4.0, attrs19.1.0, more-itertools7.2.0, packaging20.9,
pluggy0.13.1, py1.11.0, pyparsing2.4.7, six1.15.0, toml0.10.2, wcwidth0.2.5,
importlib-metadata1.7.0 and zipp1.2.0. Wheel metadata confirms Python3.7 support;
pluggy requires importlib-metadata below3.8, which requires zipp. Reuse historical
legacy wheels; three additional wheels verified against version-specific PyPI
metadata. Total15 wheels/1,331,621 bytes. Freeze exact hashes before native work.

One fresh Python3.7 container installs the wheels offline, then unchanged source
with ordinary `pip install -e .` and build isolation. No forced version, test/source
patch, conda shim or warning suppression. Check all418 source hashes before/after,
fresh public pytest import from outside source, generated metadata, and pip check.
Record all installed packages. Exercise existing authored pass, deliberate value
failure and nested failure controls with the unchanged primary-session observer.
Require native exits0/1/0, one primary item/three reports each, intended assertion
values in failing output, and nested child failure excluded from primary reports.
Any failed stage remains a failure; do not continue to original issue grading.

Each container: no network/mounts, all capabilities dropped, no-new-privileges,
default seccomp,1GiB/1CPU/64PIDs. Source export <=60s; each pip operation <=90s,
native control <=25s, total preflight <=300s. Inspect actual state/OOM and remove
owned containers in finally. Require >8GiB guest free space before starting work;
if needed, remove only an already-loaded redundant guest archive after verifying
its SHA against the retained host copy and existing transport record. Do not
delete images or unrelated resources or reduce the threshold.

All terminal paths stop Docker/socket/containerd, verify inactive/disabled, stop
the owned VM and check no owned Lima/SSH process. Preserve source/dependency/setup
failures; expose only authored evidence and hashes. No skill, featured or public
release change, no efficiency claim. Passing controls alone do not establish
original issue correctness or an unchanged official evaluation script: conda is
absent, and any later Python3.7 native issue pair needs its own explicit protocol.

한국어: 별도 Python3.7 컨테이너에서 원본 소스·Git 정보와 고정 의존성으로 실제
설치·새 프로세스 import·정상/실패/중첩 대조군을 검증한다. 원본 과제·정답 패치나
모델은 실행하지 않으며 경고 정책을 완화하지 않는다. 실패·버전·파일 모드 차이를
보존하고, 통과하더라도 공식 평가 본문 준비나 토큰 절감으로 계산하지 않는다.
