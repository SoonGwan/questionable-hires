# Pinned harness runtime lookup — 2026-09-27

Parent `a2a993c3`, unchanged skills `7172b50c`, no models or case reruns.
The complete GitHub tree at frozen harness revision
`02e7a74ffd0b707aab73d203fe87bdc7c76afc8e` was fetched successfully; three
generic source files were downloaded and verified against their Git blob IDs.
[Identities/audit](results/external-bundle-02-official-runtime-index/) preserves
exact URLs and hashes. Guessed historical constants/python.py and constants.py
paths returned404; they are not valid runtime sources for this revision.

The pinned [test-spec constructor](https://github.com/SWE-bench/SWE-bench/blob/02e7a74ffd0b707aab73d203fe87bdc7c76afc8e/swebench/harness/utils.py)
consumes enriched instance image, evaluation script and parser fields. The pinned
[image constructor](https://github.com/SWE-bench/SWE-bench/blob/02e7a74ffd0b707aab73d203fe87bdc7c76afc8e/swebench/image_builder/image_spec.py)
consumes a supplied Dockerfile. Neither inspected constructor establishes the
selected old Requests runtime from its version alone. Do not assume Python2
would restore the missing regression contrast. Inspect selected enriched row,
image configuration or frozen task metadata privately before another runtime.
Those can include answer-bearing evaluation scripts; export identities and
environment facts only and exclude them from model solving contexts.

Current PATH/common install/socket probes find no Python2 or Docker/Colima/OrbStack
command or common local daemon socket. These narrow checks do not prove no
runtime exists elsewhere. Historical pilot Colima execution is historical evidence,
not present availability. No global installation, VM startup or source mutation
was performed by this lookup. All8 quality/token/time objective remains active.

한국어: 공식 고정 리비전의 실제 파일·Git blob을 확인했다. 현재 평가 환경은
버전별 상수 파일만 보고 정할 수 없으며 선택 행의 이미지·평가 스크립트 등
별도 메타데이터를 확인해야 한다. Python2를 쓰면 해결된다고 추측하지 않는다.
확인한 일반 경로에는 실행기와 소켓이 없지만 다른 경로까지 없다고 단정하지 않는다.
