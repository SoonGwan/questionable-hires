# pytest5103 official-container pair01 — 2026-09-28

**The frozen native gate fails.** The original required label changes from failure
to pass and all64 required passes remain, but two additional primary tests fail
in both base and gold. Gold pytest exits1; the protocol requires0. Preserve this
adverse result rather than reducing the contract to required labels after execution.
There are zero model calls and no measured token/time improvement.

[Preparation protocol](EXTERNAL-BUNDLE-02-PYTEST5103-CONTAINER-01-PROTOCOL.md)
`2f174cd4`, frozen controls `241822e8`, and
[pair protocol](EXTERNAL-BUNDLE-02-PYTEST5103-PAIR-01-PROTOCOL.md)/completed controls
`4f517faa`. Exactly two issue cells run once. No registry refresh, replacement,
changed test/label/parser or unchanged retry. Historical
[Mac cache compatibility](EXTERNAL-BUNDLE-02-PYTEST5103-CACHE-REVIEW.md) covers a
different scoped required-test pair and remains historical.

| Original observation | Base | Gold |
| --- | --- | --- |
| Editable install success marker / ERROR diagnostics |present /0|present /0|
| Original FAIL_TO_PASS label |1 failed|1 passed|
| Original PASS_TO_PASS labels |64 passed|64 passed|
| Additional non-required primary failures |2|2|
| Primary passing / failing calls |64 /3|65 /2|
| Primary collected items / setup skips |72 /5|72 /5|
| Phase reports |211|211|
| Setup/teardown errors |0|0|
| Actual pytest exit |1|1|
| Official shell / container exit |0 /0|0 /0|

[Original scalar outcomes](results/external-bundle-02-pytest5103-container01/grade-summary.json)
retain parsed statuses, actual native outcomes, log hashes and the failed decision.
There are no ambiguous or unmapped required identities. Both native items and the
unchanged official parser satisfy the required-label projection; that does not
satisfy the separate native-exit requirement. Shell0 is not pytest0.

The [observer consistency check](results/external-bundle-02-pytest5103-container01/observer-consistency.json)
accounts for all72 items:67 have setup/call/teardown reports;5 skip during setup
and have a passing teardown, totaling211 reports. The reused grader's
`primary_unique_items=67` field counts call-bearing items, not all collected items.
Its unmodified parser likewise returns67 statuses and omits these setup skips.
The same two extra failing identities occur in both cells, outside the65 required
labels. They are actual primary failures, unlike embedded-output artifacts in the
earlier pytest11143 pair. Gold output includes two failed matches for an expected
assertion rendering in nested tests. This observation does not isolate the cause;
no source, runtime version, assertion or expectation is changed to make them pass.
Private required names, issue patches and raw issue logs remain outside the repo.

## Prepared environment and controls

Pinned Linux/amd64 manifest
`d873716d5de2e1caaf0f4046a37b9c376e6137022fd9a1b7b47a8292dc428771`, config
`6685f236ddea92e412c046f1276f178d34895e4efbda2830ac3ab81903364787`.
Eight cached layers are reverified and two absent blobs total365,530,348bytes;
all10 compressed hashes and uncompressed diffIDs match. The
[transport](results/external-bundle-02-pytest5103-container01/transport.json)
is1,025,771,520bytes. Loaded identity matches, overlay2, no declared volumes.
There is no host image extraction or host dependency installation.

Reuse exactly setuptools75.1.0, setuptools-scm3.5.0 and wheel0.44.0,
1,341,745bytes, already verified for pytest5221. Normal build isolation and the
original editable-install command use PIP_NO_INDEX/PIP_FIND_LINKS. This prepared
dependency set differs from the default image. All418 selected-source bytes match
before and after installation. File modes are not compared. Synthetic image Git
HEAD is `5df4d131d551b79b9fcf258482eaa4f59bf238b8`, not the selected base identity.

Fresh import resolves `/testbed/src/pytest.py`, Python3.9.20. Actual base version
is4.5.1.dev41+g5df4d131; gold adds.d20260928. Generated metadata changes during
installation. Linux `sys.pycache_prefix` is null with no Mac cache override.
[Original controls](results/external-bundle-02-pytest5103-container01/controls/)
show passing0 and intentional assertion failure1 with actual values. Nested
pytest fails1 while the outer test passes0; the observer records only that outer
item and its three phases. Reused artifact names end02, but no earlier controls
or issue pair for this case were discarded.

Both issue cells retain network none, no mounts, cap-drop ALL, no-new-privileges,
default seccomp,1GiB/1CPU/64PIDs, writable disposable roots and frozen150/180-second
limits. No timeout, OOM or infrastructure failure. All
[frozen input bytes](results/external-bundle-02-pytest5103-container01/frozen-input-check.json)
remain equal. [Cleanup](results/external-bundle-02-pytest5103-container01/cleanup.json)
confirms zero containers, three inactive/disabled services, VM Stopped and no owned
Lima/SSH processes.

This executes the official evaluation body/parser in a prepared image, not the
entire upstream harness. It establishes neither full-cohort readiness nor model
quality/cost improvement. The rejected model-tool authorization and other adverse
cases remain unresolved. Ordinary skills, installation, hosted release, featured
charts and integration07 costs are unchanged. Do not repeat this unchanged pair.

한국어: 원본의 필수 실패1개가 정답에서 통과하고 기존64개 통과도 유지되지만,
추가2개가 양쪽에서 실패해 정답 pytest 종료값이1이다. 사전에 정한 종료값0
조건을 만족하지 못하므로 전체 네이티브 검증은 불합격이다. 최상위72개 중67개는
3단계 보고,5개는 준비 단계 생략과 정리 보고로 총211개가 정확히 일치한다.
추가 실패를 중첩 출력이나 필수 항목 밖이라는 이유로 제거하지 않는다.
설치·정상/실패/중첩 대조군은 통과했고 원본 기록과 이전 Mac 결과는 보존한다.
모델 호출·절감 근거는 없으며 컨테이너·서비스·VM 종료를 확인했다.
