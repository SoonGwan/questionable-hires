# External-issue pilot: image feasibility, not task validation

2026-09-21, source checkpoint`5628ef2`. The two instances remain those selected
by [the frozen rule](SWE-LITE-PILOT-01-SELECTION.md); no replacement or model run.
[Ten read-only checks and original outputs](results/swe-lite-pilot-01-environment/)
retain commands, runtime exits and output hashes. This does not establish issue
resolution, native-test execution or any skill benefit.

## Pinned images and startup

The dataset image fields name the official `swebench` images below. Their manifests
advertise Linux/amd64, not this host's aarch64 architecture. Both were pulled once
with `--platform linux/amd64`, each with a600-second process limit, by digest:

| Instance/image suffix | Manifest digest | Compressed layer bytes |
| --- | --- | ---: |
| `sweb.eval.x86_64.psf_1776_requests-2317` | `sha256:a0ce096d4dfa27ca8ea80ae4b38103e970d17b19066d886a550936394827c9fb` |1015309228|
| `sweb.eval.x86_64.pytest-dev_1776_pytest-7432` | `sha256:0e556e33eec3eb68e7737ea264268a758197718006336b84bb5f0c99187cf066` |1026758618|

Layer sums are not incremental download/disk usage; images share layers. Both
pulls exited0. Colima remains on macOS Virtualization.Framework/aarch64. Both
images start in x86-64 compatibility mode, report Python3.9.20 and import the
project from `/testbed`: Requests2.4.3 and pytest5.4.1.dev593+ge6e300e72.d20260815.
Startup used no network/host mounts, read-only rootfs, dropped capabilities and
no-new-privileges. The first identity/import command had a45-second ceiling.
Compatibility-mode timing must not be described as native ARM performance.

## Source identity and a remaining isolation gate

Image HEADs differ from dataset base commits:

| Project | Image HEAD | Entries | Changed blob identities | Changed modes | Reachable commits across all refs |
| --- | --- | ---: | ---: | ---: | ---: |
| Requests | `ac2af6596a097252c97353aa2ec771591053b08b` |128|0|125|3690|
| pytest | `a0d8040ee4ee621e86a39ae62208596bc865c9c1` |541|0|539|12620|

`git ls-tree -rz` maps have exactly equal paths and object type/blob IDs versus
the selected base. Mode changes account for the differing trees. Base objects
exist in both images; their tree identities also match GitHub's base-commit API.
Initial `git status --porcelain` is empty. A plain Git comparison correctly
reports difference; we did not overwrite it with a false whole-tree identity claim.
Generated/ignored installation artifacts are not certified by a committed-tree
comparison, and imports are not a substitute for same-process native-test checks.

The raw images are **not ready for solving sessions**. Their broad Git object/ref
stores have not been certified ancestor-only. A future solver must receive only
the selected base source in a fresh repository, not those original Git databases
or answer-bearing evaluation materials. Preserve source bytes and original modes,
verify imports use the solver project, then execute native controls and separately
validate the frozen scoring environment. No source repair to accommodate the host
or author-made replacement test suite is justified by startup success.

## Attribution and unresolved redistribution scope

The harness repository at`02e7a74ffd0b707aab73d203fe87bdc7c76afc8e` identifies
[MIT licensing](https://github.com/SWE-bench/SWE-bench/blob/02e7a74ffd0b707aab73d203fe87bdc7c76afc8e/LICENSE).
The pinned [Requests license](https://github.com/psf/requests/blob/091991be0da19de9108dbe5e3752917fea3d7fdc/LICENSE)
identifies Apache2.0; pinned [pytest license](https://github.com/pytest-dev/pytest/blob/e6e300e729dd33956e5448d8be9a0b1540b4e53a/LICENSE)
identifies MIT. The dataset card metadata has no explicit license field. Do not
infer that the harness license automatically licenses every issue body; projected
issue text stays local, and this commit publishes only identity/environment facts.

An attempted old harness `test_spec/test_spec.py` URL returned404; the pinned tree
instead exposes `swebench.types` and `swebench.harness.utils.make_test_spec` in the
evaluation entrypoint. No guessed legacy harness was installed. Official
[evaluation documentation](https://www.swebench.com/SWE-bench/guides/evaluation/)
is background, not evidence we executed official grading.

한국어: 공식 이미지 두 개의 호환 실행과 패키지 import를 확인했다. 기준 커밋과
파일 내용은 같지만 실행 권한 및 Git HEAD가 다르다. 전체 Git 이력을 그대로
모델에 주지 않도록 격리한 뒤 실제 테스트를 검증해야 한다. 모델 호출·정답 패치
열람·채점·성능 향상 주장은 없고, 데이터 본문도 아직 공개 저장하지 않는다.
