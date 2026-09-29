# pytest5103 official-container preparation01 — 2026-09-28

Parent `9e30421b`. Author-only preparation for the already selected external case;
zero model calls. The historical [Mac cache probe](EXTERNAL-BUNDLE-02-PYTEST5103-CACHE-REVIEW.md)
separates one original failure and64 required passes after changing Apple's cache
prefix option. Preserve that result and original grade01's adverse cache check.
This distinct route uses the official Linux image and unchanged evaluation body.
Do not repeat accepted pytest5221/11143 pairs or change selected cases/labels.

Registry metadata is pinned once for repository
`swebench/sweb.eval.x86_64.pytest-dev_1776_pytest-5103`: index
`1648c614485c81d9e08bcf9ec8014fb38cd2f20fad6bea782552d923a35ce714`,
Linux/amd64 manifest
`d873716d5de2e1caaf0f4046a37b9c376e6137022fd9a1b7b47a8292dc428771`, config
`6685f236ddea92e412c046f1276f178d34895e4efbda2830ac3ab81903364787`.
Reverify eight cached compressed layers; acquire only the two missing blobs,
365,530,348bytes. All ten compressed hashes and uncompressed diffIDs must match.
Reuse existing transport/load scripts. Bounds:512MiB/600seconds acquisition,
10GiB/600seconds decompressed verification,5GiB transport,600seconds each transfer
and load,8GiB host/guest free space. No host image extraction or package install,
registry refresh, automatic retry or change to the owned VM configuration.

The selected source requires setuptools>=40, setuptools-scm and wheel. Reuse the
exact three already verified wheels from pytest5221 pair02: setuptools75.1.0,
setuptools-scm3.5.0, wheel0.44.0, total1,341,745bytes. Verify their recorded hashes
and copy to a private offline wheelhouse; no new dependency download is needed.
This explicitly prepared build environment is not the default image. Keep normal
build isolation and `python -m pip install -e .`, using PIP_NO_INDEX/PIP_FIND_LINKS.
No no-build-isolation flag or production/test repair to make setup pass.

Use the existing Lima author VM, Docker and Rosetta. Fresh writable disposable
container, network none, no host mounts, cap-drop ALL, no-new-privileges, default
seccomp,1GiB/1CPU/64PIDs. Controls have180-second lifecycle/90-second install limits.
Verify all418 selected-base source bytes before/after installation. Record actual
image Git identity, Python version, native cache prefix, source pytest import and
generated version metadata; do not relabel synthetic image history or claim mode
equivalence from byte checks. Default Linux cache behavior remains unchanged.

Reuse the byte-identical primary-session observer and pass/assertion-fail/nested
controls from pytest5221 pair02. Require actual editable-install success without
ERROR diagnostics and a fresh `/testbed/src/pytest.py` import. Passing control0,
intended value assertion1; inner failing pytest1 with outer pass0 and only the
outer item/three phase reports observed. Any failure remains recorded. Public
dependency inputs may be0644/0755 within private author root0700; issue patches,
labels and raw logs remain private and outside solving contexts.

Original evaluation body SHA256 is
`4fb5a5c9fb54a596c6dd720e30afbca905336730c2d656a3b6062e5bb4a82307`.
This preparation protocol does not run its issue cells. Freeze completed controls,
drivers, private inputs and unchanged scoring obligations separately before one
base/gold pair. Native preparation does not resolve the model-tool approval limit
or establish full-cohort readiness, independent model quality or token savings.
Remove every owned container and stop guest services/VM, verifying terminal state
after success or failure. Skills, public landing, charts and whole-task metrics
remain unchanged.

한국어: 이미 선택한 pytest5103의 공식 Linux 이미지에서 설치·실행 조건을
검증한다. Mac 캐시 호환성 결과와 원본의 불리한 결과는 보존한다. 기존 이미지
레이어·의존성·관찰기를 재사용하며, 설치와 정상/실패/중첩 대조군을 확인한 뒤
별도 계획을 고정해야 이슈 원본·정답을 검증한다. 모델 호출·절감 근거는 없다.
