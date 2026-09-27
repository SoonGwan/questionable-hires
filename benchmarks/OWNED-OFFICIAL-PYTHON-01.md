# Owned official Python01 — actual interpreter gate

Dated checkpoint **2026-09-27**, protocol/resource `905eb299`, parent
`51134006`. [Frozen protocol](OWNED-OFFICIAL-PYTHON-01-PROTOCOL.md).
**Zero model turns and zero external benchmark cases.** Eight installed skill
sources and the featured benchmark are unchanged.

The pinned official Requests2674 environment layer and Ubuntu OS base libraries
now execute Python in an owned ARM Linux guest through explicit Rosetta invocation.
This advances runtime feasibility, not a quality or token-saving measurement.

## Observed execution

[Actual outcome](results/owned-official-python-01/result.json) records Python
**3.9.20**, guest machine **x86_64**, OpenSSL **3.0.15**, pytest **7.4.4** and
pluggy **1.0.0**. The ssl/pytest/pluggy module paths all resolve under the selected
`/runtime/env` environment. The `-I -B` interpreter imports return exit0;
VM guest poweroff and parent exit0 occur within **5.342 seconds**, with no deadline
hit. [Console reading copy](results/owned-official-python-01/guest-console.txt)
normalizes CR and trailing whitespace; the original byte digest remains in the
outcome. Exit0 alone was not accepted: the controller requires marker, version,
module-path, Python exit and guest-stop evidence.

[Extraction outcome](results/owned-official-python-01/extraction-result.json)
records 7,537 environment regular files/1,289 symlinks, 188,935,442 file bytes,
and 1,007 OS-library regular files/63 symlinks, 46,312,027 file bytes. No selected
links were skipped or absolute links relocated in this actual copy. The extractor
still enforces path/link bounds, size limits, layer hashes and a 180-second streaming
deadline; it does not extract project, evaluation script or gold files.
The base layer was downloaded and SHA256 checked in 1.422 seconds.

## Retained failures and filesystem intervention

The first extraction exited1 at case-variant terminfo files `Eterm`/`eterm` on the
case-insensitive Mac filesystem. Its partial tree and
[first original log](results/owned-official-python-01/extraction-original.log)
remain preserved. No terminfo entry was dropped to produce a passing copy.
An initial `hdiutil -type UDSB` command exited1: that help-output token is not the
accepted CLI spelling. `-type SPARSEBUNDLE` successfully created a fresh owned
2GiB Case-sensitive APFS image. Only this new image was attached at a private
mountpoint; no preexisting disk was formatted or modified. The **unchanged**
extractor then copied the same pinned layers successfully in 4.662 seconds.
[Attempt record](results/owned-official-python-01/retained-attempts.json).

## Runtime boundary and limitations

The [VM source](results/owned-official-python-01/probe.swift) uses the prior
frozen raw ARM kernel/initramfs, one CPU, 512MiB RAM, no network or storage device,
a Rosetta share and one readonly runtime share. The guest RAM filesystem receives
only `/lib64/ld-linux-x86-64.so.2` pointing to the extracted OS loader; guest-only
`LD_LIBRARY_PATH=/runtime/env/lib:/runtime/glibc` selects native libraries.
No host profile, global binfmt, trust store or Rosetta installation was changed.
The [controller](results/owned-official-python-01/control.py) bounds its own
process group at 35 seconds, with TERM/KILL cleanup; Swift also has a 25-second
guest deadline. The temporary volume is detached after collecting evidence.

This is a **selected relocated runtime subtree**, not application of every OCI
layer or full filesystem parity. There is no project import, pytest execution,
benchmark FAIL/PASS control, solver run, native grading or whole-task token/time
comparison here. Frozen adverse model measurements remain adverse. Official-case
preflight requires a separate protocol and exact source/test/label boundaries.

한국어: 공식 이미지의 Python3.9.20과 ssl·pytest·pluggy를 VM에서 실제로
실행하고 버전·경로·종료를 확인했다. 처음의 대소문자 파일명 충돌과 이미지
생성 인자 오류는 보존했다. 같은 원본을 임시 대소문자 구분 볼륨에 복사한
결과이며, 전체 이미지 재현·공식 테스트 통과·전체8개 스킬 품질·토큰 절감을
입증한 결과가 아니다. 모델 실행과 외부 과제 재실행은 모두0회다.
