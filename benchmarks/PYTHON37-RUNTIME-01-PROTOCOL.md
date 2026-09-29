# Python37 runtime preparation01 — 2026-09-28

Parent `91c36c4d`. This is author environment preparation, not a new model
experiment or a replay of the rejected pytest5103 pair. Original selected CI
uses Python3.7; its Python3.8-dev job is allowed to fail. The prior
[warning-policy diagnosis](EXTERNAL-BUNDLE-02-PYTEST5103-REWRITE-01.md) established
a native rewrite boundary on Python3.9, without repairing the issue gate.

Before acquiring layers, pin Docker Official Image `library/python` tag
`3.7.17-bullseye`, linux/amd64:

- index `f36f6fe9ddb2622aab9803944cbe7e2bc50be75d624a081f7895e60e7c6b7f0a`
- manifest `47287d2f807e18545ef0c10941cc884835970fc9da43debabad1461b2782adde`
- config `db1238b04cccbbd9feb8398d29e8efcd98f02b7912b7e308dea9d1cca63392ce`
- 8 compressed layers,346,359,955 bytes; declared Python3.7.17.

Reuse the existing SHA256/diff-ID Docker transport and owned Lima environment.
Limits: >8GiB free before acquisition/load, downloads <=512MiB/600s,
uncompressed verification <10GiB/600s, transport <5GiB, load <=600s.
No host layer extraction or global package install. Keep the existing image and
host archives. If guest space is insufficient, stop rather than relaxing limits.

Freeze one fresh container per runtime: new pinned Python3.7 image and existing
pytest5103 Python3.9 image `6685f236ddea92e412c046f1276f178d34895e4efbda2830ac3ab81903364787`.
Each runs the exact [compiler probe](probe_python37_runtime.py), with no project
source, gold, test patch or original labels copied into the new image. The old
image already contains its base checkout; the probe neither imports nor reads it.
Each cell records version, executable, Git/conda availability, and six compile-only
outcomes: numeric identity guard, variable identity guard, invalid-syntax control,
under default warnings and SyntaxWarning-as-error. No executing compiled code.

Prediction: numeric identity guard compiles without warning on3.7, emits warning
on3.9/default, and fails compilation on3.9/error; variable guard compiles on both;
invalid source fails on both. Any mismatch stays recorded and prevents claiming
this prerequisite established. This synthetic guard cannot establish actual
pytest loading, successful installation, original issue correctness or token saving.
It determines whether preparing a separate3.7 native grading environment is useful.
Git and conda are observations, not assumptions; absent conda means the original
official evaluation body is not runnable unchanged here.

Containers: network none, no mounts, all capabilities dropped, no-new-privileges,
default seccomp,1GiB/1CPU/64PIDs, writable disposable root, <=60s each.
Capture actual exit/OOM states and all outputs; remove owned containers in finally.
Stop Docker/socket/containerd, verify disabled/inactive, stop VM and verify no
owned Lima/SSH processes. Export only authored probe, image identity, outcomes and
cleanup evidence. Zero models, no skill/featured/public-release change. No retry
to replace adverse observations or acceptance of a relaxed original issue gate.

한국어: 원본 CI의 Python3.7에 맞는 별도 실행 환경을 준비하고, 경고 처리 차이가
해당 인터프리터에서도 존재하는지만 고정 대조한다. 원본 사례나 모델을 실행하지
않으며 설치·채점·토큰 절감 성공으로 계산하지 않는다. conda가 없으면 공식 평가
본문을 그대로 실행할 수 없다는 제한을 유지한다. 종료 후 환경 정리까지 확인한다.
