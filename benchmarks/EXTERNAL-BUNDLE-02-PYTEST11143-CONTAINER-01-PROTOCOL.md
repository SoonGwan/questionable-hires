# pytest11143 official-container preparation01 — 2026-09-28

Parent `342f9e84`. Author-only preparation for an already selected external case;
zero model calls. The earlier Mac full-file probe already separates the original
one FAIL_TO_PASS and114 PASS_TO_PASS labels. Preserve its selector ambiguity and
all actual items. This distinct check asks whether the official Linux image can
install and run its own pytest offline under the existing owned Docker runtime.
It does not repeat the accepted pytest5221 pair or the adverse Requests2674 pair.

Pin registry metadata once: repository
`swebench/sweb.eval.x86_64.pytest-dev_1776_pytest-11143`, OCI index
`e08ce142adec5ec985e867e910045734ec3c58fe174fc054c5f83855bed78fd4`,
Linux/amd64 manifest
`4cf4b5ad2fc8141940f60947e0fe534075bb337723368408eb658c198b8e5850`, config
`c4299ec247332c00e7016f5fbfcdb5bc8fd733585b3d28b897fcd7a6c50d32e2`.
Reverify seven cached layers; acquire the three absent blobs totaling369,447,240
bytes. Reuse the existing digest/diffID verification and Docker transport scripts.
Bound acquisition at512MiB/600seconds, decompressed verification10GiB/600seconds,
transport5GiB, transfer/load600seconds each; require8GiB host/guest free space.
No host extraction, package installation, registry refresh or automatic retry.

Use the owned Lima author VM, existing Docker and Rosetta. Disposable containers:
network none, no host mounts, cap-drop ALL, no-new-privileges, default seccomp,
1GiB/1CPU/64PIDs, writable disposable root. Compare all578 selected-base source
hashes before/after building. Record image Git identity, actual entrypoint/version
and preparation differences; never fabricate version metadata or normalize it.

The original evaluation script hash is
`a5663e841a4fe2f1e3f0a3b7605082583a273122a4de9af2c41e5cf2a70013f7`.
Its editable installation remains `python -m pip install -e .`, with normal build
isolation. Determine any offline build requirements from the selected source and
pin them before controls. Do not use no-build-isolation or repair source/tests to
make preparation succeed. Reuse the proven primary-session observer and positive,
negative and nested pytest controls; no nested reports may enter primary counts.
Verify a fresh actual public import, expected native exits and assertion messages.
Public dependency inputs may be0644 within the private0700 author root; private
gold/tests/logs stay private. Output is written into container-owned scratch.

This preparation protocol does **not** launch issue grading. Freeze the completed
controls, runtime/build inputs, drivers and original scoring obligations separately
before any base/gold cells. A preparation failure remains a failure, not a reason
to relax controls or run models. Publish only identities, authored controls and
scalar summaries; keep original issue patches/labels/logs private. Remove owned
containers and stop services/VM, verifying terminal states even after failure.

The model-tool authorization blocker remains separate. Native preparation is not
independent validation, token savings or all-eight improvement. Existing exposed
integration07 remains+1.67% tokens/−9.63% elapsed; no model rerun is justified by
new packaging alone. Skills, landing, featured figures and historical results stay
unchanged during this preparation.

한국어: 이미 선정한 pytest11143의 공식 Linux 이미지에서 설치·실행 조건만
검증한다. 기존 Mac 결과를 재분류하거나 모델 절감으로 계산하지 않는다.
원본 소스578개와 런타임·의존성을 확인하고 정상/실패/중첩 대조군을 통과한 뒤
별도 채점 계획을 고정해야 한다. 이 단계에서는 이슈 채점·모델 호출을 하지 않는다.

## Frozen control inputs before execution

The selected source requires setuptools>=45 and setuptools-scm[toml]>=6.2.3.
An author metadata request for exactly6.2.3 returned HTTP404 before any control.
The first two wheel files were already verified; retain that acquisition failure
in a reconstructed scalar record (not a saved raw HTTP traceback). No runtime or
issue test ran during that attempt. Distinct wheelhouse02 pins setuptools75.1.0,
wheel0.44.0, setuptools-scm8.1.0, packaging24.1 and tomli2.0.1, all universal
wheels verified against the publisher's SHA256. The latter three are new downloads;
setuptools/wheel reuse verified prior bytes. This is an explicitly prepared build
environment, not the default image dependency set.

[Control freeze](results/external-bundle-02-pytest11143-container01/control-freeze.json),
[wheel identities](results/external-bundle-02-pytest11143-container01/wheels02.json)
and authored drivers are fixed before native controls. The primary observer is
byte-identical to pytest5221 pair02. All578 source hashes reuse the existing exact
base manifest; actual installed pytest must import `/testbed/src/pytest/__init__.py`.
Container removal uses finally even if result retrieval fails. One control container,
180-second lifecycle limit, no automatic replay. The grading prohibition above
remains: passing controls alone do not launch base/gold evaluation.
