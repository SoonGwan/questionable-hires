# pytest5221 official-container pair01 — 2026-09-28

**Required test behavior separates, but the full official-script gate fails.**
Both original cells run once in the pinned official image: base2 required failures
and170 required passes; gold172 required passes. The script's editable installation
fails in both cells because its isolated build cannot resolve `setuptools>=40.0`
with container networking disabled. Tests continue against the preinstalled source.
Do not report this as a successful complete official evaluation or model savings.

[Protocol](EXTERNAL-BUNDLE-02-PYTEST5221-CONTAINER-01-PROTOCOL.md) `91818767`,
preflight correction `6a1fd352`, parent `32e0f136`. Selected base
`4a2fdce62b73944030cff9b3e52862868ca9584d`, unchanged official script SHA256
`950987985c71231ea07667924061f204b67af5d249098b35833f08e5fa05fad3`.
[Original summaries](results/external-bundle-02-pytest5221-container01/grade-summary.json)
retain both rejected cells, original output/observer hashes and unfiltered report
counts. [Separate derived observations](results/external-bundle-02-pytest5221-container01/derived-observations.json)
explain nested pytester reports and installation failure without rewriting them.

| Actual observation | Base | Gold |
| --- | --- | --- |
| Original FAIL_TO_PASS labels, unchanged parser |2 failed|2 passed|
| Original PASS_TO_PASS labels, unchanged parser |170 passed|170 passed|
| Top-level native collection |173|173|
| Extra top-level item |1 xfail|1 xfail|
| Actual pytest session exit |1|0|
| Official shell exit |0|0|
| Editable build dependency phase |failed|failed|
| Complete official-script readiness |rejected|rejected|

The official script uses `set -uxo pipefail`, without errexit. Its final checkout
returns0 even when editable installation or pytest fails; neither shell exit nor
container exit alone is an evaluation verdict. Original stdout is parsed with the
unchanged official `parse_log_pytest`; no label normalization, invented status
lines or requirement omissions. Gold alone receives the original gold patch;
both receive the exact original script with its embedded test patch. No issue
replacement or grading retry occurred. The earlier [Mac full-file success](EXTERNAL-BUNDLE-02-FILE-PROBE-01.md)
and original literal-selector failure remain distinct historical results.

The passive observer also receives928 nested in-process pytester reports per cell.
Its first unfiltered aggregation misleadingly counts24 setup/teardown failures and
extra call outcomes. These are **not top-level infrastructure/test failures**.
A separate post-run view uses the original command's `testing/python/fixtures.py`
prefix:519 reports for173 unique items, zero top-level setup/teardown failures,
and the table's outcomes. The primary session exits1/0 were recorded correctly.
Keep the original aggregation and this limitation accessible. A future observer
should associate reports with the collected primary session; no new run is used
to conceal or replace these original observations.

## Runtime, controls and attempts

Pinned Linux/amd64 manifest `c190b1e0539cef0e292e5c6e6219734f298d1bdee17189e497c5b116d8c0ca7f`,
config `1718609d2c1e3a6d929eb4643f8474ee9e8f551cab77847f6c492dd0df6f1701`.
Seven cached layers are reused and verified; three new layers total365,275,166bytes.
All10 compressed hashes and decompressed diffIDs match. Docker load matches the
config/ordered rootfs; transport1,025,525,760bytes, overlay2. No image extraction
on the host. Full [identities and attempts](results/external-bundle-02-pytest5221-container01/identities-and-attempts.json)
and [transport evidence](results/external-bundle-02-pytest5221-container01/transport.json)
are separate from performance measurements.

Actual Python3.9.20 imports pytest4.4.2.dev174+g4a2fdce62.d20260815 from
`/testbed/src/pytest.py`. All433 selected archive file bytes match. The official
image has432 executable-mode differences and synthetic HEAD
`c0698ad6368fb4dfda4e3d2b8dab498874793848`; standard Docker does not remove these
image preparation differences. Generated version metadata is the image's existing
metadata, not a new agent-authored fix or a relabeled selected base.

The first metadata request assumes a direct manifest and stops on an OCI index.
A subsequent descriptor inspection pins the unique Linux/amd64 image before any
blob acquisition. Original preflight then fails when it writes into the copied
input directory: dropped capabilities do not let root override its guest-user
ownership. Preserve the actual PermissionError and lack of a recorded first child
outcome. Distinct preflight02 creates its own output directory; actual pytest
assertions exit0/1, with assertion diagnostics for failure and no support exception.
A later read-only result lookup assumes a flat transfer layout and fails; the
actual retained nested directory is used without copying or evaluating again.

All controls/cells retain network none, no host mounts, cap-drop ALL,
no-new-privileges, default seccomp,1GiB memory,1CPU and64 PIDs. The disposable root
is writable as declared before evaluation. Zero timeouts/OOMs or protection changes.
[Cleanup](results/external-bundle-02-pytest5221-container01/cleanup.json) verifies
zero containers, three inactive/disabled guest services, stopped VM and no owned
Lima/SSH processes. Private patches, labels and raw issue logs remain outside the
repository and any future solver context.

The next useful change is to supply pinned offline build dependencies and correct
primary-session observer accounting before freezing a distinct protocol. Do not
rerun the unchanged pair or relax network restrictions simply to obtain green.
The separate [model execution approval blocker](SOLVER-EXECUTION-ENVIRONMENT-REQUEST-01.md)
is unresolved; this author-only work makes zero model calls and demonstrates no
whole-task token/time gain, all-eight readiness or quality superiority. Installed
skills, featured benchmark and hosted landing release are unchanged.

한국어: 공식 이미지의 원본2개 실패·170개 통과, 정답172개 통과와 실제 pytest
종료1/0을 확인했다. 그러나 양쪽 모두 앞단 설치가 오프라인 빌드 의존성을 찾지
못해 실패했으므로 공식 평가 전체 성공으로 채택하지 않는다. 셸 종료0은 성공
근거가 아니다. 중첩 pytester 보고를 섞은 최초 집계와 권한·경로 조회 오류도
보존하고 별도 해석을 제공한다. 실행 제한을 유지했고 컨테이너·서비스·VM을
종료했다. 모델 호출0회이며 전체8개 토큰·시간·품질 개선 근거가 아니다.
