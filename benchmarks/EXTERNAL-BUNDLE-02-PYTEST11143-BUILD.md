# External bundle02 — pytest11143 native bootstrap, 2026-09-27

Parent `d255dd0c`; selected base `6995257cf470d2143ad1683824962de4071c0eb7`,
skill resource remains `7172b50c`. Author preparation only, zero model calls.
Earlier dependency and generated-metadata failures remain historical.

In a new owned temporary checkout, fetch the exact upstream base with depth500,
no automatic tags, isolated Git configuration and90-second subprocess limits.
A fetched7.3.1 tag is **not** its ancestor (exit1); that attempted assumption is
retained in [metadata steps](results/external-bundle-02-pytest11143-build/metadata-summary.json).
Do not derive a version from that tag. Instead match upstream tag/peeled identities
against commits actually reachable from the base. Fetch the first reachable tag
in the base rev-list order: `8.0.0.dev0`. Native merge-base validates ancestry,
and native describe yields `8.0.0.dev0-53-g6995257c`. This is a bounded shallow
checkout, not a claim of complete upstream history or nearest tag among absent refs.
Only base checkout contents were examined; no issue solutions/gold were read.

All578 tracked paths equal the prior exact-base archive in path and SHA256,
both before the build comparison and after native controls. The retained
[tracked hashes](results/external-bundle-02-pytest11143-build/tracked-source-hashes.json)
make the after-build comparison reviewable. Git tracked diff remains empty.

Using the earlier owned Python3.11 environment, execute the unchanged project's
build through `pip --isolated wheel --no-build-isolation --no-deps --no-index`.
This uses only prepared build dependencies, downloads nothing and installs no
pytest distribution. Original build generates `src/_pytest/_version.py` with
version `8.0.0.dev53+g6995257c`; no fabricated file or pretend-version environment
variable is used. Wheel build exits0. A fresh public import with PYTHONPATH set
only to this source's src exits0 and prints its actual source entry path/version.

Separate fresh native `python -B -m pytest` processes execute the retained tiny
[passing](results/external-bundle-02-pytest11143-build/test_pass.py) and
[failing](results/external-bundle-02-pytest11143-build/test_assertion_fail.py) controls.
An owned empty pytest config avoids ancestor configs; plugin autoload is disabled,
TMPDIR and basetemp are owned and process timeout30seconds. Pass exits0 with
1 passed; fail exits1 with `assert 41 == 42` and1 failed. No support-code exception
is accepted. These are bootstrap controls, **not existing project tests or issue
regressions**. Original project test/dependency completeness remains unverified.

[Build/import](results/external-bundle-02-pytest11143-build/build-summary.json),
[controls](results/external-bundle-02-pytest11143-build/controls-summary.json) and
[reading copies](results/external-bundle-02-pytest11143-build/reading-copies.json)
retain original byte hashes and path-redacted deterministic gzip logs. Raw outputs,
wheels, generated files and upstream history remain in the owned local preparation
root; none is model evidence. Solver snapshots still require removal of upstream
history, fresh-project provenance, frozen runtime and required native project tests.
Do not launch model comparisons until every selected issue's gates pass.

한국어: 실제 원본 커밋과 조상 태그를 확인해 프로젝트 자체 빌드로 버전 파일을
생성했다.578개 tracked 파일이 원본 아카이브와 같고, cold import 및 정상/실패
native assertion 검사가 통과했다.7.3.1 태그의 조상 검사 실패도 보존한다.
기존 프로젝트 검사·이슈 해결·모델 효율 검증은 아니며 다른 과제 준비가 남아 있다.
